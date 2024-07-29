from typing import Union  # 標準ライブラリ

from fastapi import FastAPI

my_app = FastAPI()

# --- Query Parameters ---

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


# e.g., /items/?skip=0&limit=10
@my_app.get("/items/")
# 非 parameter はクエリパラメータとして扱われる
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]


# 真偽値クエリ : `?short=True` のほか `=1`, `=on`, `=yes` が 真として扱われ、それ以外は偽となる
@my_app.get("/items/{item_id}")
async def read_item_with_query(
    # デフォルト値がない needy クエリは必須パラメータとなる。デフォルト値つきの q, short はオプションパラメータ。
    item_id: str,
    needy: str,
    q: Union[str, None] = None,
    short: bool = False,
):
    item = {"item_id": item_id, "needy": needy}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


# path parameter と query parameter を組み合わせても動作する (引数は順不同。名前でマッチングされる)
@my_app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: Union[str, None] = None, short: bool = False
):
    item = {"item_id": item_id, "user_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item
