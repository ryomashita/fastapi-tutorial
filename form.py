from fastapi import FastAPI, Form

app = FastAPI()

# JSON の代わりに フォームデータを受け取る場合
# フォーム： HTML の <form> タグで送信されるデータ
# e.g., OAuth2 のパスワードフローでは フォームフィールドを使用する

@app.post("/login/")
async def login(username: str = Form(), password: str = Form()):
    return {"username": username}

# `POST` リクエストは HTML フォーム経由で送信されるケースが多い。
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods/POST

# フォームデータは基本的に以下の３種類
# `application/x-www-form-urlencoded``
#  - キーと値のペアを `&` で連結し、`=` でキーと値を結びつける
# `multipart/form-data` 
# - ファイルアップロードで使用される
# `text/plain`