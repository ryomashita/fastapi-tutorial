from typing import Union, List

from fastapi import FastAPI, Query

my_app = FastAPI()

# クエリパラメータのメタデータは Query により宣言できる


@my_app.get("/items/")
async def read_items(
    q: Union[str, None] = Query(
        default=None, min_length=3, max_length=50, pattern="^fixedquery$"
    )
):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# 必須クエリの場合は Query の default 引数を省略する
@my_app.get("/items/{item_id}")
async def read_item(item_id: str, q: str = Query(min_length=3)):
    result = {"item_id": item_id}
    if q:
        result


# 同じクエリパラメータを複数受け取る場合は List を使う
@my_app.get("/items/{item_id}/name")
async def read_item_name(item_id: int, q: List[str] = Query(default=["foo", "bar"])):
    result = {"item_id": item_id}
    if q:
        result.update({"q": q})
    return result


# その他の Query 引数
# alias : パラメータの別名
# title : ドキュメントで表示されるパラメータ名
# description : ドキュメントで表示されるパラメータの説明
# deprecated : ドキュメントで非推奨として表示される
