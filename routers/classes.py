from uuid import UUID
from fastapi import APIRouter


class_router = APIRouter()

@class_router.post("/classes")
async def create_class():
    ...

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


