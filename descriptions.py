# FastAPI() 生成時に ドキュメントの説明を追加できる
from fastapi import FastAPI

# description には Markdown が使える
description = """
ChimichangApp API helps you do awesome stuff. 🚀

## Items

You can **read items**.

## Users

You will be able to:

* **Create users** (_not implemented_).
* **Read users** (_not implemented_).
"""

tags_metadata = [
    {
        "name": "users",  # `name` は path operations, APIRouter でも定義できる
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "items",
        "description": "Manage items. So _fancy_ they have their own docs.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]

app = FastAPI(
    title="ChimichangApp",
    description=description,
    summary="Deadpool's favorite app. Nuff said.",
    version="0.0.1",
    openapi_tags=tags_metadata,
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Deadpoolio the Amazing",
        "url": "http://x-force.example.com/contact/",
        "email": "dp@x-force.example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    openapi_url="/api/v1/openapi.json",  # /openapi.json のURLを変更
    docs_url="/api/v1/docs",  # Swagger UI (/docs) のURLを変更
    redoc_url="/api/v1/redoc",  # ReDoc (/redoc) のURLを変更
)


@app.get("/items/")
async def read_items():
    return [{"name": "Katana"}]
