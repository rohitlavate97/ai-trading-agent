from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from models.user import RoleEnum

class UserBase(BaseModel):
    email: EmailStr
    is_active: Optional[bool] = True
    role: RoleEnum = RoleEnum.USER

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None

class UserInDBBase(UserBase):
    id: str

    model_config = ConfigDict(from_attributes=True)

class User(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
    hashed_password: str
