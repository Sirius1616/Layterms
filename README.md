# Layterms

Layterms takes the documents people actually receive in real life — medical reports, hospital bills, legal letters, insurance emails — and re-explains them in plain language. Upload a document, and Layterms extracts its content and walks you through what it means, one question at a time, in language a layperson can follow.

The project is built on the FastAPI + React full-stack pattern, with the application domain (documents, explanations, conversations) designed specifically for this product.

## Current state

Under active development. The backend foundation is complete and the document workflow is the next milestone.

**Implemented**

- Full user authentication: registration, login with JWT, profile management, password reset via email, admin user management
- Database models for users, documents, explanations, conversations (SQLModel + Alembic migrations)
- Utility endpoints: health check, admin-only test email, admin user provisioning
- Frontend shell: login/signup/password-recovery pages, dashboard, and a documents area with upload, explanation, and chat UI

**In progress** — tracked as [GitHub issues](https://github.com/Sirius1616/Layterms/issues)

- Document upload, storage, and listing
- Text extraction pipeline (PDFs, scanned images, emails) with background jobs
- Document type classification
- AI service layer for plain-language explanations and follow-up Q&A
- Streaming conversation answers

## Tech stack

**Backend** (`backend/`)

- FastAPI, SQLModel, Alembic, PostgreSQL
- Pydantic Settings for configuration, PyJWT for tokens, Argon2/Bcrypt password hashing
- Email delivery via the `emails` library with Jinja2 templates
- Sentry for error tracking

**Frontend** (`frontend/`)

- Vite + React + TypeScript
- TanStack Router (file-based routing), TanStack Query for server state
- Tailwind CSS v4 with shadcn/ui components
- API client generated from the backend's OpenAPI schema (`openapi-ts`)

## Getting started

### Prerequisites

- Python 3.14+
- [uv](https://docs.astral.sh/uv/) (package manager, from `uv.lock`)
- PostgreSQL running locally
- Node.js or Bun

### 1. Backend

```bash
cd backend
uv sync
source .venv/bin/activate
```

Create a `.env` file in `backend/` (see `app/core/config.py` for the full list of settings). Minimum for local development:

```
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_USERNAME=postgres
DATABASE_PASSWORD=postgres
DATABASE_NAME=layterms
SECRET_KEY=change-me-to-a-long-random-string
FIRST_SUPERUSER=admin@example.com
FIRST_SUPERUSER_PASSWORD=change-me
```

Apply migrations and create the first admin user:

```bash
alembic upgrade head
python -m app.initial_data
```

Start the API:

```bash
uvicorn app.main:app --reload
```

- API: `http://localhost:8000/api/v1`
- Interactive docs: `http://localhost:8000/docs`

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173` and sign in with the superuser created above.

To regenerate the API client after backend changes:

```bash
npm run generate-client
```

## Project layout

```
backend/
  app/
    api/
      routes/            # login, users, utils, private
      deps.py            # auth dependencies (current user, admin)
    core/                # config, database, security
    models.py            # SQLModel tables + request/response schemas
    crud.py              # database operations
    initial_data.py      # seeds the first superuser
    utils.py             # email and token helpers
  migration/             # Alembic migrations
  scripts/               # dev scripts (lint, format, tests, prestart)
frontend/
  src/
    routes/              # file-based router (login, dashboard, documents)
    components/          # UI components
    services/            # API service layer
    types/               # domain types
    client/              # generated API client
```

## License

Private.
