from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_session_as_dependency
from models import Class
from schemas import CreateClassSchema

class_router = APIRouter()


@class_router.post("/classes")
async def create_class(
    class_data: CreateClassSchema, db: AsyncSession = Depends(get_session_as_dependency)
):
    new_class = Class(**class_data.model_dump())
    try:
        db.add(new_class)
        await db.commit()
        await db.refresh(new_class)
    except IntegrityError as e:
        # TODO: This way of checking the source of the integrity error can break.
        if "classes_department_id_fkey" in str(e.orig):
            e.add_detail(
                f"department with id {class_data.department_id} does not exist"
            )
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.detail,
        )
    return CreateClassSchema(**new_class.__dict__)


@class_router.get("/classes")
async def get_classes():
    ...
    # TODO: should support filter & pagination


@class_router.get("/classes/{id}")
async def get_class(id: UUID):
    ...


@class_router.get("/classes/{id}/students")
async def get_class_members(id: UUID):
    ...


@class_router.patch("/classes/{id}")
async def partial_update_class(id: UUID):
    ...


@class_router.post("/classes/{id}/download")
async def download_class_data(id: UUID):
    ...


@class_router.post("/classes/{id}/archive")
async def archive_class(id: UUID):
    ...


@class_router.delete("/classes/{id}")
async def delete_class():
    ...
