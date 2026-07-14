# Steins;Gate Fan Platform

A single-title streaming-style web application dedicated to Steins;Gate: watch both seasons and the movie, register an account, manage a profile, rate titles and discuss them in comments.

The project is a portfolio work demonstrating a production-shaped full-stack setup: a typed SPA frontend, a Django API backend with a service layer, and a containerized deployment behind nginx with Redis-backed rate limiting and caching.

## Architecture

```
browser
   |
   v
nginx (frontend container, :4173)
   |-- /            SPA static (React build)
   |-- /assets/     hashed bundles, cached immutable
   |-- /img/        posters and backgrounds (WebP)
   |-- /static/     Django admin static (shared volume)
   |-- /media/      user uploads (shared volume)
   |-- /api/   -----> backend (gunicorn, :8000)
   |-- /admin/ -----> backend (gunicorn, :8000)
                          |            |
                          v            v
                    PostgreSQL 16   Redis 7
                                    (throttling, IP lockout,
                                     aggregate cache)
```

- `frontend/` — React SPA. Pages, routing and UI state. API types are generated from the backend OpenAPI schema, so the contract is compile-checked.
- `backend/` — Django + django-ninja. Domain apps with a service layer; HTTP endpoints are thin wrappers over services.
- `compose.yaml` — four services: `db`, `redis`, `backend`, `frontend`.

## Tech stack

| Layer      | Technology |
|------------|------------|
| Frontend   | React 19, TypeScript (strict), Vite, Tailwind CSS 4, React Router 7, TanStack Query |
| Backend    | Python 3.14, Django 6, django-ninja, gunicorn |
| Storage    | PostgreSQL 16 (SQLite for local development), Redis 7 |
| Infra      | Docker, docker compose, nginx |
| Quality    | ruff, ESLint, GitHub Actions CI, Django test suite |

## API

Interactive documentation: `/api/docs` (OpenAPI schema at `/api/openapi.json`).

| Method     | Path | Auth |
|------------|-------------------------------|---------|
| GET        | `/api/anime`                  | public  |
| GET        | `/api/anime/{slug}`           | public  |
| POST       | `/api/anime/{slug}/rating`    | session |
| GET, POST  | `/api/anime/{slug}/comments`  | POST: session |
| POST       | `/api/comments/{id}/reaction` | session |
| GET, PUT   | `/api/anime/{slug}/progress`  | session |
| POST       | `/api/auth/register`, `/verify-email`, `/login`, `/logout` | — |
| GET        | `/api/auth/session`, `/api/auth/csrf` | public |
| PATCH      | `/api/profile`; POST `/api/profile/avatar` | session |

Frontend types are regenerated with `npm run gen:api` after the schema changes.

## Security

- Session authentication with HttpOnly cookies; CSRF is enforced automatically on all session-protected mutations.
- Two-level rate limiting per endpoint group (burst + sustained window), counters shared across workers via Redis.
- IP lockout on credential and code entry: 5 consecutive failures block for 30 seconds, escalating series block for 10 minutes; a successful attempt resets the counter.
- Registration creates an inactive user; the account activates only after a 6-digit email code (TTL, attempt limit, constant-time comparison).
- Comment spam filter, upload validation, request body limits. Fail-open degradation: an unavailable Redis is logged but never takes the API down.

## Caching and logging

Redis caches hot aggregates: average rating (invalidated on new votes), view counters and the title list (TTL). Personalized data is never cached.

Logs are split by purpose in `backend/logs/` (rotating files): `access.log` (HTTP), `application.log` (domain events), `security.log` (lockouts, CSRF, spam), `error.log` (errors only), `worker.log` (gunicorn lifecycle).

## Repository layout

```
.
├── backend/
│   ├── config/          # settings, urls, api root, throttling, logging
│   ├── accounts/        # auth, email verification, profiles, IP lockout
│   ├── catalog/         # titles, ratings, view history, aggregate cache
│   ├── comments/        # comments, reactions, spam filter
│   ├── watch/           # watch progress
│   └── Dockerfile       # python 3.14-slim, non-root, gunicorn
├── frontend/
│   ├── src/
│   │   ├── app/         # router, layout
│   │   ├── pages/       # route components
│   │   ├── features/    # player, comments, rating, watch, avatar crop
│   │   └── shared/      # api client + generated types, session, ui kit
│   ├── nginx/           # nginx config used in the frontend image
│   └── Dockerfile       # node build stage -> nginx
├── compose.yaml         # production-shaped stack
├── compose.dev.yaml     # dev override: vite HMR + runserver, host-mounted code
└── .env.example
```

## Getting started

### Environment

Copy `.env.example` to `.env` in the repository root and fill in the values.

| Variable | Purpose |
|----------|---------|
| `SECRET_KEY` | Django secret key, required in production |
| `DEBUG` | `True`/`False`; controls Django diagnostics but does not disable email delivery |
| `ALLOWED_HOSTS` | Comma-separated host list |
| `CSRF_TRUSTED_ORIGINS` | Comma-separated origins for production |
| `APP_PORT` | Host port for the frontend; use a different value when another project uses `4173` |
| `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` | Database connection |
| `REDIS_URL` | Optional; set by compose in Docker, in-process memory is used without it |
| `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` | Gmail SMTP credentials (an App Password is required); used in every mode |
| `API_AUTH_THROTTLE`, `API_AUTH_THROTTLE_SUSTAINED`, `API_WRITE_THROTTLE`, `API_WRITE_THROTTLE_SUSTAINED` | Rate limit overrides |

### Run with Docker

```
docker compose up --build
```

The application is available at `http://localhost:4173`. Migrations, title seeding and `collectstatic` run automatically on backend start.

### Development mode with hot reload

```
docker compose -f compose.yaml -f compose.dev.yaml up
```

Source directories are mounted from the host: vite serves the SPA with HMR at `http://localhost:5173`, Django restarts on backend changes. No image rebuilds needed while coding.

### Run locally without Docker

Backend: `cd backend`, create a venv, `pip install -r requirements.txt`, `python manage.py migrate`, `python manage.py runserver`. Frontend: `cd frontend`, `npm install`, `npm run dev` — vite proxies `/api` and `/media` to `127.0.0.1:8000`.

## Testing and linting

```
cd backend
python manage.py test        # service, API, lockout, cache and N+1 regression tests
ruff check .

cd frontend
npm run lint
npm run build                # strict type check + production build
```

CI runs both pipelines on every push and pull request.

## Roadmap

- [x] SPA frontend with generated API types, session auth, comments, ratings, watch progress.
- [x] django-ninja API over a service layer, domain app split.
- [x] Redis: two-level throttling, IP lockout, aggregate caching, fail-open degradation.
- [x] Structured logging, avatar cropping, responsive header, dev compose with HMR.
- [ ] TLS termination and global nginx hardening (CSP, HSTS in front).
- [ ] Catalog content served from the database instead of the frontend config.
- [ ] Load testing and measured performance tuning (indexes, microcache).

## Author

- [mailor](https://github.com/mailorq) — fullstack
