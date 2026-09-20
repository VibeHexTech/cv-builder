# CV Builder Project Instructions

## Project Overview

This is a Flask CV Builder application backed by PostgreSQL. It supports DOCX import, manual table copy, individual entry creation, soft deletion, recovery, and locked entries.

## Architecture

- `app.py` is the application entry point and factory.
- `cv_builder/config.py` contains configuration.
- `cv_builder/extensions.py` owns Flask extensions.
- `cv_builder/models.py` contains SQLAlchemy models.
- `cv_builder/services/` contains business logic and DOCX parsing.
- `cv_builder/*_routes.py` contains web, REST, and DOCX route adapters.
- `templates/` contains page templates; `static/` contains shared styles.
- `tests/` contains unittest coverage.

## Engineering Principles

Follow SOLID principles:

- Keep route handlers thin and move business rules into services.
- Give each module one clear responsibility.
- Depend on injected abstractions or collaborators where practical.
- Preserve existing public URLs and API contracts unless a change is explicitly requested.
- Keep database access out of templates and avoid duplicating business rules in frontend code.
- Prefer small, focused changes over broad rewrites.

## Testing

Use Python's standard `unittest` framework. Run the complete suite with:

```bash
.venv/bin/python -m unittest discover -s tests -v
```

Every behavioral change should add or update a focused unittest. Tests must use an isolated test database and must not modify development data. At minimum, preserve coverage for:

- application pages and health endpoint
- entry CRUD behavior
- lock protection
- soft deletion and recovery
- DOCX parsing and requested `Title | Rolle | Opgave | Resultat` order

## Database Rules

- Use migrations or the existing database initializer when adding columns.
- Locked entries must not be deletable.
- Deletion is soft deletion; recoverable rows belong on the deleted-entries page.
- Do not permanently delete user data without an explicit requirement.

## Validation

After changes, run the unittest suite and check the affected routes. Do not commit generated files, test databases, or temporary validation data.
