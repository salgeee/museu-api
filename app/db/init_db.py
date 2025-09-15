from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.security import get_password_hash
from app.db.database import engine, Base
from app.models.user import User
from app.models.news import News


def init_db(db: Session) -> None:
    # Create tables
    Base.metadata.create_all(bind=engine)

    # Check if admin exists
    admin = db.query(User).filter(User.email == settings.ADMIN_EMAIL).first()
    if not admin:
        # Create admin user
        admin = User(
            email=settings.ADMIN_EMAIL,
            username="admin",
            full_name=settings.ADMIN_NAME,
            hashed_password=get_password_hash(settings.ADMIN_PASSWORD),
            is_active=True,
            is_admin=True
        )
        db.add(admin)
        db.commit()
        print(f"Admin user created: {settings.ADMIN_EMAIL}")
    else:
        print("Admin user already exists")