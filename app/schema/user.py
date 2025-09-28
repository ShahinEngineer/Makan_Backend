from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str  # plain password, will be hashed

class UserOut(UserBase):
    id: int

    class Config:
        orm_mode = True

class UserInDB(UserOut):
    hashed_password: str
    is_active: bool
    is_superuser: bool