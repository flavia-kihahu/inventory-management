import pytest
from unittest.mock import patch, Mock
from app import app, inventory

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def reset_inventory():
    original_inventory = inventory.copy()
    yield
    inventory.clear()
    inventory.extend(original_inventory)

def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.get_json()["message"] == "Inventory Management API"

def test_get_all_inventory(client):
    response = client.get("/inventory")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_get_inventory_item(client):
    response = client.get("/inventory/1")
    assert response.status_code == 200
    assert response.get_json()["id"] == 1

def test_get_inventory_item_not_found(client):
    response = client.get("/inventory/999")
    assert response.status_code == 404
    assert "error" in response.get_json()

def test_add_inventory_item(client):
    new_item = {
        "name": "Test Cereal",
        "barcode": "111111111",
        "brand": "Test Brand",
        "ingredients": "Oats, sugar",
        "price": 200,
        "quantity": 5
    }
    response = client.post(
        "/inventory",
        json=new_item
    )
    assert response.status_code == 201
    assert response.get_json()["item"]["name"] == "Test Cereal"

def test_add_inventory_missing_field(client):
    new_item = {
        "name": "Test Cereal",
        "barcode": "111111111"
    }
    response = client.post(
        "/inventory",
        json=new_item
    )
    assert response.status_code == 400
    assert "error" in response.get_json()

def test_update_inventory_item(client):
    response = client.patch(
        "/inventory/1",
        json={
            "price": 400,
            "quantity": 30
        }
    )
    assert response.status_code == 200
    assert response.get_json()["item"]["price"] == 400
    assert response.get_json()["item"]["quantity"] == 30

def test_update_inventory_item_not_found(client):
    response = client.patch(
        "/inventory/999",
        json={
            "price": 400
        }
    )
    assert response.status_code == 404

def test_delete_inventory_item(client):
    response = client.delete("/inventory/1")
    assert response.status_code == 200
    assert response.get_json()["message"] == (
        "Inventory item deleted successfully"
    )

def test_delete_inventory_item_not_found(client):
    response = client.delete("/inventory/999")
    assert response.status_code == 404
@patch("app.get_product_from_openfoodfacts")
def test_find_openfoodfacts_product(mock_product, client):
    mock_product.return_value = {
        "name": "Test Chocolate",
        "barcode": "555555555",
        "brand": "Test Brand",
        "category": "Chocolate",
        "ingredients": "Cocoa, sugar"
    }
    response = client.get("/products/555555555")
    assert response.status_code == 200
    assert response.get_json()["name"] == "Test Chocolate"

@patch("app.get_product_from_openfoodfacts")
def test_find_openfoodfacts_product_not_found(mock_product, client):
    mock_product.return_value = None
    response = client.get("/products/999999999")
    assert response.status_code == 404

@patch("app.get_product_from_openfoodfacts")
def test_add_product_from_api(mock_product, client):
    mock_product.return_value = {
        "name": "Test Chocolate",
        "barcode": "555555555",
        "brand": "Test Brand",
        "category": "Chocolate",
        "ingredients": "Cocoa, sugar"
    }
    response = client.post(
        "/inventory/from-api/555555555",
        json={
            "price": 500,
            "quantity": 10
        }
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["item"]["name"] == "Test Chocolate"
    assert data["item"]["price"] == 500
    assert data["item"]["quantity"] == 10

@patch("app.get_product_from_openfoodfacts")
def test_add_product_from_api_missing_price(mock_product, client):
    mock_product.return_value = {
        "name": "Test Chocolate",
        "barcode": "555555555",
        "brand": "Test Brand",
        "category": "Chocolate",
        "ingredients": "Cocoa, sugar"
    }
    response = client.post(
        "/inventory/from-api/555555555",
        json={
            "quantity": 10
        }
    )
    assert response.status_code == 400