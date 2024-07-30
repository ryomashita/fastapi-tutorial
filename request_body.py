from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel


# データモデルを定義する (Pydantic の BaseModel を継承)
class Item(BaseModel):
    # 全てのプロパティは Python 標準型で定義する
    # デフォルト値があるプロパティはオプションとして扱われる
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None


my_app = FastAPI()


# リクエストボディ Item を受け取る
# リクエストボディを送信するときは GET でｈはなく POST などを使う
# JSON のパース, 検証, Item への変換を FastAPI が自動で行う
@my_app.post("/items/")
async def create_item(item: Item):
    item_dict = item.model_dump()  # dict() は deprecated なので model_dump() を使う
    if item.tax:
        price_with_tax = item.price * (1 + item.tax)
        item_dict.update({"price_with_tax": price_with_tax})

    return item_dict


# path, query, request body を組み合わせる
@my_app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: Union[str, None] = None):
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result
