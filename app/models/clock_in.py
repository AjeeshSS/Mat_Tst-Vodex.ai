from pydantic import BaseModel, EmailStr

class ClockIn(BaseModel):
    email: EmailStr
    location: str
