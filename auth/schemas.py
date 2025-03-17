from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    access_token : str
    token_type : str



class TokenData(BaseModel):
    id: Optional[str]


class  OTPVerification(BaseModel):
    user_id:int
    otp: int
