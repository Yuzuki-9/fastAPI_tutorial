from enum import Enum
from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Optional, List

# Enumの定義
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

app = FastAPI()

# first step
@app.get("/")
async def root():
    return {"message": "Hello World"}


# パスパラメーター
@app.get("/items/{item_id}")
async def read_item(item_id: int):  # item_idをint型で定義
    return {"item_id": item_id}

# 順序の問題（path operationsは順に評価される）
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}

# 定義済みの値
# パスパラメータを受け取るpath operationをもち、有効なパスパラメータの値を事前に定義したい場合は、標準のPython Enumを利用できる
# Enumクラスの作成
@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {"model_name": model_name, "messeage": "Deep Learning FTW!"}
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}

# クエリパラメータ
# fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]
# @app.get("/items/")
# async def read_item(skip: int = 0, limit: int = 10):
#     return fake_items_db[skip: skip + limit]

# クエリパラメータの型変換
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: Optional[str] = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

# 複数のパスパラメータとクエリパラメータ
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: Optional[str] = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item

# リクエストボディ
# データモデルの作成
class Item(BaseModel):
    name: str
    description: Optional[str] = None  # オプショナルな属性（nullでも良い）
    price: float
    tax: Optional[float] = None  # オプショナルな属性（nullでも良い）

# モデルの使用
# @app.post("/items/")
# async def create_item(item: Item):
#     item_dict = item.dict()
#     if item.tax:
#         price_with_tax = item.price + item.tax
#         item_dict.update({"price_with_tax": price_with_tax})
#     return item_dict

# リクエストボディ + パスパラメータ
@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}

# リクエストボディ + パスパラメータ + クエリパラメータ
@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item, q: Optional[str] = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result

# クエリパラメータと文字列の検証
# バリデーション・正規表現
# @app.get("/items/")
# async def read_items(
#     q: Optional[str] = Query(None, min_length=3, max_length=50, regex="^fixedquery$")  # 必須にするには「None」→「...」
# ):
#     results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
#     if q:
#         results.update({"q":q})
#     return results

# URL内に複数回出現するクエリパラメータqを宣言
# URL：http://localhost:8000/items/?q=foo&q=bar
# @app.get("/items/")
# async def read_items(q: Optional[List[str]] = Query(None)):
#     query_items = {"q": q}
#     return query_items

