# HTTP レスポンスを返した後に実行する処理を定義できる


def DBSession():
    pass


# path operation から呼ばれる関数
async def get_db():
    db = DBSession()
    try:
        yield db
        # ここで path operation に戻る
    finally:
        # yield 以降のコードは、レスポンス送信後に実行される
        db.close()


from fastapi import Depends


# yiled を持つ文を Depends() に追加し、依存ツリーを構築する


async def dependency_a():
    dep_a = None  # Something
    try:
        yield dep_a
    finally:
        dep_a.close()


async def dependency_b(dep_a=Depends(dependency_a)):
    dep_b = None  # Something
    try:
        yield dep_b
    finally:
        dep_b.close(dep_a)


async def dependency_c(dep_b=Depends(dependency_b)):
    dep_c = None  # Something
    try:
        yield dep_c
    finally:
        dep_c.close(dep_b)


# あるいは コンテキストマネージャ (with) を使っても終了処理を実装できる


class MySuperContextManager:
    def __init__(self):
        self.db = DBSession()

    def __enter__(self):
        return self.db

    def __exit__(self, exc_type, exc_value, traceback):
        self.db.close()


async def get_db():
    with MySuperContextManager() as db:
        yield db
