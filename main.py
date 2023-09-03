from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from routers import class_router, student_router, school_router

app = FastAPI(
    title="Orderlie API",
    description="Collect, organize and & export class biodata",
)
app.include_router(class_router)
app.include_router(student_router)
app.include_router(school_router)


@app.get("/")
async def docs():
    return RedirectResponse("/docs")
