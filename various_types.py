from datetime import datetime, time, timedelta
from typing import Union
from uuid import UUID
from decimal import Decimal

from fastapi import Body, FastAPI

app = FastAPI()


@app.put("/items/{item_id}")
async def read_items(
    item_id: UUID,
    start_datetime: datetime = Body(),  # ISO 8601 形式の日時文字列 (例: "2020-12-25T10:15:00")
    end_datetime: datetime = Body(),
    process_after: timedelta = Body(),  # ISO 8601 形式の時間文字列 (例: "10:15:00")
    repeat_at: Union[time, None] = Body(default=None),
    data: bytes = Body(
        ...
    ),  # リクエスト/レスポンスでは str として扱われるバイナリデータ
    unique_values: frozenset = Body(...),  # キーの重複がないことを保証する set
    amount: Decimal = Body(...),  # 金額などの精度が必要な数値
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "process_after": process_after,
        "repeat_at": repeat_at,
        "start_process": start_process,
        "duration": duration,
        "data": data,
        "unique_values": unique_values,
        "amount": amount,
    }
