Environment variables (production)
=================================

This project loads sensitive configuration from environment variables using `python-decouple`.
Do NOT commit a `.env` file to version control for production deployments — use your platform's secret management.

Required variables (recommended):

- `SECRET_KEY` — Django secret key.
- `DEBUG` — `True` or `False` (cast to boolean). In production set `False`.
- `ALLOWED_HOSTS` — comma-separated list of hosts (e.g. `example.com,api.example.com`).
- `DB_ENGINE` — set to `postgres` to use Postgres, otherwise SQLite is used.

Postgres-specific variables (when `DB_ENGINE=postgres`):

- `POSTGRES_DB` — database name.
- `POSTGRES_USER` — database user.
- `POSTGRES_PASSWORD` — database password.
- `POSTGRES_HOST` — database host (default `localhost`).
- `POSTGRES_PORT` — database port (default `5432`).

Optional variables:

- `CORS_ALLOWED_ORIGINS` — configure via settings or platform.

Usage notes:

- For local development you can create a `.env` file with the variables above, but keep it out of VCS.
- In CI/CD or production, inject variables via your deployment platform (Heroku config vars, Docker secrets, Kubernetes Secrets, etc.).
