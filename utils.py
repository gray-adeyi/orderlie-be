from typing import Type
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from models import M


async def get_model_by_id_or_404(
    db: AsyncSession, model_class: Type[M], id: UUID
) -> M | None:
    model: M | None = await model_class.get_by_id(db=db, id=id)
    if not model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{model_class.__name__} with id {id} not found",
        )
    return model
