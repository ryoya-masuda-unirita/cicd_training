from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """ヘルスチェックエンドポイントのテスト"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_create_item():
    """アイテム作成エンドポイントのテスト"""
    item_data = {
        "name": "Test Item",
        "description": "This is a test item",
        "price": 10.5
    }
    response = client.post("/items", json=item_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == item_data["name"]
    assert data["description"] == item_data["description"]
    assert data["price"] == item_data["price"]
    assert "id" in data

def test_get_items():
    """アイテム一覧取得エンドポイントのテスト"""
    response = client.get("/items")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_item():
    """個別アイテム取得エンドポイントのテスト"""
    # まず新しいアイテムを作成
    item_data = {
        "name": "Test Item for Get",
        "description": "This is a test item for get",
        "price": 15.5
    }
    create_response = client.post("/items", json=item_data)
    created_item = create_response.json()
    item_id = created_item["id"]

    # 作成したアイテムを取得
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == item_data["name"]
    assert data["description"] == item_data["description"]
    assert data["price"] == item_data["price"]

def test_get_non_existent_item():
    """存在しないアイテムの取得テスト"""
    response = client.get("/items/9999")
    assert response.status_code == 404 