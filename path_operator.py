from typing import Set, Union

from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()

# path operation デコレータに渡せる引数を紹介する。


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: Set[str] = set()


@app.post(
    "/items/",
    response_model=Item,  # レスポンスモデル
    status_code=status.HTTP_201_CREATED,  # ステータスコード
    tags=["items"],  # OpenAPI 上の分類タグを定義する
    summary="Create an item",  # 概要 (OpenAPI)
    description="Create an item with all the information, ...",  # 説明 (OpenAPI)
)
async def create_item(item: Item):
    return item


@app.get("/users/", tags=["users"], deprecated=True)  # 非推奨としてマーク
async def read_users():
    """
    ユーザー情報を返す

    - summary 引数の代わりに docstring (Markdown) で概要を記述できる
    """
    return [{"username": "johndoe"}]
