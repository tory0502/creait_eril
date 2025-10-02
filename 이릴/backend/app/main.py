from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .routers import auth, photographers, favorites, recommendations, chat
from .db import Base, engine

# Create tables on startup (for SQLite demo). In production, use migrations.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SnapLink - Tourist x Photographer Platform", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(photographers.router, prefix="/api/photographers", tags=["photographers"])
app.include_router(favorites.router, prefix="/api/favorites", tags=["favorites"])
app.include_router(recommendations.router, prefix="/api/recommendations", tags=["recommendations"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])

app.mount("/", StaticFiles(directory="backend/static", html=True), name="static")

@app.get("/")
def root():
    return {"message": "SnapLink API is running"}
