from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status, Path
from core.models import db, Product
from . import crud


async def product_by_id(
    product_id: int = Annotated[int, Path],
    session: AsyncSession = Depends(db.scope_session_dependency),
) -> Product:
    product = await crud.get_product(session=session, product_id=product_id)
    if product:
        return product
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Product {product_id} not found!",
    )
