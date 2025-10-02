from sqlalchemy.orm import Session

from app.db import SessionLocal, engine, Base
from app.models import User, PhotographerProfile, Availability, PortfolioItem, Review
from app.security import hash_password


def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def seed():
    db: Session = SessionLocal()

    u1 = User(email="tourist@example.com", password_hash=hash_password("Pass1234"), role="U1", name="Tourist A", language="en")
    p1_user = User(email="p1@example.com", password_hash=hash_password("Pass1234"), role="U2", name="Photog One", language="ko")
    p2_user = User(email="p2@example.com", password_hash=hash_password("Pass1234"), role="U2", name="Photog Two", language="en")

    db.add_all([u1, p1_user, p2_user])
    db.flush()

    p1 = PhotographerProfile(
        user_id=p1_user.id, 
        city="Seoul", 
        instagram="@sunset_photo", 
        instagram_verified=True,
        bio="Capturing warm film vibes under the sunlight", 
        base_price=300, 
        venue_fee=50,
        equipment_fee=25,
        refund_policy="Full refund if cancelled 24h before shoot",
        moods="film,portrait,warm"
    )
    p2 = PhotographerProfile(
        user_id=p2_user.id, 
        city="Busan", 
        instagram="@city_mood_photo", 
        instagram_verified=True,
        bio="Chic city mood, just like your Instagram feed", 
        base_price=300, 
        venue_fee=30,
        equipment_fee=20,
        refund_policy="50% refund if cancelled 12h before shoot",
        moods="vivid,landscape,bright"
    )
    db.add_all([p1, p2])
    db.flush()

    db.add_all([
        Availability(photographer_id=p1.id, date="2025-10-10", start_time="09:00", end_time="11:00"),
        Availability(photographer_id=p1.id, date="2025-10-10", start_time="14:00", end_time="16:00"),
        Availability(photographer_id=p2.id, date="2025-10-10", start_time="10:00", end_time="12:00"),
    ])

    db.add_all([
        PortfolioItem(photographer_id=p1.id, media_url="https://picsum.photos/seed/p1a/600/400", media_type="image"),
        PortfolioItem(photographer_id=p2.id, media_url="https://picsum.photos/seed/p2a/600/400", media_type="image"),
    ])

    db.add_all([
        Review(photographer_id=p1.id, rating=5, comment="Amazing film tones!"),
        Review(photographer_id=p1.id, rating=4, comment="Great portrait direction."),
        Review(photographer_id=p2.id, rating=5, comment="Loved the colors!"),
    ])

    db.commit()
    db.close()


if __name__ == "__main__":
    reset_db()
    seed()
    print("Seeded sample data.")
