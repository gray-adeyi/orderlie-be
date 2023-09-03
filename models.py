import uuid
from typing import cast
from uuid import UUID

from sqlalchemy import ForeignKey, select, delete
from sqlalchemy.ext.asyncio import AsyncSession, AsyncAttrs
from sqlalchemy.orm import (
    mapped_column,
    Mapped,
    relationship,
    DeclarativeBase,
)

from schemas import Level, AdmissionMode


class Base(AsyncAttrs, DeclarativeBase):
    ...


class ModelMixin:
    # TODO: Implement a generic way to perform updates
    @classmethod
    async def create(cls, db: AsyncSession, data: dict) -> Base:
        obj = cls(**data)
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj

    @classmethod
    async def all(cls, db: AsyncSession) -> list[Base]:
        objs: list[Base] = []
        query = select(cls)
        objs = cast(list[Base], (await db.execute(query)).scalars())
        return objs

    @classmethod
    async def get_by_id(cls, db: AsyncSession, id: UUID) -> Base | None:
        obj: Base | None = None
        query = select(cls).where(cls.id == id)
        obj = (await db.execute(query)).scalar_one_or_none()
        return obj

    @classmethod
    async def delete(cls, db: AsyncSession, id: UUID):
        query = delete(cls).where(cls.id == id)
        await db.execute(query)


class School(ModelMixin, Base):
    __tablename__ = "schools"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(unique=True)
    faculties: Mapped[list["Faculty"]] = relationship(back_populates="school")


class Faculty(ModelMixin, Base):
    __tablename__ = "faculties"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[
        str
    ] = mapped_column()  # TODO: Figure out how to do a unique based on school_id
    school_id: Mapped[UUID] = mapped_column(ForeignKey("schools.id"))
    school: Mapped[School] = relationship(back_populates="faculties")
    departments: Mapped[list["Department"]] = relationship(back_populates="faculty")


class Department(ModelMixin, Base):
    __tablename__ = "departments"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column()
    faculty_id: Mapped[UUID] = mapped_column(ForeignKey("faculties.id"))
    faculty: Mapped[Faculty] = relationship(back_populates="departments")


class Class(ModelMixin, Base):
    __tablename__ = "classes"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    display_name: Mapped[str | None] = mapped_column()
    level: Mapped[Level] = mapped_column()
    department_id: Mapped[UUID] = mapped_column(ForeignKey("departments.id"))
    governor_id: Mapped[UUID | None] = mapped_column()
    deputy_id: Mapped[UUID | None] = mapped_column()
    students: Mapped[list["Student"]] = relationship()


class Student(ModelMixin, Base):
    __tablename__ = "students"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    class_id: Mapped[UUID] = mapped_column(ForeignKey("classes.id"))
    first_name: Mapped[str] = mapped_column()
    middle_name: Mapped[str] = mapped_column()
    last_name: Mapped[str] = mapped_column()
    admission_mode: Mapped[AdmissionMode] = mapped_column()
    matriculation_number: Mapped[str | None] = mapped_column()
    jamb_registration_number: Mapped[str | None] = mapped_column()
    personal_email_address: Mapped[str] = mapped_column()
