from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from routers import school_router

app = FastAPI(
    title="Orderlie API",
    description="Collect, organize and & export class biodata",
)
app.include_router(school_router, prefix="/api/v1")


@app.get("/")
async def docs():
    return RedirectResponse("/docs")
