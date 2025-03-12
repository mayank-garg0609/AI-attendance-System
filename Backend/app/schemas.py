from pydantic import BaseModel
from datetime import date
from typing import Optional

class LoginBody(BaseModel):
    email: str
    password: str

class att(BaseModel):
    student_id: int
    course_id: int
    date: date

class User(BaseModel):
    name: str
    email: str
    password: str

class ShowUserProfile(BaseModel):
    student_name: str
    email: str
    class Config:
        from_attributes = True

class TokenData(BaseModel):
    username: Optional[str]=None