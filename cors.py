# Origin = スキーム(http[s]) + ドメイン(FQDN) + ポート番号 のこと
# ブラウザ機能により、異なる Origin 間のリソースのアクセスは禁止される。(Same-Origin Policy)

# CORS : Cross-Origin Resource Sharing
# SOP を回避し、異なるオリジンからのアクセスを許可するための機能
# レスポンスで Access-Control-Allow-Origin ヘッダを返すことで、指定したオリジンへのアクセスを許可する
# FastAPI においては、バックエンドで「許可されるオリジン」のリストを設定すればよい。

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 指定したオリジンからのアクセスを許可する
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

# CORS 機能は middleware として提供されている
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 許可するオリジンのリスト
    allow_credentials=True,  # Cookie の送信を許可
    allow_methods=["*"],  # 許可する HTTP メソッド
    allow_headers=["*"],  # 許可する HTTP ヘッダ
)


@app.get("/")
async def main():
    return {"message": "Hello World"}
