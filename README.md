# StudyBuddy API

Backend for StudyBuddy — a study workspace where students organise notes into
subjects and folders, keep summaries, take quizzes, and track their progress.

Flask REST API with JWT auth and PostgreSQL.

## Stack

| Layer      | Tech                                                        |
| ---------- | ----------------------------------------------------------- |
| API        | Flask · Flask-RESTful · Marshmallow                         |
| Auth       | Flask-JWT-Extended (access + refresh tokens)                 |
| Data       | SQLAlchemy · Alembic (PostgreSQL in production, SQLite in dev) |
| Runtime    | Docker · Render                                             |

## Features

- Signup, login, logout, token refresh, and token validation
- Subjects with nested folders (notes, PDFs, docs, video)
- Notes with tags, archive flag, and stored summaries
- Quizzes with questions, attempts, and per-question answers
- Summaries scoped to a note, a folder, or everything
- Health check

## API

| Method | Path | Purpose |
| ------ | ---- | ------- |
| `POST` | `/api/v1/auth/signup` | Create an account |
| `POST` | `/api/v1/auth/login` | Obtain access + refresh tokens |
| `POST` | `/api/v1/auth/refresh` | Get a new access token |
| `DELETE` | `/api/v1/auth/logout` | Log out |
| `GET` | `/api/v1/auth/validate` | Validate a token |
| `GET` `POST` | `/api/v1/notes` | List or create notes |
| `GET` `PUT` `DELETE` | `/api/v1/notes/<note_id>` | Read, update, or delete a note |
| `GET` `POST` | `/api/v1/folders` | List or create folders |
| `GET` `PUT` `DELETE` | `/api/v1/folders/<folder_id>` | Read, update, or delete a folder |
| `GET` `POST` | `/api/v1/quizzes` | List or create quizzes |
| `POST` | `/api/v1/quiz-attempts` | Submit a quiz attempt |
| `GET` `POST` | `/api/v1/summaries` | List or create summaries |
| `GET` `POST` | `/api/v1/subjects` | List or create subjects |
| `GET` `PUT` `DELETE` | `/api/v1/subjects/<uuid>` | Read, update, or delete a subject |
| `GET` `POST` | `/api/v1/subjects/<subject_uuid>/folders` | List or create subject folders |
| `GET` `PUT` `DELETE` | `/api/v1/subjects/<subject_uuid>/folders/<folder_uuid>` | Manage one subject folder |
| `POST` | `/api/v1/subjects/<subject_uuid>/folders/<folder_uuid>/upload` | Add a resource to a folder |
| `GET` | `/api/v1/health` | Health check |

## Local setup

```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env   # then fill in the values
flask db upgrade
python app.py
```

The API listens on port `5000`.

## Environment variables

| Variable | Purpose |
| -------- | ------- |
| `FLASK_ENV` | `development`, `production`, or `testing` |
| `SECRET_KEY` | Flask session signing key |
| `DATABASE_URL` | SQLAlchemy connection string (required in production) |
| `JWT_SECRET_KEY` | JWT signing key |
| `REDIS_URL` | Redis connection string |
| `MAIL_SERVER` `MAIL_PORT` `MAIL_USERNAME` `MAIL_PASSWORD` | Outgoing mail |
| `CELERY_BROKER_URL` `CELERY_RESULT_BACKEND` | Celery (defaults to `REDIS_URL`) |

Never commit `.env` or real credentials. `.env` is git-ignored.

## Deployment

`Dockerfile` builds the API image. Pushes to the `live` branch trigger
`.github/workflows/main.yml`, which pushes the image to Docker Hub and calls a
Render deploy hook.

Set these repository secrets before the workflow can run:

- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN`
- `RENDER_DEPLOY_HOOK`

`DATABASE_URL` is supplied by the deployment environment and is not baked into
the image.

## Status

The folder upload endpoint currently records resource metadata with a
placeholder URL; file storage is not wired up yet. Redis and Celery are
configured but have no async tasks. There is no automated test suite.
