from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserIn(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email:EmailStr
    password: str

class CarBase(BaseModel):
    brand: str
    model: str
    year: str
    price: int
    horse_power: int
    customs_cleared: bool = False

class CarIn(CarBase):
    pass

class CarOut(BaseModel):
    id: int
    brand: str
    model: str
    user: UserOut

    class Config:
        from_attributes = True    


# schema for token access

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None
