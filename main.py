from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from uuid import UUID

app = FastAPI(
        title="Orderlie API",
        description="Collect, organize and & export class biodata",
        )


@app.get("/")
async def docs():
    return RedirectResponse("/docs")


@app.post("/classes")
async def create_class():
    ...

@app.get("/classes")
async def get_classes():
    ...
    # TODO: should support filter & pagination

@app.get("/classes/{id}")
async def get_class(id: UUID):
    ...

@app.get("/classes/{id}/students")
async def get_class_members(id: UUID):
    ...

@app.patch("/classes/{id}")
async def partial_update_class(id: UUID):
    ...

@app.post("/classes/{id}/download")
async def download_class_data(id: UUID):
    ...

@app.post("/classes/{id}/archive")
async def archive_class(id: UUID):
    ...

@app.delete("/classes/{id}")
async def delete_class():
    ...


@app.post("/students")
async def create_student():
    ...

@app.patch("/students/{id}")
async def partial_update_student(id: UUID):
    ...

@app.delete("/students/{id}")
async def delete_student(id: UUID):
    ...
