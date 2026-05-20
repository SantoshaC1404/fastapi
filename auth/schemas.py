from pydantic import BaseModel, EmailStr


# Schemas for user creation 
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str


# Schemas for user login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

