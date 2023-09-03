from typing import cast
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_session_as_dependency
from models import School, Faculty
from routers.departments import department_router
from schemas import (
    ResponseSchema,
    DepartmentSchema,
    FacultySchema,
    CreateUpdateFacultySchema,
)
from utils import get_model_by_id_or_404, get_one_model_obj_by_query_or_404

faculty_router = APIRouter(prefix="/{school_id}/faculties", tags=["faculties"])
faculty_router.include_router(department_router)


@faculty_router.get("")
async def get_school_faculties(
    school_id: UUID,
    db: AsyncSession = Depends(get_session_as_dependency),
) -> ResponseSchema:
    school = cast(School, (await get_model_by_id_or_404(db, School, school_id)))
    faculties = []
    for faculty in await school.awaitable_attrs.faculties:
        faculty.__dict__["departments"] = [
            DepartmentSchema(**department.__dict__).model_dump()
            for department in (await faculty.awaitable_attrs.departments)
        ]
        faculties.append(FacultySchema(**faculty.__dict__).model_dump())
    return ResponseSchema(
        message="faculties successfully retrieved", data={"faculties": faculties}
    )


@faculty_router.post("", status_code=status.HTTP_201_CREATED)
async def create_school_faculty(
    school_id: UUID,
    faculty_data: CreateUpdateFacultySchema,
    db: AsyncSession = Depends(get_session_as_dependency),
) -> ResponseSchema:
    school = cast(School, (await get_model_by_id_or_404(db, School, school_id)))
    data = faculty_data.model_dump()
    data["school_id"] = school_id
    faculty = await Faculty.create(db=db, data=data)
    faculty.__dict__["departments"] = await faculty.awaitable_attrs.departments
    return ResponseSchema(
        message="faculties successfully created",
        data={"faculty": FacultySchema(**faculty.__dict__).model_dump()},
    )


@faculty_router.get("/{faculty_id}")
async def get_school_faculty(
    school_id: UUID,
    faculty_id: UUID,
    db: AsyncSession = Depends(get_session_as_dependency),
) -> ResponseSchema:
    query = (
        select(Faculty)
        .where(Faculty.school_id == school_id)
        .where(Faculty.id == faculty_id)
    )
    faculty = await get_one_model_obj_by_query_or_404(db=db, statement=query)
    return ResponseSchema(
        message="faculties successfully retrieved",
        data={"faculty": FacultySchema(**faculty.__dict__).model_dump()},
    )


@faculty_router.patch("/{faculty_id}")
async def update_school_faculty(
    school_id: UUID,
    faculty_id: UUID,
    update_data: CreateUpdateFacultySchema,
    db: AsyncSession = Depends(get_session_as_dependency),
) -> ResponseSchema:
    query = (
        select(Faculty)
        .where(Faculty.school_id == school_id)
        .where(Faculty.id == faculty_id)
    )
    faculty = cast(
        Faculty,
        (
            await get_one_model_obj_by_query_or_404(
                db=db, statement=query, resource_name="faculty"
            )
        ),
    )
    faculty.name = update_data.name or faculty.name
    db.add(faculty)
    await db.commit()
    return ResponseSchema(
        message="faculty successfully updated",
        data={"faculty": FacultySchema(**faculty.__dict__).model_dump()},
    )
