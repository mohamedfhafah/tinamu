# TinAMU Frontend

React + Vite frontend for the TinAMU campus social-platform demo.

## What is implemented

- Demo login with seeded student accounts
- Feed with discovery cards, matches, and community posts
- Quiz screen with API-backed scoring and leaderboard refresh
- Resource library with filtering and quick add form
- Messaging inbox backed by demo conversation endpoints
- Search and profile pages connected to the Flask API

## Local run

```bash
npm install
npm run dev
```

Set `VITE_API_URL` if your backend does not run on `http://localhost:5000/api`.

## Verification

```bash
npm run build
```
