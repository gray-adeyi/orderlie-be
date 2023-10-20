from typing import cast
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_session_as_dependency
from models import School, Faculty
from schemas import (
    ResponseSchema,
    DepartmentSchema,
    FacultySchema,
    CreateUpdateFacultySchema,
)
from utils import get_model_by_id_or_404, get_one_model_obj_by_query_or_404

faculty_router = APIRouter(prefix="/faculties", tags=["faculties"])


@faculty_router.get("")
async def get_school_faculties(
    school_id: UUID,
    db: AsyncSession = Depends(get_session_as_dependency),
) -> ResponseSchema:
    """
    This endpoint lets you retrieve the faculties a school has by the school's unique identifier

    Note:
        Current implementation does not support pagination but will get included in future releases.
    """
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
    faculty_data: CreateUpdateFacultySchema,
    db: AsyncSession = Depends(get_session_as_dependency),
) -> ResponseSchema:
    """This endpoint let's you create a faculty for a school.

    Note:
        This endpoint is not for direct use to end users but available to Orderlie admins to create
        and manage faculites created on the platform. This helps mitigate the creation of the
        same faculties with different names.
        This endpoint will be protected by authentication
    """
    school = cast(
        School, (await get_model_by_id_or_404(db, School, faculty_data.school_id))
    )
    faculty = await Faculty.create(db=db, data=faculty_data.model_dump())
    faculty.__dict__["departments"] = await faculty.awaitable_attrs.departments
    return ResponseSchema(
        message="faculties successfully created",
        data={"faculty": FacultySchema(**faculty.__dict__).model_dump()},
    )


@faculty_router.get("/{faculty_id}")
async def get_school_faculty(
    faculty_id: UUID,
    db: AsyncSession = Depends(get_session_as_dependency),
) -> ResponseSchema:
    """This endpoint lets you retrieve a faculty by it's unique identifier"""
    query = select(Faculty).where(Faculty.id == faculty_id)
    faculty = await get_one_model_obj_by_query_or_404(db=db, statement=query)
    return ResponseSchema(
        message="faculties successfully retrieved",
        data={"faculty": FacultySchema(**faculty.__dict__).model_dump()},
    )


@faculty_router.patch("/{faculty_id}")
async def update_school_faculty(
    faculty_id: UUID,
    update_data: CreateUpdateFacultySchema,
    db: AsyncSession = Depends(get_session_as_dependency),
) -> ResponseSchema:
    """This endpoint lets you update the information of an existing faculty.

    Note:
        This endpoint is not for direct use to end users but available to Orderlie admins to manage
        faculties on the platform. This helps mitigate the creation of the
        same faculties with different names.
        This endpoint will be protected by authentication
    """
    query = select(Faculty).where(Faculty.id == faculty_id)
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
