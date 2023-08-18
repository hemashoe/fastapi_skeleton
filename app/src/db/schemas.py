import uuid
from typing import Optional
from pydantic import BaseModel, constr


class TunedModel(BaseModel):
    class Config:
        """tells pydantic to convert even non dict obj to json"""

        orm_mode = True


class ShowUser(TunedModel):
    id: uuid.UUID
    fullname: str
    is_active: bool


class UserCreate(BaseModel):
    fullname: str
    password: str


class DeleteUserResponse(BaseModel):
    deleted_user_id: uuid.UUID


class UpdatedUserResponse(BaseModel):
    updated_user_id: uuid.UUID


class UpdateUserRequest(BaseModel):
    fullname: Optional[constr(min_length=1)]
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str
