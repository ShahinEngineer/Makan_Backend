from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    full_name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str  # plain password, will be hashed

class UserOut(UserBase):
    id: int
    model_config = {"from_attributes": True}

class UserInDB(UserOut):
    password_hash: str
    is_active: bool
    is_superuser: bool