from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import PhotographerProfile, Review
from ..schemas import PhotographerOut

router = APIRouter()


@router.get("/", response_model=List[PhotographerOut])
def recommend_photographers(
    mood: Optional[str] = Query(None),
    max_price: Optional[float] = Query(None),
    db: Session = Depends(get_db),
):
    q = db.query(PhotographerProfile)
    if mood:
        for tag in [t.strip() for t in mood.split(",") if t.strip()]:
            q = q.filter(PhotographerProfile.moods.ilike(f"%{tag}%"))
    if max_price is not None:
        q = q.filter(PhotographerProfile.base_price <= max_price)

    results = q.all()
    # naive sorting: by average rating desc, then lower price
    def avg_rating(p: PhotographerProfile) -> float:
        if not p.reviews:
            return 0.0
        return sum(r.rating for r in p.reviews) / len(p.reviews)

    results.sort(key=lambda p: (-avg_rating(p), p.base_price))
    return results
