# TinAMU

TinAMU is a university social platform prototype for computer-science students. The project combines a Flask API and a React frontend to explore peer discovery, messaging, quizzes, and resource sharing inside a single campus-oriented product.

## Current scope

- Student authentication and profile flows
- Matching / social feed concepts
- Real-time messaging foundations with Socket.IO
- Quiz and learning-oriented interactions
- Shared resources for the university community

## Configuration

Runtime secrets are expected to come from environment variables. For local development, copy `backend/.env.example` to `backend/.env`, set your values, and start the backend with explicit credentials rather than relying on static secrets committed in code.

## Tech stack

| Layer | Technologies |
| --- | --- |
| Frontend | React, Vite, Redux Toolkit, React Router, Axios |
| Backend | Flask, Flask-JWT-Extended, Flask-SQLAlchemy, Flask-Migrate, Flask-SocketIO |
| Database | SQLite by default, PostgreSQL optional |
| Realtime | Socket.IO |

## Repository layout

```text
tinamu/
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── services/
│   │   ├── sockets/
│   │   └── utils/
│   ├── config.py
│   ├── run.py
│   └── seed.py
└── frontend/
    ├── src/
    │   ├── components/
    │   ├── services/
    │   ├── socket/
    │   └── store/
    └── public/
```

## Getting started

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python seed.py
python run.py
```

The local demo now boots on SQLite without provisioning PostgreSQL.

If you explicitly want PostgreSQL, install the optional adapter too:

```bash
pip install -r requirements-postgres.txt
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Verification

Backend sanity check:

```bash
python3 -m compileall backend/app backend/run.py backend/config.py backend/seed.py
```

Frontend production build:

```bash
cd frontend
npm run build
```

## Configuration

The repository ships only with `backend/.env.example`.

Create your local file with:

```bash
cp backend/.env.example backend/.env
```

Then set values appropriate for your machine:

- `SECRET_KEY`
- `JWT_SECRET_KEY`
- `DATABASE_URL`
- `CORS_ORIGINS`

Do not commit local environment files.

## Notes

- This repository is a functional student product demo, not a production deployment.
- Sensitive configuration has been moved out of tracked files.
- `backend/API.md` documents the API surface in more detail.
