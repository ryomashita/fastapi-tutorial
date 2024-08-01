from typing import Union, List

from fastapi import FastAPI, Header

app = FastAPI()


@app.get("/items/")
async def read_items(
    user_agent: Union[str, None] = Header(default=None),
    # ヘッダ名は重複する可能性がある。正常に処理するためにはリストで受け取る
    x_token: Union[List[str], None] = Header(default=None),
):
    # HTTPヘッダーは '-' 区切り & 大文字・小文字の区別がないため、
    # `user_agent` は `User-Agent` を受け取る
    return {"User-Agent": user_agent, "X-Token values": x_token}
