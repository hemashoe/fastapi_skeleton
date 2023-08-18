import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_db
from src.db.schemas import UserCreate, ShowUser
from src.db.crud import UserDAL

user_router = APIRouter()


async def _create_new_user(body: UserCreate, db) -> ShowUser:
    async with db as session:
        async with session.begin():
            user_dal = UserDAL(session)
            user = await user_dal.create_user(
                user_id=uuid.uuid4,
                fullname=body.fullname,
                password=body.password,
            )
            return ShowUser(
                user_id=user.user_id,
                fullname=user.fullname,
                role=user.role,
                is_active=user.is_active,
            )


@user_router.post("/", response_model=ShowUser)
async def create_user(body: UserCreate, db: AsyncSession = Depends(get_db)) -> ShowUser:
    return await _create_new_user(body, db)
