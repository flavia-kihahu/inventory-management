from flask import Flask, jsonify, request
import requests

app = Flask(__name__)
inventory = [
    {
        "id": 1,
        "name": "Organic Almond Milk",
        "barcode": "123456789",
        "brand": "Silk",
        "ingredients": "Filtered water, almonds, cane sugar",
        "price": 350.00,
        "quantity": 20
    },
    {
        "id": 2,
        "name": "Whole Wheat Bread",
        "barcode": "987654321",
        "brand": "Sunshine",
        "ingredients": "Whole wheat flour, water, yeast, salt",
        "price": 120.00,
        "quantity": 15
    }
]

def get_product_from_openfoodfacts(barcode):
    url = f"https://world.openfoodfacts.org/api/v3/product/{barcode}"
    headers = {"User-Agent": "InventoryManagementSystem/1.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return None
        data = response.json()
        if data.get("status") != 1:
            return None
        product = data.get("product", {})
        return {
            "name": product.get("product_name", "Unknown"),
            "brand": product.get("brands", "Unknown"),
            "barcode": barcode,
            "category": product.get("categories", "Unknown"),
            "ingredients": product.get(
                "ingredients_text",
                "Unknown"
            )
        }
    except requests.RequestException:
        return None
@app.route('/')
def home():
    return jsonify({
        "message": "Inventory Management API"
    })

@app.route("/inventory", methods=["GET"])
def get_inventory():
    return jsonify(inventory)

@app.route("/inventory/<int:id>", methods=["GET"])
def get_inventory_by_id(id):
    for item in inventory:
        if item["id"] == id:
            return jsonify(item), 200
        return jsonify({"error": "Inventory item not found"}), 404

@app.route("/inventory", methods=["POST"])
def add_inventory():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    required_fields = ["name", "barcode", "brand", "ingredients", "price", "quantity"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing field: {field}"}), 400
    new_id = max([item["id"] for item in inventory], default=0) + 1
    new_item = {
        "id": new_id,
        "name": data["name"],
        "barcode": data["barcode"],
        "brand": data["brand"],
        "ingredients": data["ingredients"],
        "price": data["price"],
        "quantity": data["quantity"]
    }
    inventory.append(new_item)
    return jsonify({
        "message": "Inventory item added successfully", 
        "item": new_item}), 201

@app.route("/inventory/<int:item_id>", methods=["PATCH"])
def update_inventory_item(item_id):
    data = request.get_json()
    if not data:
        return jsonify({
            "error": "Request body must contain JSON data"
        }), 400
    for item in inventory:
        if item["id"] == item_id:
            allowed_fields = [
                "name",
                "barcode",
                "brand",
                "ingredients",
                "price",
                "quantity"
            ]
            for field in allowed_fields:
                if field in data:
                    item[field] = data[field]
            return jsonify({
                "message": "Inventory item updated successfully",
                "item": item
            }), 200
    return jsonify({
        "error": "Inventory item not found"
    }), 404

@app.route("/inventory/<int:item_id>", methods=["DELETE"])
def delete_inventory_item(item_id):
    for item in inventory:
        if item["id"] == item_id:
            inventory.remove(item)

            return jsonify({
                "message": "Inventory item deleted successfully"
            }), 200
    return jsonify({
        "error": "Inventory item not found"
    }), 404

@app.route("/products/<barcode>", methods=["GET"])
def find_product(barcode):
    product = get_product_from_openfoodfacts(barcode)
    if product is None:
        return jsonify({
            "error": "Product not found or OpenFoodFacts API unavailable"
        }), 404
    return jsonify(product), 200

if __name__ == '__main__':
    app.run(debug=True)