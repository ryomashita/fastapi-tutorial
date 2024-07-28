from enum import Enum # 標準ライブラリ

from fastapi import FastAPI

# run with: 
#   poetry run uvicorn main:my_app --reload
#   - main: the file name (main.py)
#   - app: the FastAPI instance
#   - --reload: auto-reload the server when the file changes

my_app = FastAPI()

@my_app.get("/") # operation decorator + path
async def my_root():
    # define response(cocntent)
    return {"message": "Hello World"}

# 固定パスは parameter path よりさきに定義する
@my_app.get("/items/me")
async def read_item_me():
    return {"item_id": "the current user's id"}

@my_app.get("/items/{item_id}") # path parameter
async def read_item(item_id: int):
    # FastAPI は Python型宣言によりvalidationを行う
    # "/items/4.2" へのアクセスはエラーレスポンスが返る
    return {"item_id": item_id}

# --- Enum parameters ---

# str 型の enum を定義
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

# enum 型の path parameter
@my_app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    # is (==) か .value
    if model_name is ModelName.alexnet:
        # Enum をそのまま返せる
        # (FastAPI が定義型 str に変換する)
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}
    return {"model_name": model_name, "message": "Have some residuals"}

# --- filepath parameters ---

# `:path` は任意のパス形式にマッチする
# `/files//home/myfile.txt` など スラッシュが連続する形になる
@my_app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}

