# 静的なディレクトリ構造を、そのまま API で公開する方法
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# /static にアクセスすると、 static ディレクトリ内のファイルが返される
app.mount("/static", StaticFiles(directory="static"), name="static")
