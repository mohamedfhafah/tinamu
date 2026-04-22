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
| Database | PostgreSQL |
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
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
flask db upgrade
python seed.py
flask run
```

### Frontend

```bash
cd frontend
npm install
npm run dev
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

- This repository is a student product prototype, not a production deployment.
- Sensitive configuration has been moved out of tracked files.
- `backend/API.md` documents the API surface in more detail.
| **J3** | Seed data réaliste pour la démo |
| **J4** | Répétition de la démo |
| **J5** | 🎯 **Démo finale** |

---

## 🔑 Règles de coordination

### 1. Modèles partagés
Le modèle `User` est utilisé par tout le monde. **Convention** :
- M1 est "propriétaire" du modèle `User` (il fait les migrations)
- Si un autre membre a besoin d'ajouter un champ → il fait une MR que M1 review

### 2. Services partagés
Chaque membre expose des **fonctions de service** réutilisables :
```
backend/app/services/
├── auth_service.py         # M1
├── feed_service.py         # M1
├── quiz_service.py         # M2
├── resource_service.py     # M2
├── conversation_service.py # M3
├── message_service.py      # M3
├── search_service.py       # M4
├── profile_service.py      # M4
```

### 3. Convention de branches
```
main
├── setup/flask-config       (M1, Sprint 1 Sem 1)
├── setup/react-config       (M2, Sprint 1 Sem 1)
├── feature/auth             (M1)
├── feature/feed-tinder      (M1)
├── feature/quiz             (M2)
├── feature/resources        (M2)
├── feature/messaging        (M3)
├── feature/search           (M4)
├── feature/profile          (M4)
└── feature/docker           (M4)
```

### 4. Merge quotidien
> Chaque soir, chaque membre merge `main` dans sa branche pour éviter les conflits massifs.

---

## 👥 Membres

| Membre | Rôle |
|--------|------|
| M1 | Auth + Feed Tinder |
| M2 | Quiz + Ressources |
| M3 | Messagerie + Recherche |
| M4 | Profil + UI/UX + DevOps |
