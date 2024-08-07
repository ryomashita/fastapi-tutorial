from typing import Union

from fastapi import Depends, FastAPI, Cookie, Header, HTTPException

app = FastAPI()


# path operation のコードを共通化するため、
# Depends() による依存性注入が利用できる


# クエリ引数とそれに対する処理を共通化する
async def common_parameters(
    q: Union[str, None] = None, skip: int = 0, limit: int = 100
):
    # ここでは dict を返すが、JSON 互換型以外を返しても構わない
    return {"q": q, "skip": skip, "limit": limit}


@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters, use_cache=False)):
    return commons


@app.get("/users/")
async def read_users(commons: dict = Depends(common_parameters)):
    return commons


# Depends() の依存関係を階層化することも可能


def query_extractor(q: Union[str, None] = None):
    return q


def query_or_cookie_extractor(
    q: str = Depends(query_extractor),
    last_query: Union[str, None] = Cookie(default=None),
):
    if not q:
        return last_query
    return q


@app.get("/items/")
async def read_query(query_or_default: str = Depends(query_or_cookie_extractor)):
    return {"q_or_cookie": query_or_default}


# dependencies 引数に Depends() を指定することで、
# 返り値が無視できる & 複数の依存関係を指定できる


async def verify_token(x_token: str = Header()):
    if x_token != "fake-super-secret-token":
        # HTTPException 例外は伝播されるので、パスオペレータで呼び出す場合と同様に扱える
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: str = Header()):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key


@app.get("/items/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]
