from datetime import datetime
from typing import Union

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

fake_db = {}

# jsonable_encoder は Pydantic モデルの型を
# JSON 互換なPython標準型のいずれか (dict, list, ...) に変換する
#
# 直接JSONに変換できない型 (e.g., datetime型) でも、
# jsonable_encoderを使い、JSON互換型 (datetime -> str) に変換できる


class Item(BaseModel):
    title: str
    timestamp: datetime  # datetime型 は 直接 JSON に変換できない
    description: Union[str, None] = None


app = FastAPI()


@app.put("/items/{id}")
def update_item(id: str, item: Item):
    json_compatible_item_data = jsonable_encoder(item)
    fake_db[id] = json_compatible_item_data
