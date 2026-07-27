# HockeyKE Agent Instructions

## Project purpose

HockeyKE is a fixtures, results, standings and statistics platform for Kenyan field hockey competitions.

The system must support current and historical seasons without damaging historical results or creating duplicate competition data.

## Technology stack

Backend:

* Python 3.11
* Django 5.2
* Django REST Framework
* MySQL in production
* A local development database may be used for development

Frontend:

* Vue 3
* Vue Router
* Vite
* TailAdmin-based interface
* Dark mode

Before making changes, inspect the actual dependency files and existing implementation. Do not assume that every package or version listed here is configured exactly as described.

## Repository-first rule

The repository is the source of truth.

Before implementing any task:

1. Inspect the relevant files.
2. Search for existing implementations and references.
3. Identify backend and frontend dependencies.
4. Explain the intended change.
5. Identify data, migration, API and compatibility risks.
6. Make the smallest coherent change that solves the task.

Do not redesign the application based only on this file when the repository already contains a valid implementation.

## Core data model

The principal entities are:

* Season
* League
* LeagueSeason
* Team
* Match

Expected relationships:

* LeagueSeason connects a League to a Season.
* Match belongs to a LeagueSeason.
* Match references a home team and away team.
* Standings are calculated from Match records.
* Teams should not be assigned directly to seasons merely to make standings work.
* Historical participation should be determined from the established competition and match data.

Inspect all current models and migrations before changing these relationships.

## Supported competitions

Men:

* Premier League Men — PLM
* Super League Men — SLM
* National League Men — NLM
* Supported National League zones

Women:

* Premier League Women — PLW
* Super League Women — SLW

Historical mappings may include:

* Pool A to Eastern Zone
* Pool B to Western Zone

Do not alter historical mappings without explaining how existing records will be affected.

## Known historical team aliases

Imports may contain older team names, including:

* Butali Warriors → Warriors
* Telkom → Blazers
* UON Cubs → University of Nairobi
* Kenyatta University Men → Kenyatta University
* Strathmore University Men → Strathmore University
* Technical University Men → Technical University
* Mombasa Sports Club Men → Mombasa Sports Club
* KCAU → KCA University

Inspect the existing database, import commands and alias mappings before adding new names.

Never silently create a new team when a probable historical alias exists. Record and report unresolved names.

## Match statuses

Expected statuses include:

* SCHEDULED
* LIVE
* FT
* POSTPONED
* CANCELLED

Only valid completed matches should contribute to completed-match standings and statistics.

## Standings requirements

Standings are calculated rather than stored as duplicated permanent records.

The table must support:

* Played
* Won
* Drawn
* Lost
* Goals for
* Goals against
* Goal difference
* Points

Expected ordering:

1. Points
2. Goal difference
3. Goals scored
4. Team name

A competition table must display applicable teams with zero values when no matches have been completed.

Before changing participation logic, inspect how current fixtures and historical matches identify teams belonging to a LeagueSeason.

## Known API patterns

Existing API patterns may include:

* `/api/stats/standings/?league=<slug>&season=<year>`
* `/api/matches/fixtures/?league=<slug>&season=<year>`
* `/api/matches/results/?league=<slug>&season=<year>`
* `/api/matches/<id>/`
* `/api/matches/<id>/form/`
* `/api/matches/<id>/league-table/`
* `/api/matches/<id>/head-to-head/`
* `/api/matches/<id>/stats/`

Inspect the actual URL configuration before relying on these paths.

Do not change an API response structure without:

1. Finding every frontend consumer.
2. Identifying compatibility effects.
3. Updating affected consumers in the same task.
4. Adding or updating tests.

## Frontend expectations

League sections may contain:

* League Table
* Fixtures
* Results
* Stats

Expected behaviour includes:

* Month navigation for fixtures and results
* Team names linking to team profiles
* Responsive tables
* Accessible keyboard navigation
* Home and away team highlighting in match-specific tables
* Scheduled matches displaying date, time and venue
* Completed matches displaying final scores
* Clear postponed and cancelled states
* Recent form
* Head-to-head summaries
* Previous meetings
* Loading, empty and error states
* Dark-mode compatibility

Preserve existing TailAdmin conventions and reusable components unless a replacement is clearly justified.

## Backend development rules

* Keep API views thin.
* Put reusable business logic in services or appropriate domain modules.
* Validate query parameters.
* Return consistent API errors.
* Avoid N+1 queries.
* Use `select_related` and `prefetch_related` where appropriate.
* Preserve historical results.
* Do not duplicate standings or statistics logic.
* Do not use migrations to insert placeholder production data.
* Do not change unrelated files.
* Do not expose secrets or internal error details.

## Frontend development rules

* Follow existing Vue component and routing conventions.
* Reuse established components before creating duplicates.
* Preserve responsive behaviour.
* Preserve dark mode.
* Provide loading, empty and error states.
* Keep links and clickable rows keyboard accessible.
* Do not place interactive links or buttons inside invalid nested interactive elements.
* Do not silently change API expectations.
* Avoid broad visual redesigns during functional fixes.

## Database safety

Never:

* Connect to the production database without explicit approval.
* Delete production data.
* Run `flush` against any database that may contain real data.
* Reset or rewrite migration history.
* alter historical results merely to make tests pass;
* apply destructive migrations without review;
* expose database credentials.

Before a potentially destructive operation, stop and report:

1. The exact command.
2. The records or schema it may affect.
3. The backup requirement.
4. The rollback method.
5. A safer alternative, when available.

## Migration procedure

When a model change is necessary:

1. Explain why the model must change.
2. Describe the effect on existing data.
3. Create the migration.
4. Display and review the migration contents.
5. Run migration checks and tests.
6. Do not apply it to production.
7. Explain rollback considerations.

Do not run `makemigrations` without `--check` unless the task intentionally changes models.

## Dependency policy

Do not install dependencies merely for convenience.

Before adding a package:

1. Explain why current dependencies or standard functionality are insufficient.
2. Check compatibility with the current project.
3. Identify security and maintenance implications.
4. Update the correct dependency file.
5. State any deployment implications.

Request approval before installing it.

## Security requirements

* Keep secrets in environment variables.
* Never commit `.env` files.
* Validate untrusted input.
* Apply appropriate Django and DRF permissions.
* Do not weaken CSRF, CORS, authentication or authorisation controls to bypass an error.
* Do not expose production exception details.
* Treat uploaded files as untrusted.
* Parameterise any necessary raw SQL.
* Apply least-privilege access.

## Git rules

* Work on the `development` branch or a dedicated feature branch.
* Do not work directly on `main`.
* Check `git status` before editing.
* Do not discard existing user changes.
* Keep each task focused.
* Review the final diff.
* Do not push, merge, rebase, reset or force-push without explicit approval.
* Do not commit unless explicitly instructed.
* Never include credentials, environment files, database dumps or private keys.

## Required backend validation

Inspect the project structure and run commands from the correct directory.

Where configured and applicable, run:

```bash
python manage.py check
python manage.py makemigrations --check
python manage.py test
```

Use the existing pytest command instead when the project is already configured for pytest.

Do not claim that a command passed unless it was executed successfully.

## Required frontend validation

Inspect `package.json` and use only scripts that actually exist.

Where configured and applicable, run:

```bash
npm run lint
npm run test
npm run build
```

Do not invent scripts that are not defined in `package.json`.

## Completion standard

A change is not complete only because the page renders.

A completed task requires:

* Relevant Django checks pass.
* Relevant tests pass.
* The frontend build passes when frontend code is affected.
* API and frontend contracts match.
* No unrelated files changed.
* Historical data remains protected.
* Any migration is reviewed.
* Remaining limitations are disclosed.

## Required response structure

For substantive tasks, report:

### Understanding

Restate the requested behaviour and constraints.

### Inspection

List the important files and current implementation found.

### Plan

Describe the smallest coherent implementation.

### Changes

List changed files and behavioural changes.

### Validation

List every command executed and whether it passed or failed.

### Risks and follow-up

Identify remaining limitations, data concerns or recommended subsequent work.

Never claim that a feature is complete when required validation is failing or was not performed.
