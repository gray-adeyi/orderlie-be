from uuid import UUID

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import Response
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_session_as_dependency
from extras.exporter import FileFormat, get_exporter_class, get_media_type
from models import Class
from schemas import (
    CreateClassSchema,
    UpdateClassSchema,
    ClassSchema,
    StudentSchema,
    ResponseSchema,
)

class_router = APIRouter(prefix="/{department_id}/classes", tags=["classes"])


@class_router.post("", status_code=status.HTTP_201_CREATED)
async def create_class(
    class_data: CreateClassSchema, db: AsyncSession = Depends(get_session_as_dependency)
) -> ResponseSchema:
    """This endpoint lets you create classes on the Orderlie platform"""
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
    """This endpoint lets you retrieve classes on the platform"""
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
    """This endpoint lets you retrieve a class by it's unique identifier"""
    class_ = await Class.get_by_id(db, class_id)
    return ResponseSchema(
        message="class successfully created",
        data={"class": ClassSchema(**class_.__dict__).model_dump()},
    )


@class_router.get("/{class_id}/students")
async def get_class_students(
    class_id: UUID, db: AsyncSession = Depends(get_session_as_dependency)
) -> ResponseSchema:
    """This endpoint lets you retrieve the student members of a class"""
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
async def partial_update_class(
    class_id: UUID,
    class_data: UpdateClassSchema,
    db: AsyncSession = Depends(get_session_as_dependency),
) -> ResponseSchema:
    """The endpoint lets you perform a partial update on a class information"""
    class_to_update = await Class.get_by_id(db, class_id)

    if not class_to_update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Class not found"
        )

    for key, value in class_data.model_dump().items():
        setattr(class_to_update, key, value)

    db.add(class_to_update)
    await db.commit()
    await db.refresh(class_to_update)

    return ResponseSchema(
        message="Class successfully updated",
        data={"class": ClassSchema(**class_to_update.__dict__).model_dump()},
    )


@class_router.post("/{class_id}/download")
async def download_class_data(
    class_id: UUID,
    format: FileFormat,
    db: AsyncSession = Depends(get_session_as_dependency),
):
    """This endpoint lets you download the class data in the desired format.

    Note: This endpoint has not been implemented yet
    """
    class_: Class = await Class.get_by_id(db, class_id)
    data = class_.get_export_data()
    exporter = get_exporter_class(format)()
    exporter.load_data(data)
    return Response(exporter.export(), media_type=get_media_type(format))


@class_router.post("/{class_id}/archive")
async def archive_class(
    class_id: UUID, db: AsyncSession = Depends(get_session_as_dependency)
):
    """
    This endpoint lets you archive a class. So its information is not indexed.

    Note: This endpoint has not been implemented yet
    """
    class_ = await Class.get_by_id(db, class_id)

    if not class_:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Class not found"
        )

    # Archive the class by setting the `archived` field to True
    class_.archived = True

    # Add the updated class instance back to the session
    db.add(class_)
    # Commit the changes to the database
    await db.commit()

    return ResponseSchema(message="class successfully archived")


@class_router.delete("/{class_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_class(
    class_id: UUID, db: AsyncSession = Depends(get_session_as_dependency)
):
    """This endpoint let's you delete a class."""
    await Class.delete(db, class_id)
