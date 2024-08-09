from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()

# FastAPI で OAuth2 Bearer 認証を実装するための手順
# tokenUrl : username/password を送信して token を取得するための URL (の相対パス)
# oauth2_scheme : 認証情報を取得するための関数オブジェクト
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/items/")
# Depends() で依存関係を渡すことで、 oatuh2_scheme の認証処理が実行される
# = HTTPヘッダー `Authorization` を探し、 `Bearer` トークンを取得し検証する。
# HTTPヘッダーが無い/不正なトークンには 401 Unauthorized エラーを返す
async def read_items(token: str = Depends(oauth2_scheme)):
    return {"token": token}
