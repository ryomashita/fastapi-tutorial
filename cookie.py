from typing import Union

from fastapi import Cookie, FastAPI, Response
import json

app = FastAPI()

# クッキーの操作
# Response : HTTP レスポンスの ステータスコード・ヘッダ・クッキー等を操作するクラス

# cookie : HTTP ヘッダに含まれる要素で、client/server 間でデータをやり取りするためのもの
# 基本的に Name-Value ペアで、その他 Expires, Domain, Path, HttpOnly など属性を持っている。
# 属性は set_cookie() メソッドで設定できる


# 引数がクッキーであることを明示するため、 Cookie を使う
@app.get("/items/")
async def read_items(ads_id: Union[str, None] = Cookie(default=None)):
    # クライアントから送信されたクッキーの id を取得
    return {"ads_id": ads_id}


# クライアントにカスタムレスポンスを返すエンドポイント
@app.get("/custom_response/")
async def custom_response():
    content = {"message": "This is a custom response"}
    response = Response(content=json.dumps(content), media_type="application/json")
    response.headers["X-Custom-Header"] = "Custom value"
    response.set_cookie(key="cookie_id", value="cookie_value")
    return response
