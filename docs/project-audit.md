# HockeyKE Project Audit

Audit date: 27 July 2026  
Audit scope: read-only inspection of the Django backend and Vue frontend  
Repository branch at audit time: `development`

## Evidence labels

- **Verified** — confirmed directly from repository files or a command that completed successfully.
- **Inferred** — concluded from the implementation, but not confirmed by successfully running the complete application.
- **Not yet verified** — execution or runtime confirmation was blocked or was outside the read-only audit.

## Confirmed repository structure

- **Verified** — The repository root contains `AGENTS.md`, `backend/`, and `frontend/`.
- **Verified** — The root branch is `development`, tracking `origin/development`.
- **Verified** — Before the audit, root Git status already reported `m frontend`. This was treated as a pre-existing change.
- **Verified** — `frontend/` contains its own `.git` directory, but the root repository has no matching `.gitmodules` entry.
- **Verified** — Nested frontend Git inspection was blocked by Git's dubious-ownership protection. No global Git configuration was changed.

```text
D:\hockeyke
├── AGENTS.md
├── backend
│   ├── manage.py
│   ├── config
│   ├── core
│   ├── competitions
│   ├── teams
│   ├── matches
│   ├── players
│   ├── stats
│   ├── templates/admin
│   ├── imports
│   ├── db.sqlite3
│   └── venv
└── frontend
    ├── package.json
    ├── package-lock.json
    ├── vite.config.ts
    ├── eslint.config.ts
    ├── src
    │   ├── router
    │   ├── services
    │   ├── views
    │   ├── components
    │   ├── composables
    │   └── assets
    ├── public
    ├── node_modules
    └── .env
```

- **Verified** — The Django project is rooted at `backend/manage.py`; its settings and root URLs are under `backend/config/`.
- **Verified** — The Vue 3 application is rooted at `frontend/` and uses Vite, Vue Router, Tailwind CSS, and TailAdmin-derived components.
- **Verified** — `backend/db.sqlite3` exists and is ignored by Git.
- **Verified** — Current Django settings use MySQL, not the SQLite file.
- **Verified** — No backend dependency manifest such as `requirements.txt`, `pyproject.toml`, Pipfile, or Poetry file exists.

### Startup commands

- **Inferred** — Backend development startup is intended to be `python manage.py runserver` from `backend/`, or `backend\venv\Scripts\python.exe manage.py runserver` when the virtual environment is valid.
- **Verified** — The configured frontend development command is `npm run dev`.
- **Verified** — The configured frontend preview command is `npm run preview`.
- **Verified** — The configured frontend production build command is `npm run build`.
- **Verified** — No production Django server, container, process manager, or deployment command is configured in the repository.
- **Not yet verified** — Backend startup could not be executed because no usable Python interpreter was available.

### Dependencies

- **Verified** — Python package metadata in `backend/venv` reports:
  - Django 5.2.15
  - Django REST Framework 3.17.1
  - django-cors-headers 4.9.0
  - django-jazzmin 3.0.4
  - mysqlclient 2.2.8
  - psycopg2-binary 2.9.12
  - Pillow 12.2.0
  - openpyxl 3.1.5
  - python-dotenv 1.2.2
  - asgiref 3.11.1
  - sqlparse 0.5.5
  - tzdata 2026.2
  - et-xmlfile 2.0.0
- **Verified** — Direct frontend dependencies include Vue 3.5, Vue Router 4.5, Axios, ApexCharts, FullCalendar, Tailwind CSS 4, Dropzone, Flatpickr, Swiper, JSVectorMap, and their Vue adapters.
- **Verified** — Frontend development dependencies include Vite 6, TypeScript 5.7, vue-tsc, ESLint 9, Vue ESLint configurations, Prettier, Sass, and npm-run-all2.
- **Verified** — Node.js 22.18.0 is available.
- **Verified** — The existing backend virtual environment points to a missing user-specific Python 3.11.9 installation.

## Confirmed architecture

### Django applications

- **Verified** — `core` is an empty placeholder application.
- **Verified** — `competitions` owns seasons, leagues, league seasons, and related admin screens.
- **Verified** — `teams` owns teams, gender-specific proxy models, competition memberships, team profile APIs, and team CSV import.
- **Verified** — `matches` owns fixtures/results, match events, competition-specific admin proxies, match APIs, and legacy/Excel match imports.
- **Verified** — `stats` calculates standings and aggregate team statistics in Python and exposes public and admin views.
- **Verified** — `players` is an empty placeholder application.

### Models and relationships

- **Verified** — `Season` has a unique name, optional start/end dates, and an `is_current` flag.
- **Verified** — `League` has a name, short name, gender, and zone, with uniqueness on `(name, gender, zone)`.
- **Verified** — `LeagueSeason` links one `League` to one `Season`, with uniqueness on `(league, season)` and protected foreign keys.
- **Verified** — `Team` has name, short name, nullable gender, optional logo, and active status.
- **Verified** — `MenTeam` and `WomenTeam` are proxy models used for gender-filtered administration.
- **Verified** — `TeamLeagueSeason` links teams to league seasons and is unique on `(team, league_season)`.
- **Verified** — `Match` belongs to a `LeagueSeason` and references home and away teams with protected foreign keys.
- **Verified** — Match statuses are `SCHEDULED`, `LIVE`, `FT`, `POSTPONED`, and `CANCELLED`.
- **Verified** — `MatchEvent` stores match, team, event type, minute, goal type, free-text player name, and notes.
- **Verified** — `Standings` is an unmanaged, fieldless model used to expose calculated standings in Django admin.

### Standings and statistics

- **Verified** — `stats/services.py` is the central standings implementation.
- **Verified** — It seeds participants from all teams appearing in fixtures for one `LeagueSeason`.
- **Verified** — Only matches with `status="FT"` affect standings totals.
- **Verified** — It calculates played, won, drawn, lost, goals for, goals against, goal difference, points, and recent form.
- **Verified** — Ordering is points, goal difference, goals scored, then team name.
- **Verified** — Form is limited to five results.
- **Verified** — Aggregate team statistics calculate goals scored/conceded, clean sheets, and longest winning/losing streaks.
- **Verified** — `TeamLeagueSeason` memberships are not used by standings calculations.

### League, season, gender, zone, fixtures, and results filtering

- **Verified** — League selection uses duplicated hard-coded `LEAGUE_MAPPING` dictionaries in `matches/views.py` and `stats/views.py`.
- **Verified** — Supported public mappings cover PLM, PLW, SLM, SLW, and four men's National League zones.
- **Verified** — The requested season is matched against `Season.name`.
- **Verified** — The match list endpoint accepts league, season, year, and month.
- **Verified** — Without an explicit month, it selects the next future scheduled-fixture month, then falls back to the latest completed-match month.
- **Verified** — The monthly response contains all match statuses, mixing fixtures and results.
- **Verified** — No separate results endpoint is implemented.
- **Verified** — The frontend defaults league pages to season `2026` when no season query parameter is present.

### Team profiles

- **Verified** — Team profile APIs provide overview, matches, team stats, and league table endpoints.
- **Verified** — The active league season is inferred from the highest season name among the team's matches.
- **Verified** — Team profile selection does not use `Season.is_current`, `TeamLeagueSeason`, or explicit league/season query parameters.
- **Verified** — Overview data includes position, recent form, previous match, next match, and a nearby table snapshot.
- **Inferred** — Lexicographical season selection can choose an unintended competition when season naming formats differ or a team plays in multiple competitions.

### Match detail, form, head-to-head, and team comparison

- **Verified** — Match detail returns a manually serialized match object.
- **Verified** — Recent form returns the last five FT matches in the same league season for each selected team.
- **Verified** — Match league table calls the shared standings service and returns home/away highlight IDs.
- **Verified** — Head-to-head returns up to ten previous FT meetings across all league seasons and competitions.
- **Verified** — Head-to-head summary includes wins, draws, goals, and clean sheets.
- **Verified** — Match team statistics separately recalculate W/D/L, goals, goal difference, and points.
- **Verified** — `MatchSerializer` exists but is not used by the implemented endpoints.

### API endpoints and Vue consumers

| Status | Endpoint | Main response | Vue consumer |
|---|---|---|---|
| **Verified** | `GET /api/matches/?league=&season=&year=&month=` | `{year, month, matches[]}` | `LeagueFixturesTab.vue` |
| **Verified** | `GET /api/matches/<id>/` | Match object | `MatchDetailView.vue` |
| **Verified** | `GET /api/matches/<id>/form/` | Home/away teams with recent matches | `MatchFormTab.vue` |
| **Verified** | `GET /api/matches/<id>/league-table/` | Highlight IDs and standings | `MatchLeagueTableTab.vue` |
| **Verified** | `GET /api/matches/<id>/head-to-head/` | Summary and previous matches | `MatchHeadToHeadTab.vue` |
| **Verified** | `GET /api/matches/<id>/team-stats/` | Home/away aggregate statistics | `MatchStatsTab.vue` |
| **Verified** | `GET /api/stats/standings/?league=&season=` | League metadata and standings | `LeagueTableTab.vue` |
| **Verified** | `GET /api/stats/teams/?league=&season=` | Per-team statistics | No frontend consumer found |
| **Verified** | `GET /api/stats/season/?league=&season=` | Ranked statistic categories | `LeagueStatsTab.vue` |
| **Verified** | `GET /api/teams/<id>/overview/` | Profile overview | `TeamProfile.vue` |
| **Verified** | `GET /api/teams/<id>/matches/` | Team matches | `TeamFixturesTab.vue` |
| **Verified** | `GET /api/teams/<id>/stats/` | Team aggregate statistics | `TeamStatsTab.vue` |
| **Verified** | `GET /api/teams/<id>/table/` | Inferred competition table | `TeamTableTab.vue` |

### Vue routes, pages, tabs, and reusable components

- **Verified** — Hockey routes are:
  - `/league/:gender/:competition/:division?`
  - `/fixtures`
  - `/match/:id/:slug`
  - `/teams/:teamId/:teamSlug/:tab?`
- **Verified** — League tabs are League Table, Fixtures, and Team Stats.
- **Verified** — Match tabs are Form, League Table, H2H, and Stats.
- **Verified** — Team tabs are Overview, Table, Fixtures, and Stats.
- **Verified** — Hockey components are grouped under `components/league`, `components/match`, and `components/teams`.
- **Verified** — TailAdmin layout, theme, sidebar, common UI, chart, ecommerce, form, profile, and demonstration pages remain in the application.
- **Verified** — The router still exposes TailAdmin demonstration routes.

### Imports and historical aliases

- **Verified** — Import data includes 570 National Men rows, 642 Premier Men rows, 328 Premier Women rows, 482 Super League Men rows, 230 Super League Women rows, two team CSV files, and one 2026 KHU Excel calendar.
- **Verified** — `import_teams` creates or updates teams by name.
- **Verified** — `import_legacy_matches` uses static alias and zone maps, does not create missing teams, supports `--dry-run`, and reports row errors.
- **Verified** — `import_khu_fixtures` performs exact case-insensitive name/short-name resolution within league gender and wraps writes in a transaction.
- **Verified** — The legacy alias map includes several documented aliases but omits `Telkom → Blazers` and `UON Cubs → University of Nairobi`.
- **Verified** — The legacy map converts `University of Nairobi` to `UON`, conflicting with the canonical direction documented in `AGENTS.md`.
- **Verified** — Pool A and Pool B currently remain literal pool names rather than mapping to Eastern and Western Zone.

### Migrations

- **Verified** — Migration counts are: competitions 2, teams 4, matches 7, and stats 3.
- **Verified** — `core` and `players` have no schema migrations beyond `__init__.py`.
- **Verified** — Teams migration `0004` removes global uniqueness from `Team.name` without adding a replacement constraint.
- **Verified** — Match migrations add nullable match dates and league-specific proxy models but no fixture identity constraints.
- **Verified** — Stats migrations create stored standings, alter them, then delete that stored model in migration `0003`.
- **Not yet verified** — Migration graph consistency and model/migration drift could not be checked with Django because Python was unavailable.

## Working features

- **Verified** — The core historical relationship `Season → LeagueSeason → League`, with matches belonging to league seasons, is implemented.
- **Verified** — Standings are calculated rather than stored permanently.
- **Verified** — Only FT matches count in standings and aggregate statistics.
- **Verified** — Required standings columns and tie-break ordering are implemented.
- **Verified** — League table team names link to team profiles.
- **Verified** — League month navigation is implemented.
- **Verified** — Fixture cards contain branches for scheduled, FT, postponed, and cancelled states.
- **Verified** — Scheduled fixture cards display date/time and venue when available.
- **Verified** — Dark-mode styling is present across HockeyKE pages.
- **Verified** — Match-specific league tables highlight home and away teams.
- **Verified** — Recent form, head-to-head summaries, and previous meetings are implemented.
- **Verified** — Team overview, table, fixtures, and statistics tabs are implemented.
- **Verified** — Match importers do not silently create unresolved teams.
- **Verified** — The legacy importer supports read-only dry runs and unresolved-row reporting.
- **Verified** — The KHU importer uses a database transaction.
- **Verified** — Several list queries use `select_related`.
- **Not yet verified** — End-to-end backend behaviour, response status codes, database compatibility, and rendered frontend behaviour were not runtime-tested.

## Known problems

### Critical

- **Verified** — `config/settings.py` contains a hard-coded Django secret, `DEBUG=True`, fixed local MySQL credentials, empty `ALLOWED_HOSTS`, and no environment-specific settings.
  - Impact: unsafe production defaults, possible exception disclosure, secret exposure, and non-portable deployment.
  - Recommended correction: introduce environment-based development/production settings and fail closed for required production values.

### High

- **Verified** — There is no reproducible backend dependency manifest, and the checked-in/local virtual environment is non-portable.
  - Impact: the backend cannot be reliably installed, checked, tested, or deployed.
  - Recommended correction: add a reviewed Python dependency manifest and recreate the environment outside version control.

- **Verified** — The KHU importer uses `update_or_create(match_number=...)` without league-season scope.
  - Impact: importing a new season or competition can overwrite an unrelated historical fixture.
  - Recommended correction: scope identity to league season plus match number and report collisions.

- **Verified** — `Match` has no constraints preventing duplicate fixtures or home team equalling away team.
  - **Inferred** — Team/league gender mismatches and duplicate records can corrupt standings.
  - Recommended correction: audit existing data, add service validation, then introduce reviewed constraints.

- **Verified** — Team profile competition selection is based on lexicographically latest season name among matches.
  - Impact: profiles can select the wrong competition or omit registered teams without matches.
  - Recommended correction: support explicit season/league context with a deliberate current-season fallback.

- **Verified** — `MatchDetailView.vue` treats any non-null scores as completed, while model scores always default to zero.
  - Impact: scheduled, postponed, or cancelled fixtures can display as `0–0 Full Time`.
  - Recommended correction: render completion from `status === "FT"` and handle every status explicitly.

- **Verified** — Backend test files contain only generated placeholders, and there is no frontend test script.
  - Impact: core data and API behaviour have no regression protection.
  - Recommended correction: add service, API, import, and targeted component tests.

- **Verified** — Alias handling omits documented aliases and contains a conflicting UON canonical direction.
  - Impact: historical imports can fail or resolve to unintended team identities.
  - Recommended correction: define and test one canonical, context-aware alias policy.

- **Verified** — Standings seed teams only from matches and ignore `TeamLeagueSeason`.
  - Impact: registered teams with no fixtures are absent instead of appearing with zero values.
  - Recommended correction: define participation precedence and seed eligible membership teams safely.

### Medium

- **Verified** — Pool A/B history is not mapped to the documented Eastern/Western zones.
  - Recommended correction: audit existing league and match data before any reconciliation.

- **Verified** — No separate Results endpoint or league Results tab exists.
  - Recommended correction: add shared validated monthly filtering with separate fixture/result modes.

- **Verified** — Raw integer parsing, unhandled `.get()` calls, and unconditional date formatting can produce server errors for invalid parameters, missing IDs, or null dates.
  - Recommended correction: add DRF query validation, consistent 404 handling, and null-safe serialization.

- **Verified** — API response construction is duplicated across manual serializers, while `MatchSerializer` is unused.
  - Recommended correction: centralize serializers and protect contracts with tests.

- **Verified** — Match detail UI expects league/season fields that the active response does not return.
  - Impact: the page can display a generic heading and blank season.

- **Verified** — Match team statistics and recent-form logic duplicate calculations from the stats domain.
  - Recommended correction: move reusable calculations into domain services.

- **Verified** — `Team.name` uniqueness was removed without a replacement identity constraint, while team import updates by name alone.
  - Impact: duplicate or wrong-gender team resolution is possible.

- **Verified** — Stats migration `0003` deletes the previous stored standings model.
  - Impact: applying it to a legacy database with meaningful stored rows is destructive without reconciliation.

- **Verified** — Frontend non-mutating lint reports 103 errors, and type checking reports two ApexCharts typing errors.
  - Recommended correction: align ESLint with the intended JavaScript/TypeScript policy and fix genuine type errors.

- **Verified** — No production static/media, HTTPS, cookie, deployment, or process configuration exists.

### Low

- **Verified** — API views contain leftover `print()` debugging statements.
- **Verified** — Django `SecurityMiddleware` is listed twice.
- **Verified** — Team route `:tab` is declared but ignored.
- **Verified** — `/fixtures` displays unrelated TailAdmin profile/settings/billing placeholder content.
- **Verified** — Some HockeyKE components lack explicit error states.
- **Verified** — Tab controls do not implement complete ARIA tab semantics.
- **Verified** — TailAdmin demonstration pages and ecommerce home content remain exposed.

## Validation results

- **Verified** — `git status --short --branch` completed successfully and showed the pre-existing `m frontend`.
- **Verified** — `git branch --show-current` completed successfully and returned `development`.
- **Verified** — `python --version` failed because `python` is not installed or available on `PATH`.
- **Verified** — `py -0p` reported that no Python installations are registered.
- **Verified** — `backend\venv\Scripts\python.exe --version` failed because its configured Python executable is missing.
- **Not yet verified** — `python manage.py check` could not run.
- **Not yet verified** — `python manage.py makemigrations --check` could not run.
- **Not yet verified** — `python manage.py test` could not run.
- **Verified** — The configured frontend lint script is `eslint . --fix`, which was not used because it would modify files.
- **Verified** — Non-mutating `npm exec eslint -- .` exited with code 1 and reported 103 pre-existing errors.
- **Verified** — Non-emitting `npm exec vue-tsc -- --noEmit -p tsconfig.app.json` exited with code 1 and reported two pre-existing ApexCharts option typing errors.
- **Verified** — No frontend test script exists, so no frontend tests were run.
- **Not yet verified** — `npm run build` was not run because it creates or replaces `dist`, conflicting with the read-only audit.
- **Verified** — No application, dependency, migration, configuration, database, commit, or remote changes were made during the audit.

## Missing functionality

- **Verified** — Separate results browsing and a Results tab are missing.
- **Verified** — Membership-only teams do not appear in zero-value standings.
- **Verified** — Team profiles cannot explicitly select historical league seasons.
- **Verified** — No public season or league discovery endpoint exists.
- **Verified** — Match status display is incomplete or incorrect on the detail page.
- **Verified** — The standalone fixtures page is placeholder content.
- **Verified** — `players` has no implemented domain functionality.
- **Verified** — Match events have no public API or frontend.
- **Verified** — Card counts in standings responses are always zero because standings do not aggregate events.
- **Verified** — Loading, empty, and error states are inconsistent across components.
- **Verified** — API parameter validation and error envelopes are inconsistent.
- **Verified** — Production deployment configuration and project-specific setup documentation are missing.
- **Verified** — Required backend/frontend validation does not currently pass or cannot run.
- **Verified** — There is no substantive automated test coverage.
- **Inferred** — Historical Pool A/B competitions may be inaccessible through current public league slugs if imported as literal pool zones.
- **Not yet verified** — Existing database duplicate teams, duplicate match numbers, duplicate fixtures, and historical pool records were not queried because backend database execution was unavailable.

## Recommended implementation phases

### Phase 1 — Reproducible and safe development baseline

- **Inferred** — Add a reviewed Python dependency manifest and project-specific setup documentation.
- **Inferred** — Separate development and production settings and move secrets/database details to environment variables.
- **Inferred** — Restore executable Django checks.
- **Inferred** — Add non-mutating frontend validation scripts.
- **Not yet verified** — Completion should be demonstrated with a fresh environment, Django checks, and frontend lint/type checks.

### Phase 2 — Characterization tests

- **Inferred** — Add tests for seasons, leagues, memberships, matches, standings, imports, and API contracts before changing behaviour.
- **Inferred** — Add query-count tests for high-traffic endpoints.
- **Not yet verified** — Expected coverage targets and CI platform still need project decisions.

### Phase 3 — Data integrity and importer safety

- **Inferred** — Audit duplicate teams, match numbers, and fixtures.
- **Inferred** — Fix canonical aliases and import collision handling.
- **Inferred** — Scope KHU fixture identity to a league season.
- **Inferred** — Add constraints only after existing data is reconciled.

### Phase 4 — Centralize competition resolution and statistics

- **Inferred** — Replace duplicated league mappings with one tested resolver.
- **Inferred** — Centralize match serialization, form, and team-summary calculations.
- **Inferred** — Preserve or deliberately version API contracts and update every consumer together.

### Phase 5 — Participation and historical correctness

- **Inferred** — Define how memberships and match-derived historical participation interact.
- **Inferred** — Include zero-match participants in tables.
- **Inferred** — Add explicit league/season selection to team profiles.
- **Inferred** — Reconcile Pool A/B mappings only after reviewing existing records and rollback requirements.

### Phase 6 — Fixtures, results, and match-status UX

- **Inferred** — Add validated, separate fixtures and results flows.
- **Inferred** — Add a Results tab and repair the global fixtures page.
- **Inferred** — Correct scheduled/live/postponed/cancelled match detail rendering.
- **Inferred** — Add component tests for navigation, statuses, errors, and empty states.

### Phase 7 — Product completion and production readiness

- **Inferred** — Implement player/event statistics if confirmed as product scope.
- **Inferred** — remove or isolate unused TailAdmin demonstration pages.
- **Inferred** — Complete accessibility and error/retry behaviour.
- **Inferred** — Configure static/media hosting, HTTPS security, a production WSGI server, deployment checks, and full regression validation.

## Safest first task

- **Inferred** — Create characterization tests for `stats.services.calculate_standings()` without changing production behaviour.
- **Verified** — This service currently drives league tables, team profile tables, and match-specific league tables.
- **Inferred** — The first test set should cover:
  1. only FT matches contribute;
  2. played/won/drawn/lost and goal totals;
  3. points and tie-break ordering;
  4. form limited to five matches;
  5. scheduled, postponed, and cancelled matches do not contribute;
  6. current behaviour for membership-only teams is documented as a deferred gap.
- **Inferred** — Locking down standings behaviour first provides the highest protection for later participation, importer, and API refactoring work.
- **Not yet verified** — These tests cannot be executed until a working Python environment and dependency manifest are available.
