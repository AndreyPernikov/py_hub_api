from enum import Enum

from fastapi import FastAPI

app = FastAPI()


class ModelName(str, Enum):
    alexnet = "alexnet"
    renet = "renet"
    lenet = "lenet"


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

