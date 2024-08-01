from typing import Any, List, Union

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = 10.5
    tags: List[str] = []


# response_model はレスポンスのスキーマを指定する
# 出力データの検証, JSON Schema, ドキュメント生成に利用される


@app.post("/items/", response_model=Item)
async def create_item(item: Item) -> Any:
    return item
    # Item 以外を返すと、 validation error が発生する
    # return {"name": "Item Name", "price": 9.99}


@app.get("/items/", response_model=List[Item])
async def read_items() -> Any:
    return [
        {"name": "Portal Gun", "price": 42.0},
        {"name": "Plumbus", "price": 32.0},
    ]


# response_model_exclude_unset : 未設定のプロパティを削除して出力する
# (デフォルト値が設定されていても、未設定なら削除される。)

items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/items/{item_id}", response_model=Item, response_model_exclude_unset=True)
async def read_item(item_id: str):
    return items[item_id]  # return {"name": "Foo", "price": 50.2}


# 出力形式への変換(プロパティの削除)が可能な場合、 FastAPI により自動でオブジェクトが変換される


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: Union[str, None] = None


class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: Union[str, None] = None


@app.post("/user/", response_model=UserOut)
async def create_user(user: UserIn) -> Any:
    return user
