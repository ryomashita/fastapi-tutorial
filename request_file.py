from typing import Annotated

from fastapi import FastAPI, File, UploadFile

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
    read_file = await file.read(10000)
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "read_file": read_file.__sizeof__(),
    }
