import uuid
from typing import cast, TypeVar
from uuid import UUID

from sqlalchemy import ForeignKey, select, delete
from sqlalchemy.ext.asyncio import AsyncSession, AsyncAttrs
from sqlalchemy.orm import (
    mapped_column,
    Mapped,
    relationship,
    DeclarativeBase,
)

from extras.exporter import ExportData
from schemas import Level, AdmissionMode

M = TypeVar("M")


class Base(AsyncAttrs, DeclarativeBase):
    ...


class ModelMixin:
    # TODO: Implement a generic way to perform updates
    @classmethod
    async def create(cls, db: AsyncSession, data: dict) -> M:
        obj = cls(**data)
        db.add(obj)
        await db.commit()
        await db.refresh(obj)
        return obj

    @classmethod
    async def all(cls, db: AsyncSession) -> list[M]:
        objs: list[M] = []
        query = select(cls)
        objs = cast(list[Base], (await db.execute(query)).scalars())
        return objs

    @classmethod
    async def get_by_id(cls, db: AsyncSession, id: UUID) -> M | None:
        obj: M | None = None
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
    department: Mapped[Department] = relationship()
    governor_id: Mapped[UUID | None] = mapped_column()
    deputy_id: Mapped[UUID | None] = mapped_column()
    students: Mapped[list["Student"]] = relationship()
    archived: Mapped[bool] = mapped_column(default=False)

    def get_export_data(self) -> ExportData:
        rows = [
            (
                student.fist_name,
                student.middle_name,
                student.last_name,
                student.admission_mode,
                student.matriculation_numer,
                student.jamb_registration_number,
                student.personal_email_address,
            )
            for student in self.students
        ]
        return ExportData(
            headers=(
                "First Name",
                "Middle Name",
                "Last Name",
                "Admission Mode",
                "Matriculation Number",
                "JAMB Registration Number",
                "Personal Email Address",
            ),
            rows=rows,
            metadata={
                "Display Name": self.display_name,
                "Level": self.level,
                "Department": self.department.name,
                "Faculty": self.department.faculty.name,
                "School": self.department.faculty.school.name,
            },
        )


class Student(ModelMixin, Base):
    __tablename__ = "students"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    class_id: Mapped[UUID] = mapped_column(ForeignKey("classes.id"))
    first_name: Mapped[str] = mapped_column()
    middle_name: Mapped[str] = mapped_column()
    last_name: Mapped[str] = mapped_column()
    admission_mode: Mapped[AdmissionMode] = mapped_column()
    matriculation_number: Mapped[str | None] = mapped_column(nullable=True)
    jamb_registration_number: Mapped[str | None] = mapped_column(nullable=True)
    personal_email_address: Mapped[str] = mapped_column()
