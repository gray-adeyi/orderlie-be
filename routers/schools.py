from typing import cast
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_session_as_dependency
from models import School, Faculty
from schemas import (
    SchoolSchema,
    CreateUpdateSchoolSchema,
    ResponseSchema,
    FacultySchema,
    CreateFacultySchema,
)
from utils import get_model_by_id_or_404

school_router = APIRouter()


@school_router.post("/schools", status_code=status.HTTP_201_CREATED)
async def create_school(
    school_data: CreateUpdateSchoolSchema,
    db: AsyncSession = Depends(get_session_as_dependency),
) -> ResponseSchema:
    # TODO: Require admin scope to create new schools
    new_school = await School.create(db=db, data=school_data.model_dump())
    return ResponseSchema(
        message="school successfully created",
        data=SchoolSchema(**new_school.__dict__).model_dump(),
    )


@school_router.get("/schools")
async def get_schools(
    db: AsyncSession = Depends(get_session_as_dependency),
) -> ResponseSchema:
    # TODO: Pagination
    schools = [
        SchoolSchema(**school.__dict__).model_dump()
        for school in (await School.all(db))
    ]
    return ResponseSchema(message="schools successfully retrieved", data=schools)


@school_router.get("/schools/{school_id}")
async def get_school(
    school_id: UUID,
    db: AsyncSession = Depends(get_session_as_dependency),
) -> ResponseSchema:
    school = cast(School, (await get_model_by_id_or_404(db, School, school_id)))
    return ResponseSchema(
        message="school successfully retrieved",
        data=SchoolSchema(**school.__dict__).model_dump(),
    )


@school_router.patch("/schools/{school_id}")
async def update_school(
    school_id: UUID,
    update_data: CreateUpdateSchoolSchema,
    db: AsyncSession = Depends(get_session_as_dependency),
):
    school = cast(School, (await get_model_by_id_or_404(School, school_id)))
    school.name = update_data.name or school.name
    db.add(school)
    await db.commit()
    await db.refresh(school)
    return ResponseSchema(
        message="school successfully updated",
        data=SchoolSchema(**school.__dict__).model_dump(),
    )


@school_router.get("/schools/{school_id}/faculties")
async def get_school_faculties(
    school_id: UUID,
    db: AsyncSession = Depends(get_session_as_dependency),
) -> ResponseSchema:
    school = cast(School, (await get_model_by_id_or_404(db, School, school_id)))
    faculties = [
        FacultySchema(**faculty.__dict__).model_dump()
        for faculty in (await school.awaitable_attrs.faculties)
    ]
    return ResponseSchema(message="faculties successfully retrieved", data=faculties)


@school_router.post(
    "/schools/{school_id}/faculties", status_code=status.HTTP_201_CREATED
)
async def create_school_faculty(
    school_id: UUID,
    faculty_data: CreateFacultySchema,
    db: AsyncSession = Depends(get_session_as_dependency),
):
    school = cast(School, (await get_model_by_id_or_404(db, School, school_id)))
    data = faculty_data.model_dump()
    data["school_id"] = school_id
    faculty = await Faculty.create(db=db, data=data)
    faculty.__dict__["departments"] = await faculty.awaitable_attrs.departments
    return ResponseSchema(
        message="faculties successfully retrieved",
        data=FacultySchema(**faculty.__dict__).model_dump(),
    )


@school_router.get("/schools/{id}/faculties")
async def get_school_faculty(id: UUID):
    ...


@school_router.patch("/schools/{id}/faculties")
async def update_school_faculty(id: UUID):
    ...


@school_router.get("/schools/{school_id}/faculties/{faculty_id}/departments")
async def get_school_faculty_departments(school_id: UUID, faculty_id: UUID):
    ...


@school_router.post("/schools/{school_id}/faculties/{faculty_id}/departments")
async def create_school_faculty_department(school_id: UUID, faculty_id: UUID):
    ...


@school_router.get(
    "/schools/{school_id}/faculties/{faculty_id}/departments/{department_id}"
)
async def get_school_faculty_department(
    school_id: UUID, faculty_id: UUID, department_id: UUID
):
    ...
