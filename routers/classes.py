from uuid import UUID

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_session_as_dependency
from models import Class
from routers.students import student_router
from schemas import (
    CreateClassSchema,
    ClassSchema,
    StudentSchema,
    ResponseSchema,
)

class_router = APIRouter(prefix="/classes", tags=["classes"])
class_router.include_router(student_router)


@class_router.post("", status_code=status.HTTP_201_CREATED)
async def create_class(
    class_data: CreateClassSchema, db: AsyncSession = Depends(get_session_as_dependency)
) -> ResponseSchema:
    try:
        new_class = await Class.create(db=db, data=class_data.model_dump())
        return ResponseSchema(
            message="class successfully created",
            data={"class": ClassSchema(**new_class.__dict__).model_dump()},
        )
    except IntegrityError as e:
        if "classes_department_id_fkey" in str(e.orig):
            e.add_detail(f"department with id {class_data.department_id} not found")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)


@class_router.get("")
async def get_classes(
    db: AsyncSession = Depends(get_session_as_dependency),
) -> ResponseSchema:
    # TODO: Pagination
    classes = [
        ClassSchema(**class_.__dict__).model_dump() for class_ in await Class.all(db)
    ]
    return ResponseSchema(
        message="classes successfully retrieved",
        data={"classes": classes},
    )


@class_router.get("/{class_id}")
async def get_class(
    class_id: UUID, db: AsyncSession = Depends(get_session_as_dependency)
) -> ResponseSchema:
    class_ = await Class.get_by_id(db, class_id)
    return ResponseSchema(
        message="class successfully created",
        data={"class": ClassSchema(**class_.__dict__).model_dump()},
    )


@class_router.get("/{class_id}/students")
async def get_class_students(
    class_id: UUID, db: AsyncSession = Depends(get_session_as_dependency)
) -> ResponseSchema:
    class_ = await Class.get_by_id(db, class_id)
    students = [
        StudentSchema(**student.__dict__).model_dump()
        for student in await class_.awaitable_attrs.students
    ]
    return ResponseSchema(
        message="students successfully retrieved",
        data={"students": students},
    )


@class_router.patch("/{class_id}")
async def partial_update_class(class_id: UUID) -> ResponseSchema:
    ...


@class_router.post("/{class_id}/download")
async def download_class_data(class_id: UUID):
    ...


@class_router.post("/{class_id}/archive")
async def archive_class(class_id: UUID):
    ...


@class_router.delete("/{class_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_class(
    class_id: UUID, db: AsyncSession = Depends(get_session_as_dependency)
):
    await Class.delete(db, class_id)
