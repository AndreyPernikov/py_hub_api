from fastapi import FastAPI

app = FastAPI()


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


@app.get("/users")
async def read_user_1():
    return ['Andrey', 'Stas']


@app.get("/users")
async def read_user_2():
    return ['Vika', 'Vasilisa']
