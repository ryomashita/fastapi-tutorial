from typing import Union

from fastapi import FastAPI, Path, Query

app = FastAPI()

# パスパラメータのメタデータは Path により宣言できる
# Path, Query は共通の引数を持つが、 Path は必須のため default 引数を常に省略する


# gt : greater than, ge : greater than or equal
# lt : less than,    le : less than or equal
# 従って gt < item_id <= le となる
@app.get("/items/{item_id}")
async def read_items(
    item_id: int = Path(title="The ID of the item to get", gt=0, le=1000),
    q: Union[str, None] = Query(default=None, alias="item-query"),
):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    return results
