from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from app.schema.user import UserCreate, UserInDB, UserOut, UserOut
from app.lib.user import create_user, get_user_by_email, get_user
from app.db.session import get_db

router = APIRouter()

@router.post("/users/", response_model=UserOut)
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    try:
        existing_user = get_user_by_email(db, user.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        # Create new user
        db_user = create_user(db, user)
        return db_user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/users/{user_id}", response_model=UserOut)
def read_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
