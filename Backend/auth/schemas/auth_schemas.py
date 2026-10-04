from datetime import datetime
from pydantic import BaseModel,EmailStr

class RegisterSchemas(BaseModel):
    email : EmailStr
    password: str
    role: str
    created_at: datetime

class LoginSchemas(BaseModel):
    email : EmailStr
    password: str