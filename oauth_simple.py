from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

# OAuth2PasswordBearer を使ったセキュリティシステムの概観
# このサンプルでは トークンの生成/検証を行っていない

# OAuth のパスワードフローでは
# `username` と `password` の２つを、
# fomr-data として送信する必要がある

# オプションで `Scope` フィールドで任意の文字列を指定できる
# e.g., `users:read` などセキュリティ権限を表す文字列`


# API で公開されるユーザーモデル
class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


# DB に格納されるユーザーモデル
# (User + hashed_password)
class UserInDB(User):
    hashed_password: str


# DB に格納されるユーザー情報
# password はハッシュ化して格納する必要がある
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

app = FastAPI()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def fake_hash_password(password: str):
    return "fakehashed" + password


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)  # dict -> class に変換


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},  # 401 エラーで必須のヘッダ
        )
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


# OAuth2 パスワードフローのエンドポイント
@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    # 本当は JWT トークンを返すべきだが、仮実装で username を返す
    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user
