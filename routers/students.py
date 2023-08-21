from uuid import UUID
from fastapi import APIRouter

student_router = APIRouter()


@student_router.post("/students")
async def create_student():
    ...

@student_router.patch("/students/{id}")
async def partial_update_student(id: UUID):
    ...

@student_router.delete("/students/{id}")
async def delete_student(id: UUID):
    ...
