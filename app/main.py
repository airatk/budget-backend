from fastapi import FastAPI

from pydantic import BaseModel


api: FastAPI = FastAPI()


class Item(BaseModel):
    id: int
    name: str | None


@api.get("/items/{item_id}")
async def get_item(item_id: int):
    """Getting item with given ID.
    """

    return { "item_id": item_id }

@api.put("/items/{item_id}/update")
async def update_item(item_id: int, item: Item):
    """Updating item with given ID.
    """

    return { "item_id": item_id, "item": item }
