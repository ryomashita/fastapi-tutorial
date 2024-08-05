from typing import Annotated

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import HTMLResponse

app = FastAPI()

# ファイルを含むリクエストを受け取る場合
# (注) リクエストボディは `multipart/form-data` となるため、JSON他は同時に送信できない
# ファイル引数には `bytes` または `fastapi.UploadFile` のいずれかを指定する（`UploadFile` の方が多機能）


# Annotated : 型ヒントにメタデータを追加する
# [bytes, File()] : bytes型 かつ File() であることを示す
# bytes の場合、ファイルの全データがメモリに読み込まれる
@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(
    # UploadFile でも Annotated でメタデータを追加できる
    # file: UploadFile = File(...) # とすることも可能
    file: Annotated[UploadFile, File(description="A file read as UploadFile")],
):
    # await : 非同期処理(async)の終了を待機する
    read_file = await file.read(10000)
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "read_file": read_file.__sizeof__(),
    }


# 複数ファイルを受け取る場合 : list[UploadFile]
@app.post("/uploadfiles/")
async def create_upload_files(files: list[UploadFile]):
    return {"filenames": [file.filename for file in files]}


# Form としてファイルを受け取る場合
@app.post("/files/new/")
async def create_file_with_form(
    file: bytes = File(), fileb: UploadFile = File(), token: str = Form()
):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }


# ファイルを送信する HTML フォーム例
@app.get("/")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)
