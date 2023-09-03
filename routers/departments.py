from typing import cast
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_session_as_dependency
from models import Department, Faculty
from routers import class_router
from schemas import DepartmentSchema, ResponseSchema, CreateUpdateDepartmentSchema
from utils import get_one_model_obj_by_query_or_404

department_router = APIRouter(prefix="/{faculty_id}/departments", tags=["departments"])
department_router.include_router(class_router)


@department_router.get("")
async def get_school_faculty_departments(
    school_id: UUID,
    faculty_id: UUID,
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
    departments = [
        DepartmentSchema(**department.__dict__).model_dump()
        for department in (await faculty.awaitable_attrs.departments)
    ]
    return ResponseSchema(
        message="departments successfully retrieved",
        data={"departments": departments},
    )


@department_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
async def create_school_faculty_department(
    school_id: UUID,
    faculty_id: UUID,
    department_data: CreateUpdateDepartmentSchema,
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
    data = department_data.model_dump()
    data["faculty_id"] = faculty.id
    new_department = Department(**data)
    db.add(new_department)
    await db.commit()
    await db.refresh(new_department)
    return ResponseSchema(
        message="department successfully created",
        data={"department": DepartmentSchema(**new_department.__dict__).model_dump()},
    )


@department_router.get("/{department_id}")
async def get_school_faculty_department(
    school_id: UUID,
    faculty_id: UUID,
    department_id: UUID,
    db: AsyncSession = Depends(get_session_as_dependency),
) -> ResponseSchema:
    query = (
        select(Department)
        .where(Department.faculty_id == faculty_id)
        .where(Department.id == department_id)
        .where(Department.faculty.school_id == school_id)
    )
    department = cast(
        Department,
        (
            await get_one_model_obj_by_query_or_404(
                db=db, statement=query, resource_name="department"
            )
        ),
    )
    return ResponseSchema(
        message="department successfully retrieved",
        data={"department": DepartmentSchema(**department.__dict__).model_dump()},
    )
