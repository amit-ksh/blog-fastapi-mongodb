from beanie import Document
from fastapi.security import HTTPBasicCredentials
from pydantic import BaseModel, EmailStr


class User(Document):
    """User model"""

    fullname: str
    email: EmailStr
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "fullname": "John Doe",
                "email": "john@doe.com",
                "password": "password",
            }
        }

    class Settings:
        name = "user"


class UserSignIn(HTTPBasicCredentials):
    """User sign in model"""

    class Config:
        json_schema_extra = {
            "example": {"username": "john@doe.com", "password": "password"}
        }


class UserData(BaseModel):
    """User data model"""

    fullname: str
    email: EmailStr

    class Config:
        json_schema_extra = {
            "example": {
                "fullname": "John Doe",
                "email": "john@doe.com",
            }
        }
