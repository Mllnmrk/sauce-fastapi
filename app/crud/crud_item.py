from collections.abc import Sequence

from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.item import Item, ItemCreate, ItemUpdate


async def create_item(session: AsyncSession, item_create: ItemCreate) -> Item:
    db_item = Item.model_validate(item_create)
    session.add(db_item)
    await session.commit()
    await session.refresh(db_item)
    return db_item


async def get_item(session: AsyncSession, item_id: int) -> Item | None:
    return await session.get(Item, item_id)


async def get_items(
    session: AsyncSession, skip: int = 0, limit: int = 100
) -> Sequence[Item]:
    statement = select(Item).offset(skip).limit(limit)
    result = await session.exec(statement)
    return result.all()


async def update_item(
    session: AsyncSession, db_item: Item, item_update: ItemUpdate
) -> Item:
    item_data = item_update.model_dump(exclude_unset=True)
    db_item.sqlmodel_update(item_data)
    session.add(db_item)
    await session.commit()
    await session.refresh(db_item)
    return db_item


async def delete_item(session: AsyncSession, db_item: Item) -> Item:
    await session.delete(db_item)
    await session.commit()
    return db_item
