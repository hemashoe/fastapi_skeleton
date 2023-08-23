import uuid
from typing import Optional
from pydantic import BaseModel, constr, UUID4


class TunedModel(BaseModel):
    class Config:
        """tells pydantic to convert even non dict obj to json"""

        orm_mode = True


class ShowUser(TunedModel):
    id: uuid.UUID
    fullname: str
    is_active: bool


class UserCreate(TunedModel):
    fullname: str
    password: str


class DeleteUserResponse(TunedModel):
    deleted_user_id: uuid.UUID


class UpdatedUserResponse(TunedModel):
    updated_user_id: uuid.UUID


class UpdateUserRequest(TunedModel):
    fullname: Optional[constr(min_length=1)]
    hashed_password: str


class Token(TunedModel):
    access_token: str
    token_type: str


class ShowFaculty(TunedModel):
    faculty_id: UUID4
    faculty_name: str
    faculty_dean: str


class FacultyCreate(TunedModel):
    faculty_id: UUID4
    faculty_name: str
    faculty_dean: str
