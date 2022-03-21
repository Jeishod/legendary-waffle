import re
from datetime import datetime
from typing import List, Optional

from fastapi import HTTPException, status
from pydantic import BaseModel, EmailStr, validator


class TimestampMixin(BaseModel):
    class Config:
        json_encoders = {
            datetime: lambda v: int(v.timestamp()),
        }


class LoginResponseSchema(BaseModel):
    access_token: str
    token_type: str


class CheckEmailResponse(BaseModel):
    email: EmailStr
    is_available: bool


class UserBaseSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr


class UserRegisterSchema(UserBaseSchema):
    password: str

    @validator("password")
    def validate_password(cls, password, values) -> str:
        if not re.match(r"[A-Za-z0-9!@#$%^&*()_+]{6,}", password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="password should be at least 6 alphanumeric characters or symbols: !@#$%^&*()_+",
            )
        if values["email"] in password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="password should not contain email",
            )
        return password


class UserCreateSchema(UserRegisterSchema):
    is_superuser: bool


class UserSimpleSchema(UserBaseSchema):
    id: int
    is_superuser: bool

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "first_name": "Linus",
                "last_name": "Torvalds",
                "is_superuser": True,
            }
        }


class UserExtendedSchema(UserSimpleSchema):
    created_at: datetime
    updated_at: datetime
    archived_at: Optional[datetime]

    class Config:
        json_encoders = {
            datetime: lambda v: int(v.timestamp()),
        }


class UserUpdateSchema(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[EmailStr]


class UsersListSchema(BaseModel):
    users: List[UserExtendedSchema]

    class Config:
        orm_mode = True
