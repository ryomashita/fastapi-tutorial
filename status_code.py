from fastapi import FastAPI, status
from http import HTTPStatus

app = FastAPI()


# status_code でレスポンスのHTTPステータスコードを指定できる

@app.post("/items/", status_code=HTTPStatus.CREATED)
async def create_item(name: str):
    return {"name": name}

# int, http.HTTPStatus, fastapi.status のいずれかを使用する
assert status.HTTP_201_CREATED == 201
assert HTTPStatus.CREATED == 201

# HTTP ステータスコードの種類
# 1XX - Informational
#    (レスポンスはボディを持たない)
# - 100: Continue
# - 101: Switching Protocols
# 2XX - Success (リクエストが成功した場合)
# - 200: OK
# - 201: Created
# - 202: Accepted
# 3XX - Redirection 
#   (リクエストを完了するために追加の処理が必要)
# 4XX - Client Error
#   (リクエストに誤りがある場合)
# - 400: Bad Request
# - 401: Unauthorized
# - 403: Forbidden
# - 404: Not Found
# 5XX - Server Error
#   (サーバーがリクエストを処理できない場合)
# - 500: Internal Server Error
