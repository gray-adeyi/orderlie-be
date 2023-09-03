from typing import cast
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_session_as_dependency
from models import School
from routers.faculties import faculty_router
from schemas import (
    SchoolSchema,
    CreateUpdateSchoolSchema,
    ResponseSchema,
)
from utils import get_model_by_id_or_404

school_router = APIRouter(prefix="/schools", tags=["schools"])
school_router.include_router(faculty_router)


@school_router.post("", status_code=status.HTTP_201_CREATED)
async def create_school(
    school_data: CreateUpdateSchoolSchema,
    db: AsyncSession = Depends(get_session_as_dependency),
) -> ResponseSchema:
    # TODO: Require admin scope to create new schools
    new_school = await School.create(db=db, data=school_data.model_dump())
    return ResponseSchema(
        message="school successfully created",
        data={"school": SchoolSchema(**new_school.__dict__).model_dump()},
    )


@school_router.get("")
async def get_schools(
    db: AsyncSession = Depends(get_session_as_dependency),
) -> ResponseSchema:
    # TODO: Pagination
    schools = [
        SchoolSchema(**school.__dict__).model_dump()
        for school in (await School.all(db))
    ]
    return ResponseSchema(
        message="schools successfully retrieved", data={"schools": schools}
    )


@school_router.get("/{school_id}")
async def get_school(
    school_id: UUID,
    db: AsyncSession = Depends(get_session_as_dependency),
) -> ResponseSchema:
    school = cast(School, (await get_model_by_id_or_404(db, School, school_id)))
    return ResponseSchema(
        message="school successfully retrieved",
        data={"school": SchoolSchema(**school.__dict__).model_dump()},
    )


@school_router.patch("/{school_id}")
async def update_school(
    school_id: UUID,
    update_data: CreateUpdateSchoolSchema,
    db: AsyncSession = Depends(get_session_as_dependency),
) -> ResponseSchema:
    school = cast(School, (await get_model_by_id_or_404(db, School, school_id)))
    school.name = update_data.name or school.name
    db.add(school)
    await db.commit()
    await db.refresh(school)
    return ResponseSchema(
        message="school successfully updated",
        data={"school": SchoolSchema(**school.__dict__).model_dump()},
    )
