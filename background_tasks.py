# BackgounrdTasks : レスポンスを返した後に実行するタスクを定義する

from typing import Union
from fastapi import BackgroundTasks, FastAPI, Depends

app = FastAPI()


def write_notification(email: str, message=""):
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)


@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    # BackgroundTasks オブジェクトに タスクを追加する
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}


def write_log(message: str):
    with open("log.txt", mode="a") as log:
        log.write(message)


def get_query(background_tasks: BackgroundTasks, q: Union[str, None] = None):
    if q:
        message = f"found query: {q}\n"
        background_tasks.add_task(write_log, message)
    return q


# Depends による依存関係の注入でも BackgroundTaks は機能する
@app.post("/send-notification/{email}")
async def send_notification_with_query(
    email: str, background_tasks: BackgroundTasks, q: str = Depends(get_query)
):
    message = f"message to {email}\n"
    background_tasks.add_task(write_log, message)
    return {"message": "Message sent"}
