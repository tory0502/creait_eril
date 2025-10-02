from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6,max_length=72)
    role: str  # U1 or U2
    name: str
    language: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1,max_length=72)


class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str
    name: str
    language: Optional[str] = None

    class Config:
        from_attributes = True


class PhotographerBase(BaseModel):
    id: int
    user_id: int
    city: str
    instagram: Optional[str] = None
    bio: Optional[str] = None
    base_price: float
    moods: Optional[str] = None

    class Config:
        from_attributes = True


class PortfolioItemOut(BaseModel):
    id: int
    media_url: str
    media_type: str

    class Config:
        from_attributes = True


class ReviewOut(BaseModel):
    id: int
    rating: int
    comment: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class AvailabilityOut(BaseModel):
    id: int
    date: str
    start_time: str
    end_time: str

    class Config:
        from_attributes = True


class PhotographerOut(PhotographerBase):
    user: UserOut
    portfolios: List[PortfolioItemOut] = []
    reviews: List[ReviewOut] = []
    availabilities: List[AvailabilityOut] = []


class FavoriteOut(BaseModel):
    id: int
    photographer: PhotographerOut

    class Config:
        from_attributes = True
