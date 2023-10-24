from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from routers import school_router, faculty_router, department_router, class_router
from routers.students import student_router

app = FastAPI(
    title="Orderlie API",
    description="Collect, organize and & export class biodata",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Provide specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

VERSION_PREFIX = "/api/v1"

app.include_router(school_router, prefix=VERSION_PREFIX)
app.include_router(faculty_router, prefix=VERSION_PREFIX)
app.include_router(department_router, prefix=VERSION_PREFIX)
app.include_router(class_router, prefix=VERSION_PREFIX)
app.include_router(student_router, prefix=VERSION_PREFIX)


@app.get("/")
async def docs():
    return RedirectResponse("/docs")
