from datetime import timedelta
from typing import Union
from uuid import UUID

from db.session import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.settings import variables
from src.core.utils import Hasher, create_access_token
from src.db.crud import UserDAL
from src.db.models.users import AdminRole, User
from src.db.schemas import ShowUser, Token, UserCreate


login_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")


async def _create_new_user(body: UserCreate, session) -> ShowUser:
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.create_user(
            fullname=body.fullname,
            hashed_password=Hasher.get_password_hash(body.password),
            roles=[
                AdminRole.ROLE_ADMIN,
            ],
        )
        return ShowUser(
            user_id=user.user_id,
            fullname=user.fullname,
            is_active=user.is_active,
        )


async def _delete_user(user_id, session) -> Union[UUID, None]:
    async with session.begin():
        user_dal = UserDAL(session)
        deleted_user_id = await user_dal.delete_user(
            user_id=user_id,
        )
        return deleted_user_id


async def _update_user(
    updated_user_params: dict, user_id: UUID, session
) -> Union[UUID, None]:
    async with session.begin():
        user_dal = UserDAL(session)
        updated_user_id = await user_dal.update_user(
            user_id=user_id, **updated_user_params
        )
        return updated_user_id


async def _get_user_by_id(user_id, session) -> Union[User, None]:
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.get_user_by_id(
            user_id=user_id,
        )
        if user is not None:
            return user


def check_user_permissions(target_user: User, current_user: User) -> bool:
    if AdminRole.ROLE_SUPERADMIN in current_user.roles:
        raise HTTPException(
            status_code=406, detail="Superadmin cannot be deleted via API."
        )
    if target_user.user_id != current_user.user_id:
        # check admin role
        if not {
            AdminRole.ROLE_ADMIN,
            AdminRole.ROLE_SUPERADMIN,
        }.intersection(current_user.roles):
            return False
        # check admin deactivate superadmin attempt
        if (
            AdminRole.ROLE_SUPERADMIN in target_user.roles
            and AdminRole.ROLE_ADMIN in current_user.roles
        ):
            return False
        # check admin deactivate admin attempt
        if (
            AdminRole.ROLE_ADMIN in target_user.roles
            and AdminRole.ROLE_ADMIN in current_user.roles
        ):
            return False
    return True


async def _get_user_by_fullname_for_auth(fullname: str, session: AsyncSession):
    async with session.begin():
        user_dal = UserDAL(session)
        return await user_dal.get_user_by_fullname(
            fullname=fullname,
        )


async def authenticate_user(
    fullname: str, password: str, db: AsyncSession
) -> Union[User, None]:
    user = await _get_user_by_fullname_for_auth(fullname=fullname, session=db)
    if user is None:
        return
    if not Hasher.verify_password(password, user.hashed_password):
        return
    return user


async def get_current_user_from_token(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(
            token, variables.secret_key, algorithms=[variables.algorithm]
        )
        fullname: str = payload.get("sub")
        if fullname is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await _get_user_by_fullname_for_auth(fullname=fullname, session=db)
    if user is None:
        raise credentials_exception
    return user


@login_router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)
):
    user = await authenticate_user(form_data.fullname, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=variables.token_life)
    access_token = create_access_token(
        data={"sub": user.email, "other_custom_data": [1, 2, 3, 4]},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}