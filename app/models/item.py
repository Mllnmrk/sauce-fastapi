from sqlmodel import Field, SQLModel


class ItemBase(SQLModel):
    title: str
    description: str | None = None


class Item(ItemBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    owner_id: int | None = Field(default=None, foreign_key="user.id")


class ItemCreate(ItemBase):
    pass


class ItemUpdate(ItemBase):
    title: str | None = None  # type: ignore
    description: str | None = None  # type: ignore


class ItemPublic(ItemBase):
    id: int
    owner_id: int | None = None
