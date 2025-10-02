from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime,
    Float,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship, Mapped, mapped_column

from .db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(10), nullable=False)  # U1 or U2
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    language: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    photographer_profile: Mapped["PhotographerProfile"] = relationship(
        back_populates="user", uselist=False
    )
    favorites: Mapped[list["Favorite"]] = relationship(back_populates="user")


class PhotographerProfile(Base):
    __tablename__ = "photographer_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    city: Mapped[str] = mapped_column(String(100), index=True)
    instagram: Mapped[Optional[str]] = mapped_column(String(100))
    instagram_verified: Mapped[bool] = mapped_column(default=False)
    bio: Mapped[Optional[str]] = mapped_column(Text)
    base_price: Mapped[float] = mapped_column(Float, default=0)
    venue_fee: Mapped[Optional[float]] = mapped_column(Float, default=0)
    equipment_fee: Mapped[Optional[float]] = mapped_column(Float, default=0)
    refund_policy: Mapped[Optional[str]] = mapped_column(Text)
    moods: Mapped[Optional[str]] = mapped_column(String(255))  # comma-separated tags

    user: Mapped[User] = relationship(back_populates="photographer_profile")
    availabilities: Mapped[list["Availability"]] = relationship(back_populates="photographer")
    portfolios: Mapped[list["PortfolioItem"]] = relationship(back_populates="photographer")
    reviews: Mapped[list["Review"]] = relationship(back_populates="photographer")
    liked_by: Mapped[list["Favorite"]] = relationship(back_populates="photographer")


class Availability(Base):
    __tablename__ = "availabilities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    photographer_id: Mapped[int] = mapped_column(ForeignKey("photographer_profiles.id"))
    date: Mapped[str] = mapped_column(String(10), index=True)  # YYYY-MM-DD
    start_time: Mapped[str] = mapped_column(String(5))  # HH:MM
    end_time: Mapped[str] = mapped_column(String(5))

    photographer: Mapped[PhotographerProfile] = relationship(back_populates="availabilities")

    __table_args__ = (
        UniqueConstraint("photographer_id", "date", "start_time", "end_time", name="uq_availability"),
    )


class PortfolioItem(Base):
    __tablename__ = "portfolio_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    photographer_id: Mapped[int] = mapped_column(ForeignKey("photographer_profiles.id"))
    media_url: Mapped[str] = mapped_column(String(255))
    media_type: Mapped[str] = mapped_column(String(10), default="image")  # image/video

    photographer: Mapped[PhotographerProfile] = relationship(back_populates="portfolios")


class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    photographer_id: Mapped[int] = mapped_column(ForeignKey("photographer_profiles.id"), index=True)
    rating: Mapped[int] = mapped_column(Integer)  # 1-5
    comment: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    photographer: Mapped[PhotographerProfile] = relationship(back_populates="reviews")


class Favorite(Base):
    __tablename__ = "favorites"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    photographer_id: Mapped[int] = mapped_column(ForeignKey("photographer_profiles.id"), index=True)

    user: Mapped[User] = relationship(back_populates="favorites")
    photographer: Mapped[PhotographerProfile] = relationship(back_populates="liked_by")

    __table_args__ = (
        UniqueConstraint("user_id", "photographer_id", name="uq_favorite"),
    )
