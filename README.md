# Steins;Gate Fan Platform

A single-title streaming-style web application dedicated to Steins;Gate: watch both seasons and the movie, register an account, manage a profile, rate titles and discuss them in comments.

The project is a portfolio work demonstrating a production-shaped full-stack setup: an SPA frontend, a Django backend, and a containerized deployment behind nginx.

## Architecture

```
browser
   |
   v
nginx (frontend container, :4173)
   |-- /            SPA static (React build)
   |-- /assets/     hashed bundles, cached immutable
   |-- /static/     Django admin static (shared volume)
   |-- /media/      user uploads (shared volume)
   |-- /api/   -----> backend (gunicorn, :8000)
   |-- /admin/ -----> backend (gunicorn, :8000)
                          |
                          v
                     PostgreSQL 16
```

- `frontend/` — React SPA. All pages, routing and UI state live here. Served by nginx, which also proxies API and admin traffic to the backend.
- `backend/` — Django project. Business logic, ORM models, admin. HTTP API layer is being migrated to django-ninja; until then legacy view code remains as the reference implementation.
- `compose.yaml` — three services: `db` (PostgreSQL), `backend` (gunicorn), `frontend` (nginx).

## Tech stack

| Layer      | Technology |
|------------|------------|
| Frontend   | React 19, TypeScript (strict), Vite, Tailwind CSS 4, React Router 7 |
| Backend    | Python 3.14, Django 6, gunicorn |
| Database   | PostgreSQL 16 (SQLite for local development) |
| Infra      | Docker, docker compose, nginx |

## Repository layout

```
.
├── backend/
│   ├── config/          # settings, urls, wsgi/asgi
│   ├── mainpage/        # titles, comments, ratings, view history
│   ├── users/           # auth, email verification, profiles
│   ├── manage.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── app/         # router, layout
│   │   ├── pages/       # route components
│   │   ├── features/    # player, comments, rating
│   │   └── shared/      # ui kit, config, session
│   ├── nginx/           # nginx config used in the frontend image
│   └── Dockerfile
├── compose.yaml
└── .env.example
```

## Getting started

### Prerequisites

- Docker with the compose plugin, or
- Python 3.14+ and Node.js 22+ for local development.

### Environment

Copy `.env.example` to `.env` in the repository root and fill in the values. For local development without Docker, place the same file at `backend/.env`.

| Variable              | Purpose |
|-----------------------|---------|
| `SECRET_KEY`          | Django secret key, required in production |
| `DEBUG`               | `True`/`False`; security headers and cookies are DEBUG-aware |
| `ALLOWED_HOSTS`       | Comma-separated host list |
| `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` | Database connection |
| `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` | SMTP credentials for registration emails |

### Run with Docker

```
docker compose up --build
```

The application is available at `http://localhost:4173`. Migrations and `collectstatic` run automatically on backend start.

### Run locally (development)

Backend:

```
cd backend
python -m venv .venv && .venv/Scripts/activate   # or source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Frontend (separate terminal):

```
cd frontend
npm install
npm run dev
```

Vite serves the SPA at `http://localhost:5173` and proxies `/api` and `/media` to `http://127.0.0.1:8000`.

## Testing

```
cd backend
python manage.py test
```

Frontend type checking and production build:

```
cd frontend
npm run build
```

## Status and roadmap

- [x] SPA frontend: all pages ported from Django templates (titles, lab page, auth, profile, comments, rating).
- [x] Containerized deployment: nginx + gunicorn + PostgreSQL.
- [ ] HTTP API on django-ninja (session auth, typed schemas, OpenAPI).
- [ ] Frontend switched from local demo state to the API (comments, ratings, watch progress persistence).
- [ ] Domain split of backend apps (accounts, catalog, comments, watch).

## Authors

- [mailor](https://github.com/mailorq) — frontend, backend
- [oinqq](https://github.com/oniqq1) — backend
