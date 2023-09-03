from typing import Type
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from models import Base


async def get_model_by_id_or_404(
    db: AsyncSession, model_class: Type[Base], id: UUID
) -> Base | None:
    model: Base | None = await model_class.get_by_id(db=db, id=id)
    if not model:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{model_class.__name__} with id {id} not found",
        )
    return model
