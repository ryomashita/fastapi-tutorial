from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import JSONResponse
from fastapi.responses import PlainTextResponse
from fastapi.exceptions import RequestValidationError

app = FastAPI()

# HTTP エラーステータス (e.g., 404) を返す場合は HTTPException を使用する
# 例外として実装される理由は「依存関係とセキュリティ」にある。

items = {"foo": "The Foo Wrestlers"}


@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found",  # detail : 任意のJSONエラーメッセージ
        )
    return {"item": items[item_id]}


# エラーレスポンスに カスタムヘッダー を追加する例
@app.get("/items-header/{item_id}")
async def read_item_header(item_id: str):
    if item_id not in items:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "There goes my error"},
        )
    return {"item": items[item_id]}


# -- 独自の例外を FastAPI で処理する場合は、exception_handler を使用する --


class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name


@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=status.HTTP_418_IM_A_TEAPOT,
        content={
            "message": f"Oops! {exc.name} did something. There goes a rainbow...",
            "details": exc.errors(),
            "body": exc.body,
        },
    )


@app.get("/unicorns/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}


# -- FastAPI デフォルトの例外処理をカスタマイズする --


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    # PlainTextResponse : テキストのみを含むレスポンスを返す
    # -> デフォルト(JSON) の代わりにテキストが返される
    return PlainTextResponse(str(exc), status_code=400)
