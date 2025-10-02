# SnapLink Backend (MVP)

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
```

## Seed data (optional)
```bash
python backend/seed.py
```

## Run (serves API + static frontend)
```bash
uvicorn backend.app.main:app --reload
```

- Open UI: `http://127.0.0.1:8000/`
- Pages:
  - `/` search/list, login/signup, favorites
  - `/photographer.html?id={id}` detail + translate demo

## Endpoints (MVP)
- `POST /api/auth/signup` {email,password,role(U1/U2),name,language}
- `POST /api/auth/login` {email,password}
- `GET /api/photographers?city=Seoul&mood=film,portrait&max_price=200`
- `GET /api/photographers/{id}`
- `GET /api/recommendations?mood=film&max_price=200`
- `POST /api/favorites/add?user_id=1&photographer_id=2`
- `GET /api/favorites/list?user_id=1`
- `POST /api/chat/translate` {text,target}

Note: Favorites currently use `user_id` from token decoded on frontend for demo. In production, secure via backend auth dependency.
