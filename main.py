from enum import Enum
from pydantic import BaseModel
from fastapi import FastAPI, Query
from typing import Annotated

app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "bar"}, {"item_name": "Baz"}]


class ModelName(str, Enum):
    alexnet = "alexnet"
    renet = "renet"
    lenet = "lenet"


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user_id(user_id: int):
    return {"user_id": user_id}


@app.get("/model/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW"}
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LecNN all the images"}

    return {"model_name": model_name, "message": "Have some rediduals"}


@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip: skip + limit]


# path and query params
@app.get("/q/items/{item_id}")
async def read_item_id(item_id: str, q: str | None = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}


@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(user_id: int, item_id: int, q: str | None = None, short: bool = False):
    item = {"user_id": user_id, "item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update({"description": "This is an amazing item that has a long description"})
    return item


@app.get("/i/items/{item_id}")
async def read_item_needy(item_id: int, needy: str):
    item = ({"item_id": item_id, "needy": needy})
    return item


@app.get("/it/items/{item_id}")
async def read_item_it(item_id: str, needy: str | None = None, skip: int = 0, limit: int | None = None):
    item = ({"item_id": item_id, "needy": needy, "skip": skip, "limit": limit})
    return item


@app.post("/item/")
async def create_item(item_id: int, item: Item):
    item_dict = item.model_dump()
    if item.tax is not None:
        price_with_tax = item.tax + item.price
        item_dict.update({"price_with_tax": price_with_tax})
    return item_id, item_dict


@app.put("/item/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.model_dump()}


@app.put("/i/item/{item_id}")
async def i_update_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result


# Query-параметры и валидация строк

@app.get("/i/items")
async def read_items_i(q: Annotated[str | None, Query(min_length=1, max_length=50)] = "fixedquery"):
    result = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        result.update({"q": q})
    return result


@app.get("/i2/items")
async def read_items_i2(q: Annotated[str, Query(min_length=1, max_length=50)]):
    result = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        result.update({"q": q})
    return result


@app.get("/i3/items")
async def read_items_i3(q: Annotated[list[str] | None, Query()] = None):
    query_item = {"q": q}
    return query_item


@app.get("/i4/items")
async def read_items_i4(q: Annotated[list[str] | None, Query()] = ["foo", "bar"]):
    query_item = {"q": q}
    return query_item


@app.get("/i5/items")
async def read_items_i5(q: Annotated[list, Query()] = []):  # Просто list
    query_item = {"q": q}
    return query_item


@app.get("/i6/items")
async def read_items_i6(q: Annotated[str | None, Query(title="Query string", min_length=3)] = None, ):
    result = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        result.update({"q": q})

    return result
