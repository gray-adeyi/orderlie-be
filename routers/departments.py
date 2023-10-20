from typing import cast
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_session_as_dependency
from models import Department, Faculty
from schemas import DepartmentSchema, ResponseSchema, CreateUpdateDepartmentSchema
from utils import get_one_model_obj_by_query_or_404

department_router = APIRouter(prefix="/{faculty_id}/departments", tags=["departments"])


@department_router.get("")
async def get_departments(
    faculty_id: UUID,
    db: AsyncSession = Depends(get_session_as_dependency),
) -> ResponseSchema:
    """This endpoint lets you retrieve all the departments a faculty has"""
    query = select(Faculty).where(Faculty.id == faculty_id)
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
async def create_department(
    department_data: CreateUpdateDepartmentSchema,
    db: AsyncSession = Depends(get_session_as_dependency),
) -> ResponseSchema:
    """This endpoint lets you create a department under a faculty.

    Note:
        This endpoint is not for direct use to end users but available to Orderlie admins to manage
        departments on the platform. This helps mitigate the creation of the
        same department with different names.
        This endpoint will be protected by authentication
    """
    query = select(Faculty).where(Faculty.id == department_data.faculty_id)
    faculty = cast(
        Faculty,
        (
            await get_one_model_obj_by_query_or_404(
                db=db, statement=query, resource_name="faculty"
            )
        ),
    )
    new_department = Department(**department_data.model_dump())
    db.add(new_department)
    await db.commit()
    await db.refresh(new_department)
    return ResponseSchema(
        message="department successfully created",
        data={"department": DepartmentSchema(**new_department.__dict__).model_dump()},
    )


@department_router.get("/{department_id}")
async def get_department(
    department_id: UUID,
    db: AsyncSession = Depends(get_session_as_dependency),
) -> ResponseSchema:
    """This endpoint let's you retrieve a department."""
    query = select(Department).where(Department.id == department_id)
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
