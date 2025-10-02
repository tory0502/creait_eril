from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Favorite, PhotographerProfile, User
from ..schemas import FavoriteOut

router = APIRouter()


# For demo: assume user_id via query (replace with auth dependency later)
@router.post("/add", response_model=FavoriteOut)
def add_favorite(user_id: int, photographer_id: int, db: Session = Depends(get_db)):
    user = db.query(User).get(user_id)
    prof = db.query(PhotographerProfile).get(photographer_id)
    if not user or not prof:
        raise HTTPException(status_code=404, detail="User or Photographer not found")

    existing = (
        db.query(Favorite)
        .filter(Favorite.user_id == user_id, Favorite.photographer_id == photographer_id)
        .first()
    )
    if existing:
        return existing

    fav = Favorite(user_id=user_id, photographer_id=photographer_id)
    db.add(fav)
    db.commit()
    db.refresh(fav)
    return fav


@router.get("/list", response_model=List[FavoriteOut])
def list_favorites(user_id: int, db: Session = Depends(get_db)):
    favs = db.query(Favorite).filter(Favorite.user_id == user_id).all()
    return favs
