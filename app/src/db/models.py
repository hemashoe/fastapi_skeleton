import uuid
from enum import Enum

from sqlalchemy import Boolean, Column, String
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class AdminRole(str, Enum):
    ROLE_ADMIN = "admin"
    ROLE_SUPERADMIN = "superadmin"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fullname = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    roles = Column(ARRAY(String), nullable=False)

    @property
    def is_superadmin(self) -> bool:
        return AdminRole.ROLE_SUPERADMIN in self.roles

    @property
    def is_admin(self) -> bool:
        return AdminRole.ROLE_ADMIN in self.roles

    def enrich_admin_roles_by_admin_role(self):
        if not self.is_admin:
            return {*self.roles, AdminRole.ROLE_ADMIN}

    def remove_admin_privileges_from_model(self):
        if self.is_admin:
            return {role for role in self.roles if role != AdminRole.ROLE_ADMIN}
