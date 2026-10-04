import requests

def get_product_from_openfoodfacts(barcode):
    url = f"https://world.openfoodfacts.org/api/v2/product/{barcode}"
    headers = {"User-Agent": "InventoryManagementSystem/1.0"}
    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )
        if response.status_code != 200:
            return None
        data = response.json()
        if data.get("status") != 1:
            return None
        product = data.get("product", {})
        return {
            "name": product.get("product_name")
                    or product.get("generic_name")
                    or "Unknown",
            "barcode": product.get("code", barcode),
            "brand": product.get("brands") or "Unknown",
            "category": product.get("categories") or "Unknown",
            "ingredients": product.get("ingredients_text")
                            or "Unknown"
        }
    except requests.RequestException as error:
        print("OpenFoodFacts error:", error)
        return None