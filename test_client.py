# FastAPI では httpx をベースとして、 pytest を利用したテストを実装できる。
# httpx : HTTP client for Python

from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


@app.get("/")
async def read_main():
    return {"msg": "Hello World"}


# TestClient は httpx 由来。
client = TestClient(app)


# テストは同期関数として実装する。
# (pytest は通常は同期関数のみテスト可能。非同期関数のテストには別途プラグインが必要。)
def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}
