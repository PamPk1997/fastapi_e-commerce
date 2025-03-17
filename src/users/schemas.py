from pydantic import BaseModel, EmailStr,Field
from typing import Optional
from datetime import datetime
from src.models import RoleType
from typing import List


class UserBase(BaseModel):
    username: str = Field(...,max_length=100)
    first_name: str = Field(...,max_length=100)
    last_name: Optional[str] = Field(None,max_length=100)
    email: Optional[EmailStr] = Field(None,max_length=100)
    phone_number: Optional[str] = Field(None,max_length=15)
    address: str = Field(..., max_length=250)


class UserCreate(UserBase):
    password_hash: str = Field(...,max_length=255)


class UserOut(UserBase):
    id: int
    username: str
    first_name: str 
    last_name: str

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    email: Optional[EmailStr] = Field(None, max_length=100)
    phone_number: Optional[str] = Field(None, max_length=15)
    address: Optional[str] = Field(None, max_length=250)


    

class RoleOut(BaseModel):
    id: int 
    role_name: RoleType
    desc: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True



class RoleRequest(BaseModel):
    username: str 
    role_name: List[RoleType]

    class Config:
        from_attributes = True
