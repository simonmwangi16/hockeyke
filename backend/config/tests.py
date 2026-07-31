import os
import subprocess
import sys
from unittest.mock import patch

from django.core.exceptions import ImproperlyConfigured
from django.test import SimpleTestCase

from config.settings.base import BASE_DIR, env_bool, env_list, required_env


class EnvironmentValueTests(SimpleTestCase):
    def test_env_bool_accepts_explicit_true_and_false_values(self):
        with patch.dict(
            os.environ,
            {"TRUE_SETTING": "yes", "FALSE_SETTING": "0"},
            clear=False,
        ):
            self.assertIs(env_bool("TRUE_SETTING"), True)
            self.assertIs(env_bool("FALSE_SETTING"), False)

    def test_env_bool_rejects_ambiguous_values(self):
        with patch.dict(os.environ, {"BOOL_SETTING": "sometimes"}, clear=False):
            with self.assertRaises(ImproperlyConfigured):
                env_bool("BOOL_SETTING")

    def test_env_list_trims_values_and_discards_empty_items(self):
        with patch.dict(
            os.environ,
            {"LIST_SETTING": "example.com, api.example.com,,"},
            clear=False,
        ):
            self.assertEqual(
                env_list("LIST_SETTING"),
                ["example.com", "api.example.com"],
            )

    def test_required_env_rejects_missing_or_blank_values(self):
        with patch.dict(os.environ, {"REQUIRED_SETTING": "  "}, clear=False):
            with self.assertRaisesMessage(
                ImproperlyConfigured,
                "REQUIRED_SETTING is required",
            ):
                required_env("REQUIRED_SETTING")

    def test_required_env_rejects_placeholder_values(self):
        with patch.dict(
            os.environ,
            {"REQUIRED_SETTING": "REQUIRED-replace-this"},
            clear=False,
        ):
            with self.assertRaisesMessage(
                ImproperlyConfigured,
                "REQUIRED_SETTING must not use a placeholder",
            ):
                required_env("REQUIRED_SETTING")


class SettingsSelectionTests(SimpleTestCase):
    production_environment = {
        "HOCKEYKE_ENV": "production",
        "DJANGO_SECRET_KEY": (
            "production-test-secret-with-at-least-fifty-characters-123456789"
        ),
        "DJANGO_ALLOWED_HOSTS": "hockeyke.example",
        "DJANGO_DB_NAME": "hockeyke",
        "DJANGO_DB_USER": "hockeyke",
        "DJANGO_DB_PASSWORD": "production-test-password",
        "DJANGO_DB_HOST": "database",
    }

    def run_settings_import(self, environment, code="import config.settings"):
        process_environment = os.environ.copy()
        for name in [
            "HOCKEYKE_ENV",
            "DJANGO_SECRET_KEY",
            "DJANGO_ALLOWED_HOSTS",
            "DJANGO_DB_NAME",
            "DJANGO_DB_USER",
            "DJANGO_DB_PASSWORD",
            "DJANGO_DB_HOST",
            "DJANGO_STATIC_ROOT",
            "DJANGO_MEDIA_ROOT",
        ]:
            process_environment.pop(name, None)
        process_environment.update(environment)

        return subprocess.run(
            [sys.executable, "-c", code],
            cwd=str(BASE_DIR),
            env=process_environment,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_development_is_the_default_environment(self):
        result = self.run_settings_import(
            {},
            "from config import settings; assert settings.DEBUG is True",
        )

        self.assertEqual(result.returncode, 0, result.stderr)

    def test_unknown_environment_fails_closed(self):
        result = self.run_settings_import({"HOCKEYKE_ENV": "staging"})

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("HOCKEYKE_ENV must be either", result.stderr)

    def test_production_rejects_missing_required_values(self):
        result = self.run_settings_import({"HOCKEYKE_ENV": "production"})

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("DJANGO_SECRET_KEY is required", result.stderr)

    def test_production_rejects_placeholder_secret_key(self):
        environment = self.production_environment | {
            "DJANGO_SECRET_KEY": "django-insecure-placeholder-value",
        }

        result = self.run_settings_import(environment)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("DJANGO_SECRET_KEY must be a non-placeholder", result.stderr)
        self.assertNotIn(environment["DJANGO_SECRET_KEY"], result.stderr)

    def test_production_rejects_missing_allowed_hosts_without_exposing_secret(self):
        environment = self.production_environment.copy()
        environment.pop("DJANGO_ALLOWED_HOSTS")

        result = self.run_settings_import(environment)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("DJANGO_ALLOWED_HOSTS", result.stderr)
        self.assertNotIn(environment["DJANGO_SECRET_KEY"], result.stderr)

    def test_production_rejects_incomplete_database_configuration(self):
        environment = self.production_environment.copy()
        environment.pop("DJANGO_DB_PASSWORD")

        result = self.run_settings_import(environment)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("DJANGO_DB_PASSWORD is required", result.stderr)
        self.assertNotIn(environment["DJANGO_SECRET_KEY"], result.stderr)

    def test_production_accepts_complete_required_values(self):
        result = self.run_settings_import(
            self.production_environment,
            (
                "from config import settings; "
                "assert settings.DEBUG is False; "
                "assert settings.ALLOWED_HOSTS == ['hockeyke.example']; "
                "assert settings.SESSION_COOKIE_SECURE is True; "
                "assert settings.DATABASES['default']['NAME'] == 'hockeyke'"
            ),
        )

        self.assertEqual(result.returncode, 0, result.stderr)

    def test_production_accepts_explicit_static_and_media_roots(self):
        environment = self.production_environment | {
            "DJANGO_STATIC_ROOT": "/home/hockeyk1/api.example/static",
            "DJANGO_MEDIA_ROOT": "/home/hockeyk1/api.example/media",
        }

        result = self.run_settings_import(
            environment,
            (
                "from pathlib import Path; "
                "from config import settings; "
                "assert settings.STATIC_ROOT == "
                "Path('/home/hockeyk1/api.example/static'); "
                "assert settings.MEDIA_ROOT == "
                "Path('/home/hockeyk1/api.example/media'); "
                "assert settings.STATIC_URL == '/static/'; "
                "assert settings.MEDIA_URL == '/media/'"
            ),
        )

        self.assertEqual(result.returncode, 0, result.stderr)
