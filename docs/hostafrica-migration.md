# HockeyKE HOSTAFRICA Migration Guide

This guide describes the proposed deployment of the HockeyKE Django backend and Vue frontend to HOSTAFRICA cPanel.

Do not commit database dumps, `.env` files, passwords, secret keys, private keys, or production credentials to Git.

## Recommended hosting layout

Use the main domain for the compiled Vue frontend and an API subdomain for Django:

```text
HOSTAFRICA account home
├── public_html/                 Vue production build only
│   ├── index.html
│   ├── assets/
│   └── .htaccess
│
└── hockeyke_backend/           Django source outside public_html
    ├── manage.py
    ├── config/
    ├── matches/
    ├── stats/
    └── passenger_wsgi.py
```

Proposed public addresses:

```text
Frontend:     https://yourdomain.com
API:          https://api.yourdomain.com/api/
Django admin: https://api.yourdomain.com/admin/
```

Keeping Django outside `public_html` prevents source files, settings, imports, and other internal files from being directly exposed. Using an API subdomain also avoids conflicts between Vue's client-side routing and the cPanel Python application.

## Before migration

1. Confirm the final domain name.
2. Ensure the domain uses HOSTAFRICA nameservers or suitable DNS records.
3. Create `api.yourdomain.com` in cPanel.
4. Enable SSL for the main domain, `www`, and the API subdomain.
5. Take a verified backup of the source database.
6. Do not upload or commit the database backup to Git.
7. Confirm that HOSTAFRICA offers Python 3.11 for the account.
8. Confirm how Apache or LiteSpeed will serve Django's collected static files.

## Create the MySQL database

In cPanel:

1. Open **MySQL Databases** or **MySQL Database Wizard**.
2. Create a database for HockeyKE.
3. Create a dedicated database user with a strong, unique password.
4. Grant that user only the permissions needed for the HockeyKE database.
5. Record the exact database and user names displayed by cPanel.

cPanel may prefix these names:

```text
Database: cpanelaccount_hockeyke
User:     cpanelaccount_hockeyuser
Host:     localhost
Port:     3306
```

Do not put these credentials in a committed file.

## Create the Python application

HOSTAFRICA's documented workflow is:

1. Open cPanel.
2. Go to **Software**.
3. Open **Setup Python App**.
4. Select **Create Application**.

Use these values, replacing domain placeholders:

| cPanel field | Value |
| --- | --- |
| Python version | Python 3.11 |
| Application root | `hockeyke_backend` |
| Application URL | `api.yourdomain.com` |
| Application startup file | `passenger_wsgi.py` |
| Application entry point | `application` |

The application root should not be `public_html`. The application URL and application root are separate settings.

Reference: [HOSTAFRICA — Setting up a Python app in cPanel](https://help.hostafrica.com/article/setting-up-a-python-app-in-cpanel)

## Passenger WSGI entry point

cPanel may generate `passenger_wsgi.py`. Inspect the generated file before changing it. It needs to load the existing Django WSGI application:

```python
import os
import sys

application_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, application_root)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

from config.wsgi import application
```

The existing HockeyKE `config.settings` package selects the environment-specific Django settings. Production is selected using `HOCKEYKE_ENV=production`.

## Configure production environment variables

Add production values through the cPanel Python application's environment-variable interface:

```text
HOCKEYKE_ENV=production
DJANGO_SECRET_KEY=<new-long-random-production-secret>
DJANGO_ALLOWED_HOSTS=api.yourdomain.com
DJANGO_DB_NAME=<exact-cpanel-database-name>
DJANGO_DB_USER=<exact-cpanel-database-user>
DJANGO_DB_PASSWORD=<strong-database-password>
DJANGO_DB_HOST=localhost
DJANGO_DB_PORT=3306
DJANGO_CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
DJANGO_CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com,https://api.yourdomain.com
DJANGO_SECURE_SSL_REDIRECT=true
```

Requirements:

- Generate a new production-only Django secret key.
- Do not reuse a development secret.
- Do not upload a `.env` file into `public_html`.
- Do not commit any real values.
- Use the precise comma-separated format expected by the existing settings.

## Prepare backend dependencies

The repository now includes `backend/requirements.txt`, containing the pinned
direct dependencies verified from the backend imports and working environment.
Follow the operational instructions in `docs/hostafrica-live-setup.md`.

After uploading the backend, activate the virtual environment command shown by
cPanel and install the manifest:

```bash
pip install -r requirements.txt
```

Do not install or update dependencies without reviewing and committing the dependency-file change first.

## Upload the Django backend

Upload the backend application files into the Python application root:

```text
/home/CPANEL_USER/hockeyke_backend/
```

Do not upload:

- A local virtual environment
- `.env` files
- `db.sqlite3`
- database exports
- Git credentials
- editor settings
- cache directories
- temporary import files unless they are explicitly required and safe

Restart the Python application from cPanel after changing application files or environment variables.

## Database import and migrations

Treat database import and schema migration as separate operations.

Before changing the hosted database:

1. Confirm the target database name and host.
2. Take a backup.
3. Confirm that the backup can be restored.
4. Import the source data using cPanel/phpMyAdmin or an approved database command.
5. Run a read-only Django check against the hosted environment.
6. Review the migration plan.
7. Apply migrations only after the plan has been reviewed.

Suggested command sequence from the activated cPanel Python environment:

```bash
python manage.py check
python manage.py check --deploy
python manage.py makemigrations --check
python manage.py migrate --plan
python manage.py migrate
```

The `migrate` command modifies the hosted database. Run it only after a backup and migration-plan review.

If the imported database predates the local data corrections and team participation backfill, review the relevant management commands and records before changing production data. Do not assume that local database-only corrections are included in Git.

## Django static files

The repository defines a Django `STATIC_ROOT`, but `collectstatic` does not itself make the files publicly available. The web server must serve the collected directory.

After confirming the HOSTAFRICA static-file strategy, run:

```bash
python manage.py collectstatic --noinput
```

Possible strategies include:

1. Configure Apache or LiteSpeed to serve the collected `staticfiles` directory.
2. Configure a dedicated public directory for the API subdomain.
3. Add WhiteNoise to Django in a separately reviewed change.

WhiteNoise would be a new application dependency and must not be installed without first updating and reviewing the dependency manifest and Django configuration.

Reference: [Django — Deploying static files](https://docs.djangoproject.com/en/5.2/howto/static-files/deployment/)

## Build the Vue frontend

The Vue source and `node_modules` should not be uploaded to `public_html`. Build locally and upload only the contents of `frontend/dist`.

Set the production build-time values without committing a production `.env` file:

```text
VITE_API_BASE_URL=https://api.yourdomain.com/api
VITE_ADSENSE_CLIENT_ID=ca-pub-3505579912898804
VITE_ADSENSE_HOME_SLOT=1212648508
VITE_ADSENSE_LEAGUE_SLOT=<league-slot-id>
VITE_ADSENSE_TEAM_SLOT=<team-slot-id>
VITE_ADSENSE_FOOTER_SLOT=<footer-slot-id>
```

Build from the frontend directory using only scripts that exist in `package.json`:

```powershell
cd D:\hockeyke\frontend
npm ci
npm run build
```

The production build should not be uploaded if the configured build command fails. Resolve build and type-check failures first.

## Upload the Vue frontend

Upload the contents of `frontend/dist`, not the enclosing `dist` folder:

```text
frontend/dist/index.html  -> public_html/index.html
frontend/dist/assets/     -> public_html/assets/
frontend/dist/.htaccess   -> public_html/.htaccess
```

The resulting server layout must have:

```text
public_html/index.html
```

not:

```text
public_html/dist/index.html
```

Ensure the file manager or upload tool includes hidden files so that `.htaccess` is uploaded. The existing frontend `.htaccess` provides the fallback needed when visitors refresh Vue routes such as team and league pages.

Reference: [HOSTAFRICA — Correct public_html layout](https://help.hostafrica.com/article/why-do-i-get-an-index-of-when-i-visit-my-site)

## Validation before launch

### Backend

Run in the activated hosted Python environment:

```bash
python manage.py check
python manage.py check --deploy
python manage.py makemigrations --check
python manage.py test
```

Confirm:

- The Python application starts without exposing a traceback.
- `/api/` endpoints return the expected JSON.
- Django admin loads with CSS and JavaScript.
- Database queries use the intended hosted MySQL database.
- `DEBUG` is disabled.
- HTTP redirects to HTTPS.
- Invalid hosts are rejected.
- CORS permits only the intended frontend domains.

### Frontend

Test:

- Home page
- League pages and every tab
- Fixtures and results
- Standings, including teams with zero matches
- Team profiles
- Match details
- Search
- Error/404 page
- Direct route refreshes
- Mobile navigation and sticky tabs
- AdSense slots
- API error and empty states

Use browser developer tools to confirm that API requests go to:

```text
https://api.yourdomain.com/api/
```

and never to `127.0.0.1`, `localhost`, or the old host.

## Recommended migration order

1. Confirm the domain and create the API subdomain.
2. Enable SSL.
3. Create the MySQL database and restricted user.
4. Review the pinned Python dependency manifest locally.
5. Confirm the Django static-file serving strategy.
6. Create the cPanel Python application outside `public_html`.
7. Configure production environment variables.
8. Upload the backend and install pinned dependencies.
9. Back up and import the database.
10. Run checks and review the migration plan.
11. Apply reviewed migrations.
12. Collect and verify Django static files.
13. Build Vue with the production API address.
14. Upload the compiled Vue files into `public_html`.
15. Run the complete backend and frontend validation checklist.
16. Change final DNS or declare the installation live only after validation passes.

## Rollback preparation

Before launch, retain:

- A backup of the old production database.
- A backup of the new database before migrations.
- The previous working frontend build.
- The previous working backend release.
- The previous DNS values and TTL information.

If launch validation fails:

1. Put the site into a controlled maintenance state if necessary.
2. Restore the previous frontend build.
3. Restore the previous backend release.
4. Restore the database only when required and only from a verified backup.
5. Revert DNS if the migration cannot be completed safely.

Never use a Git rollback as a substitute for a database rollback plan.

## Information needed at deployment time

Have these values available privately, not in Git:

- Final domain name
- cPanel username
- API subdomain
- Python versions offered by the account
- MySQL database name
- MySQL user name
- MySQL host and port
- Production Django secret key
- AdSense league, team, and footer slot IDs
- Source database backup location
- HOSTAFRICA static-file or document-root configuration
