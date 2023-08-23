import uuid
from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, Column, Integer, String, Time, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class AdminRole(str, Enum):
    ROLE_CLIENT = "client"
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


class Faculty(Base):
    __tablename__ = "faculty"

    id = Column(Integer, primary_key=True, autoincrement=True)
    faculty_name = Column(String, nullable=False)
    faculty_dean = Column(String, nullable=False)


class StudyYear(Base):
    __tablename__ = "study_year"

    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(String, nullable=False)


class Change(Base):
    __tablename__ = "change"

    id = Column(Integer, primary_key=True, autoincrement=True)
    change_name = Column(String, nullable=False)
    start_time = Column(Time, nullable=True)
    end_time = Column(Time, nullable=True)
    change_year = Column(Integer, ForeignKey("study_year.id"), nullable=True)

    change_year = relationship("StudyYear")


class Profession(Base):
    __tablename__ = "professions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    profession_name = Column(String, nullable=False)


class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, autoincrement=True)
    group_name = Column(String, nullable=False)
    group_year = Column(String, nullable=False)
    group_change_id = Column(Integer, ForeignKey("change.id"), nullable=True)
    study_year_id = Column(
        Integer, ForeignKey("study_year.id"), nullable=False
    )  # Add this line

    group_change = relationship("Change")
    study_year = relationship("StudyYear")  # Add this line


class Student(Base):
    __tablename__ = "students"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    fullname = Column(String, nullable=False)
    student_id = Column(String, nullable=False)
    gender = Column(String, nullable=False)
    student_image = Column(String, nullable=False)
    course = Column(Integer, nullable=False)
    qr_code = Column(String, nullable=False)
    created_time = Column(DateTime, default=datetime.now())
    student_profession_id = Column(Integer, ForeignKey("professions.id"))
    student_group_id = Column(Integer, ForeignKey("groups.id"))

    student_profession = relationship("Profession")
    student_group = relationship("Group")


class GeneralAttendance:
    __tablename__ = "general_attendance"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    attended_student_id = Column(
        String, ForeignKey("students.student_id"), nullable=False
    )
    attended_student_name = Column(
        String, ForeignKey("students.fullname"), nullable=False
    )
    attended_time = Column(DateTime, nullable=False, default=datetime.now())
    attended_change = Column(Integer, ForeignKey("change.id"), nullable=True)
    students_qr_code = Column(String, nullable=False)

    attended_student = relationship("Student")
