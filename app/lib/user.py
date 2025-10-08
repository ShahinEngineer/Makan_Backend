from sqlalchemy.orm import Session
from app.models.user import User
from app.schema.user import UserCreate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate) -> User:
    new_user = User(
        full_name=user.full_name,
        email=user.email,
        hashed_password=pwd_context.hash(user.password),  # Hash the password
        is_active=1,
        is_superuser=1
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()