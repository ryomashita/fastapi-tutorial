from fastapi import FastAPI

# run with: 
#   poetry run uvicorn main:my_app --reload
#   - main: the file name (main.py)
#   - app: the FastAPI instance
#   - --reload: auto-reload the server when the file changes

my_app = FastAPI()

@my_app.get("/") # operation decorator + path
async def my_root():
    # define response(cocntent)
    return {"message": "Hello World"}

@my_app.get("/items/{item_id}") # path parameter
async def read_item(item_id: int):
    # FastAPI は Python型宣言によりvalidationを行う
    # "/items/4.2" へのアクセスはエラーレスポンスが返る
    return {"item_id": item_id}
