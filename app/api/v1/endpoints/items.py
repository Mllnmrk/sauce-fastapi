from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core import db
from app.crud import crud_item
from app.models.item import Item, ItemCreate, ItemPublic, ItemUpdate

router = APIRouter()


@router.post("/", response_model=ItemPublic)
async def create_item(
    *,
    session: Annotated[AsyncSession, Depends(db.get_db)],
    item_in: ItemCreate,
) -> Item:
    return await crud_item.create_item(session=session, item_create=item_in)


@router.get("/", response_model=list[ItemPublic])
async def read_items(
    session: Annotated[AsyncSession, Depends(db.get_db)],
    skip: int = 0,
    limit: int = 100,
) -> list[Item]:
    return list(await crud_item.get_items(session=session, skip=skip, limit=limit))


@router.get("/{item_id}", response_model=ItemPublic)
async def read_item(
    session: Annotated[AsyncSession, Depends(db.get_db)], item_id: int
) -> Item:
    item = await crud_item.get_item(session=session, item_id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.put("/{item_id}", response_model=ItemPublic)
async def update_item(
    *,
    session: Annotated[AsyncSession, Depends(db.get_db)],
    item_id: int,
    item_in: ItemUpdate,
) -> Item:
    item = await crud_item.get_item(session=session, item_id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return await crud_item.update_item(session=session, db_item=item, item_update=item_in)


@router.delete("/{item_id}", response_model=ItemPublic)
async def delete_item(
    session: Annotated[AsyncSession, Depends(db.get_db)], item_id: int
) -> Item:
    item = await crud_item.get_item(session=session, item_id=item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return await crud_item.delete_item(session=session, db_item=item)
