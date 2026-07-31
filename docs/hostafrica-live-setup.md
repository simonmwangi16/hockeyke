# HockeyKE Live Deployment on HOSTAFRICA

This is the operational setup and upload guide for the HOSTAFRICA account
`hockeyk1`. Read `AGENTS.md` and `docs/hostafrica-migration.md` for the project
rules and migration background.

The files in this repository are deployment-ready inputs, not a live deployment.
Do not commit or upload passwords, secret keys, `.env` files, database dumps, or
the local virtual environment.

## 1. Target layout

Use separate locations for Django and the compiled Vue site:

```text
/home/hockeyk1/
|-- hockeyke_backend/       Django application
|-- public_html/            Compiled Vue frontend
|   |-- index.html
|   |-- assets/
|   `-- .htaccess
`-- deployment_backups/     Private backups; never place under public_html
```

Recommended URLs:

```text
https://YOUR_DOMAIN/             Vue frontend
https://api.YOUR_DOMAIN/api/     Django API
https://api.YOUR_DOMAIN/admin/   Django administration
```

Create `api.YOUR_DOMAIN` before creating the Python application. Enable SSL for
the root domain, `www`, and the API subdomain.

## 2. Create the database

In cPanel, open **MySQL Database Wizard**:

1. Create a database.
2. Create a dedicated database user with a unique password.
3. Grant that user privileges only on the HockeyKE database.
4. Keep the exact cPanel-prefixed database and user names.

Typical values look like:

```text
Database: hockeyk1_hockeyke
User:     hockeyk1_hockeyuser
Host:     localhost
Port:     3306
```

Do not put the real password in Git.

## 3. Create the cPanel Python application

Open **cPanel > Software > Setup Python App > Create Application**.

Enter:

| Field | Value |
| --- | --- |
| Python version | `3.11` |
| Application root | `hockeyke_backend` |
| Application URL | `api.YOUR_DOMAIN` |
| Startup file | `passenger_wsgi.py` |
| Entry point | `application` |

The resulting application root must be:

```text
/home/hockeyk1/hockeyke_backend
```

Do not use `public_html` as the Python application root.

After creating the app, cPanel displays a command for activating its virtual
environment. Copy that exact command; it will resemble:

```bash
source /home/hockeyk1/virtualenv/hockeyke_backend/3.11/bin/activate
```

## 4. Upload the backend

Upload the **contents** of the repository's `backend` directory into:

```text
/home/hockeyk1/hockeyke_backend
```

Required examples:

```text
/home/hockeyk1/hockeyke_backend/manage.py
/home/hockeyk1/hockeyke_backend/requirements.txt
/home/hockeyk1/hockeyke_backend/passenger_wsgi.py
/home/hockeyk1/hockeyke_backend/config/
/home/hockeyk1/hockeyke_backend/competitions/
/home/hockeyk1/hockeyke_backend/core/
/home/hockeyk1/hockeyke_backend/matches/
/home/hockeyk1/hockeyke_backend/players/
/home/hockeyk1/hockeyke_backend/stats/
/home/hockeyk1/hockeyke_backend/teams/
/home/hockeyk1/hockeyke_backend/templates/
```

Exclude:

```text
venv/
__pycache__/
*.pyc
.env
db.sqlite3
imports/
staticfiles/
*.log
```

The `requirements.txt` file contains the verified direct packages used by the
application. Do not upload the Windows virtual environment.

## 5. Install backend dependencies

Open cPanel Terminal and activate the Python app using the command supplied by
cPanel. Then run:

```bash
cd /home/hockeyk1/hockeyke_backend
python -m pip install -r requirements.txt
```

If `mysqlclient` fails to build, stop and send the complete error to HOSTAFRICA
support. Do not replace the database driver or install an unrelated package
without a reviewed code change.

## 6. Add Python application environment variables

In **Setup Python App**, add:

```text
HOCKEYKE_ENV=production
DJANGO_SECRET_KEY=<NEW_RANDOM_SECRET_AT_LEAST_50_CHARACTERS>
DJANGO_ALLOWED_HOSTS=api.YOUR_DOMAIN
DJANGO_DB_NAME=<CPANEL_DATABASE_NAME>
DJANGO_DB_USER=<CPANEL_DATABASE_USER>
DJANGO_DB_PASSWORD=<CPANEL_DATABASE_PASSWORD>
DJANGO_DB_HOST=localhost
DJANGO_DB_PORT=3306
DJANGO_DB_CONN_MAX_AGE=60
DJANGO_STATIC_ROOT=<API_SUBDOMAIN_DOCUMENT_ROOT>/static
DJANGO_MEDIA_ROOT=<API_SUBDOMAIN_DOCUMENT_ROOT>/media
DJANGO_CORS_ALLOWED_ORIGINS=https://YOUR_DOMAIN,https://www.YOUR_DOMAIN
DJANGO_CSRF_TRUSTED_ORIGINS=https://YOUR_DOMAIN,https://www.YOUR_DOMAIN,https://api.YOUR_DOMAIN
DJANGO_SECURE_SSL_REDIRECT=true
DJANGO_SECURE_HSTS_SECONDS=3600
DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS=true
DJANGO_SECURE_HSTS_PRELOAD=false
```

Replace every placeholder. Obtain the API subdomain document root from cPanel or
HOSTAFRICA; do not guess it. HockeyKE production settings intentionally refuse
to start when the secret, allowed hosts, or database values are missing or still
contain placeholder text.

Restart the Python application after changing environment variables.

## 7. Validate Django before importing data

From the activated virtual environment:

```bash
cd /home/hockeyk1/hockeyke_backend
python manage.py check
python manage.py check --deploy
python manage.py makemigrations --check
python manage.py migrate --plan
```

Do not continue if `check` fails. Review warnings from `check --deploy` before
making the site public.

`migrate --plan` is read-only. The next database steps are not.

## 8. Import and migrate the database

1. Make a private backup of the destination database.
2. Import the approved source SQL backup through phpMyAdmin or cPanel Terminal.
3. Confirm that the import went into the intended `hockeyk1_...` database.
4. Run `python manage.py migrate --plan` again.
5. Only after reviewing the plan, run:

```bash
python manage.py migrate
```

Do not place the SQL backup in `public_html` or Git. If the source backup does
not include recent local database-only corrections, those corrections must be
reviewed and repeated separately; source code deployment cannot reproduce them.

## 9. Configure Django static and uploaded media files

Run:

```bash
python manage.py collectstatic --noinput
```

With the recommended environment variables, Django collects assets and stores
uploaded team logos under the API subdomain document root:

```text
<API_SUBDOMAIN_DOCUMENT_ROOT>/static/
<API_SUBDOMAIN_DOCUMENT_ROOT>/media/
```

Confirm that HOSTAFRICA serves these directories as:

```text
https://api.YOUR_DOMAIN/static/ -> <API_SUBDOMAIN_DOCUMENT_ROOT>/static/
https://api.YOUR_DOMAIN/media/  -> <API_SUBDOMAIN_DOCUMENT_ROOT>/media/
```

Do not set either path to the backend source directory and do not make the
entire backend directory public.

Verify that `https://api.YOUR_DOMAIN/admin/` loads with CSS and JavaScript before
continuing.

## 10. Build the frontend on the office PC

Do not build the Vue app on the live server unless the hosting plan explicitly
provides a compatible Node environment. Build locally from a clean checkout of
the `development` branch.

In PowerShell:

```powershell
git switch development
git pull origin development
cd frontend
npm ci

$env:VITE_API_BASE_URL = "https://api.YOUR_DOMAIN/api"
$env:VITE_ADSENSE_CLIENT_ID = "ca-pub-3505579912898804"
$env:VITE_ADSENSE_HOME_SLOT = "1212648508"
$env:VITE_ADSENSE_LEAGUE_SLOT = "<LEAGUE_SLOT_ID>"
$env:VITE_ADSENSE_TEAM_SLOT = "<TEAM_SLOT_ID>"
$env:VITE_ADSENSE_FOOTER_SLOT = "<FOOTER_SLOT_ID>"

npm run build
```

Replace every placeholder. Vite embeds these values during the build; changing
server environment variables after building does not update the compiled site.

Do not upload `frontend/src` or `frontend/node_modules`.

## 11. Upload the frontend

Back up the current `public_html` before replacing it.

Upload the **contents** of `frontend/dist`:

```text
frontend/dist/index.html -> /home/hockeyk1/public_html/index.html
frontend/dist/assets/    -> /home/hockeyk1/public_html/assets/
frontend/dist/.htaccess  -> /home/hockeyk1/public_html/.htaccess
```

The correct result is:

```text
/home/hockeyk1/public_html/index.html
```

It must not be:

```text
/home/hockeyk1/public_html/dist/index.html
```

Enable the cPanel File Manager option to show hidden files so `.htaccess` is
uploaded. That file allows direct visits and refreshes of Vue routes.

## 12. Restart and validate the live site

Restart the Python application in **Setup Python App** and test:

```text
https://api.YOUR_DOMAIN/admin/
https://api.YOUR_DOMAIN/api/stats/standings/?league=<slug>&season=<year>
https://YOUR_DOMAIN/
```

Complete this checklist:

- HTTP redirects to HTTPS.
- Django does not display debug tracebacks.
- Admin CSS and JavaScript load.
- The frontend calls `https://api.YOUR_DOMAIN/api`, not localhost.
- CORS succeeds only for the approved frontend origins.
- Home page content and ads load.
- Search works.
- League tables, fixtures, results, and statistics load.
- Teams with no completed games appear correctly in tables.
- Team pages and direct URL refreshes work.
- Match detail pages work.
- Mobile navigation and sticky tabs work.
- Unknown frontend routes show the HockeyKE 404 page.
- Postponed and cancelled matches are displayed correctly.

Run the hosted backend tests if the hosting limits allow them:

```bash
python manage.py test
```

## 13. Rollback

Before launch, retain:

- The previous `public_html` contents.
- The previous backend application directory or release archive.
- A verified pre-import database backup.
- A verified pre-migration database backup.
- The previous DNS records.

If deployment fails:

1. Restore the previous frontend files.
2. Restore the previous backend release.
3. Restart the Python application.
4. Restore the database only when necessary and from a verified backup.
5. Revert DNS if the new host cannot be made operational safely.

Never assume reverting Git will reverse a database migration or data import.

## 14. Values still required

Before live deployment, provide privately:

- The final domain name.
- Confirmation that `api.YOUR_DOMAIN` exists and has SSL.
- The cPanel-generated virtual environment activation command.
- The API subdomain document root or HOSTAFRICA static mapping.
- MySQL database and user names.
- A new production Django secret key.
- AdSense league, team, and footer slot IDs.
- The approved database backup location and date.
