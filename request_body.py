from typing import List, Set, Union, Dict

from fastapi import FastAPI, Body
from pydantic import BaseModel, Field, HttpUrl


# リクエストボディで使うデータモデルを定義する (Pydantic の BaseModel を継承)
class Image(BaseModel):
    url: HttpUrl
    name: str


# Field によりメタデータを指定できる
class Item(BaseModel):
    # 全てのプロパティは Python 標準型で定義する
    # デフォルト値があるプロパティはオプションとして扱われる
    name: str
    description: Union[str, None] = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(..., gt=0, description="The price must be greater than zero")
    tax: Union[float, None] = None
    tags: Set[str] = (
        []
    )  # Set : ユニークな要素の集合 (リクエスト上で重複がある場合は、エラーにはならずSetに変換される)
    image: Union[List[Image], None] = (
        None  # 他のデータモデルをネストして使うこともできる
    )


class User(BaseModel):
    username: str
    full_name: Union[str, None] = None


my_app = FastAPI()


# リクエストボディ Item を定義する
# リクエストボディを送信するときは GET でｈはなく POST などを使う
# JSON のパース, 検証, Item への変換は FastAPI が自動で行う
@my_app.post("/items/")
async def create_item(item: Item):
    item_dict = item.model_dump()  # dict() は deprecated なので model_dump() を使う
    if item.tax:
        price_with_tax = item.price * (1 + item.tax)
        item_dict.update({"price_with_tax": price_with_tax})

    return item_dict


# path, query, request body を組み合わせる例
@my_app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: Union[str, None] = None):
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result


# Body() により、クエリではなくボディであることを明示する
@my_app.put("/items/importance/{item_id}")
async def update_item_importance(
    item_id: int, item: Item, user: User, importance: int = Body()
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    return results


# embed=True を指定すると、キーを含むオブジェクトとして定義される
# e.g., embed=True => {"item": {"name": "item_name", ... }}
# e.g., embed=False => {"name": "item_name", ... }
@my_app.put("/items/{item_id}")
async def update_item_embed(item_id: int, item: Item = Body(embed=True)):
    results = {"item_id": item_id, "item": item}
    return results


# Dict で未知のキー, str型以外のキーを受け取れる
@my_app.post("/index-weights/")
async def create_index_weights(weights: Dict[int, float]):
    return weights
