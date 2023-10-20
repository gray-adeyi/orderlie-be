from typing import cast
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_session_as_dependency
from models import School
from schemas import (
    SchoolSchema,
    CreateUpdateSchoolSchema,
    ResponseSchema,
)
from utils import get_model_by_id_or_404

school_router = APIRouter(
    prefix="/schools",
    tags=["schools"],
)


@school_router.post("", status_code=status.HTTP_201_CREATED)
async def create_school(
    school_data: CreateUpdateSchoolSchema,
    db: AsyncSession = Depends(get_session_as_dependency),
) -> ResponseSchema:
    """Let's you create a new school (University / Polytechnic/ College of Education) on Orderlie.

    Note:
        This endpoint is not for direct use to end users but available to Orderlie admins to create
        and manage institutions created on the platform. This helps mitigate the creation of the
        same institution with different names.
        This endpoint will be protected by authentication
    """
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
    """This endpoint let's you retrieve all the available Schools (University / Polytechnic / College of Education)
    on the Orderlie platform.

    Note:
        Current implementation does not support pagination but will get included in future releases.
    """
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
    """
    This endpoint let's you retrieve a Schools (University / Polytechnic / College of Education)
    by it's unique identifier.
    """
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
    """Let's you update a school (University / Polytechnic / College of Education) on Orderlie

    Note:
        This endpoint is not for direct use to end users but available to Orderlie admins to manage
        institutions on the platform. This helps mitigate the creation of the
        same institution with different names.
        This endpoint will be protected by authentication
    """
    school = cast(School, (await get_model_by_id_or_404(db, School, school_id)))
    school.name = update_data.name or school.name
    db.add(school)
    await db.commit()
    await db.refresh(school)
    return ResponseSchema(
        message="school successfully updated",
        data={"school": SchoolSchema(**school.__dict__).model_dump()},
    )
