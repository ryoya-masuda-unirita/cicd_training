from fastapi import FastAPI, HTTPException
from typing import List, Dict
from .models import Item

app = FastAPI(title="CI/CD Learning API")

# インメモリデータストア
items: Dict[int, Item] = {}
current_id: int = 0


@app.get("/health")
def health_check():
    """ヘルスチェックエンドポイント"""
    return {"status": "healthy"}


@app.get("/items", response_model=List[Item])
def get_items():
    """全アイテムを取得"""
    return list(items.values())


@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    """指定されたIDのアイテムを取得"""
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]


@app.post("/items", response_model=Item)
def create_item(item: Item):
    """新しいアイテムを作成"""
    global current_id
    current_id += 1
    item.id = current_id
    items[current_id] = item
    return item 