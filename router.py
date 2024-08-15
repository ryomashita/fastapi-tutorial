# API Router : API を機能ごとに分割して実装するための機能
# python サブパッケージとして実装する

from fastapi import APIRouter, Depends, HTTPException

from dependencies import get_token_header

# main 側で以下のように router を利用する
# app.include_router(users.router)


router = APIRouter(
    prefix="/items",  # このパス以下を ルーティングする
    tags=["items"],
    dependencies=[Depends(get_token_header)],  # 全パス共通の依存関係
    responses={404: {"description": "Not found"}},  # 全パス共通のレスポンス
)


fake_items_db = {"plumbus": {"name": "Plumbus"}, "gun": {"name": "Portal Gun"}}


# path operation の実装方法は FastAPI と同じ
@router.get("/")  # "/items/" にアクセスされた場合に呼び出される
async def read_items():
    return fake_items_db


@router.get("/{item_id}")
async def read_item(item_id: str):
    if item_id not in fake_items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"name": fake_items_db[item_id]["name"], "item_id": item_id}


# APIRouter インスタンス時の設定を上書き可能
@router.put(
    "/{item_id}",
    tags=["custom"],
    responses={403: {"description": "Operation forbidden"}},
)
async def update_item(item_id: str):
    if item_id != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the item: plumbus"
        )
    return {"item_id": item_id, "name": "The great Plumbus"}
