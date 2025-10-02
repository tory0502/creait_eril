from typing import List, Optional
from pydantic import BaseModel

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import PhotographerProfile, User
from ..schemas import PhotographerOut

router = APIRouter()


class InstagramVerificationRequest(BaseModel):
    instagram: str
    verification_code: str


@router.get("/", response_model=List[PhotographerOut])
def search_photographers(
    city: Optional[str] = Query(None),
    mood: Optional[str] = Query(None),  # comma-separated
    max_price: Optional[float] = Query(None),
    db: Session = Depends(get_db),
):
    q = db.query(PhotographerProfile).join(User)
    if city:
        q = q.filter(PhotographerProfile.city.ilike(f"%{city}%"))
    if max_price is not None:
        q = q.filter(PhotographerProfile.base_price <= max_price)
    if mood:
        for tag in [t.strip() for t in mood.split(",") if t.strip()]:
            q = q.filter(PhotographerProfile.moods.ilike(f"%{tag}%"))

    results = q.all()
    return results


@router.get("/{photographer_id}", response_model=PhotographerOut)
def get_photographer(photographer_id: int, db: Session = Depends(get_db)):
    prof = (
        db.query(PhotographerProfile)
        .join(User)
        .filter(PhotographerProfile.id == photographer_id)
        .first()
    )
    if not prof:
        raise HTTPException(status_code=404, detail="Photographer not found")
    return prof


@router.post("/{photographer_id}/verify-instagram")
def verify_instagram(
    photographer_id: int, 
    request: InstagramVerificationRequest,
    db: Session = Depends(get_db)
):
    """인스타그램 인증 (데모용 - 실제로는 인스타 API 연동 필요)"""
    prof = db.query(PhotographerProfile).filter(PhotographerProfile.id == photographer_id).first()
    if not prof:
        raise HTTPException(status_code=404, detail="Photographer not found")
    
    # 데모용 간단한 인증 (실제로는 인스타그램 API로 확인)
    if request.verification_code == "VERIFY123":
        prof.instagram = request.instagram
        prof.instagram_verified = True
        db.commit()
        return {"message": "Instagram verified successfully!", "verified": True}
    else:
        return {"message": "Invalid verification code", "verified": False}


@router.put("/{photographer_id}/pricing")
def update_pricing(
    photographer_id: int,
    base_price: Optional[float] = None,
    venue_fee: Optional[float] = None,
    equipment_fee: Optional[float] = None,
    refund_policy: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """작가 가격 정보 업데이트"""
    prof = db.query(PhotographerProfile).filter(PhotographerProfile.id == photographer_id).first()
    if not prof:
        raise HTTPException(status_code=404, detail="Photographer not found")
    
    if base_price is not None:
        prof.base_price = base_price
    if venue_fee is not None:
        prof.venue_fee = venue_fee
    if equipment_fee is not None:
        prof.equipment_fee = equipment_fee
    if refund_policy is not None:
        prof.refund_policy = refund_policy
    
    db.commit()
    return {"message": "Pricing updated successfully"}
