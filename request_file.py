from typing import Annotated

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse

app = FastAPI()

# ファイルを含むリクエストを受け取る場合

# Annotated : 型ヒントにメタデータを追加する
# [bytes, File()] : bytes型 かつ File() であることを示す
# bytes の場合、ファイルの全データがメモリに読み込まれる
@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}

# UploadFile : メモリへの読み込みに制限を設ける
# (制限を超えた分はファイルに保存される)
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    # await : 非同期処理(async)の終了を待機する
    read_file = await file.read(10000)
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "read_file": read_file.__sizeof__(),
    }

@app.post("/uploadfile/")
async def create_upload_file(
    # UploadFile でも Annotated でメタデータを追加できる
    file: Annotated[UploadFile, File(description="A file read as UploadFile")],
):
    return {"filename": file.filename}

# 複数ファイルを受け取る場合 : list[UploadFile]
@app.post("/uploadfiles/")
async def create_upload_files(files: list[UploadFile]):
    return {"filenames": [file.filename for file in files]}

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
