from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_session_as_dependency
from models import Student, Class
from schemas import StudentSchema, ResponseSchema, CreateStudentSchema
from utils import get_model_by_id_or_404

student_router = APIRouter(prefix="/{class_id}/students", tags=["students"])


@student_router.post("")
async def create_student(
    class_id: UUID,
    student_data: CreateStudentSchema,
    db: AsyncSession = Depends(get_session_as_dependency),
):
    data = student_data.model_dump()
    data["class_id"] = class_id
    student = await Student.create(db, data)
    return ResponseSchema(
        message="students successfully retrieved",
        data={"student": StudentSchema(**student.__dict__).model_dump()},
    )


@student_router.patch("/{student_id}")
async def partial_update_student(
    class_id: UUID,
    student_id: UUID,
    db: AsyncSession = Depends(get_session_as_dependency),
):
    await get_model_by_id_or_404(db, Class, class_id)


@student_router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(
    class_id: UUID,
    student_id: UUID,
    db: AsyncSession = Depends(get_session_as_dependency),
):
    await get_model_by_id_or_404(db, Class, class_id)
    await Student.delete(db, student_id)
