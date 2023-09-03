from typing import Type
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy import Executable
from sqlalchemy.ext.asyncio import AsyncSession

from models import M


async def get_model_by_id_or_404(db: AsyncSession, model_class: Type[M], id: UUID) -> M:
    model: M | None = await model_class.get_by_id(db=db, id=id)
    if not model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{model_class.__name__} with id {id} not found",
        )
    return model


async def get_one_model_obj_by_query_or_404(
    db: AsyncSession, statement: Executable, resource_name: str | None = None
) -> M:
    result = (await db.execute(statement)).scalar_one_or_none()
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource_name or 'resource'} not found",
        )
    return result
