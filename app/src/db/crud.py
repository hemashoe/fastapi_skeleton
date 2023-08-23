from typing import Union
from uuid import UUID

from sqlalchemy import and_, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import User, Faculty, StudyYear, Change


class UserDAL:
    """Data Access Layer for operating User info"""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(
        self,
        user_id: UUID,
        fullname: str,
        hashed_password: str,
        roles: str,
    ) -> User:
        new_user = User(
            id=user_id,
            fullname=fullname,
            hashed_password=hashed_password,
            roles=roles,
        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user

    async def delete_user(self, user_id: UUID) -> Union[UUID, None]:
        query = (
            update(User)
            .where(and_(User.user_id == user_id, User.is_active == True))
            .values(is_active=False)
            .returning(User.user_id)
        )
        res = await self.db_session.execute(query)
        deleted_user_id_row = res.fetchone()
        if deleted_user_id_row is not None:
            return deleted_user_id_row[0]

    async def get_user_by_id(self, user_id: UUID) -> Union[User, None]:
        query = select(User).where(User.id == user_id)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]

    async def get_user_by_fullname(self, fullname: str) -> Union[User, None]:
        query = select(User).where(User.fullname == fullname)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]

    async def update_user(self, user_id: UUID, **kwargs) -> Union[UUID, None]:
        query = (
            update(User)
            .where(and_(User.id == user_id, User.is_active == True))
            .values(kwargs)
            .returning(User.id)
        )
        res = await self.db_session.execute(query)
        update_user_id_row = res.fetchone()
        if update_user_id_row is not None:
            return update_user_id_row[0]


class FacultyDAL:
    """Data Access Layer for operating Faculty info"""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(
        self,
        faculty_id: UUID,
        faculty_name: str,
        faculty_dean: str,
    ) -> Faculty:
        new_faculty = User(
            id=faculty_id,
            faculty_name=faculty_name,
            faculty_dean=faculty_dean,
        )
        self.db_session.add(new_faculty)
        await self.db_session.flush()
        return new_faculty


class StudyYearDAL:
    """Data Access Layer for operating StudyYear info"""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(
        self,
        studyYear_id: int,
        year: str,
    ) -> StudyYear:
        new_studyYear = User(
            id=studyYear_id,
            year=year,
        )
        self.db_session.add(new_studyYear)
        await self.db_session.flush()
        return new_studyYear


class ChangeDAL:
    """Data Access Layer for operating Change info"""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(
        self,
        change_id: int,
        year: str,
    ) -> Change:
        new_studyYear = User(
            change_id=studyYear_id,
            year=year,
        )
        self.db_session.add(new_studyYear)
        await self.db_session.flush()
        return new_studyYear
