import requests
BASE_URL = "http://127.0.0.1:5000"

def view_all_inventory():
    response = requests.get(f"{BASE_URL}/inventory")
    if response.status_code == 200:
        items = response.json()
        print("\n--- Inventory ---")
        for item in items:
            print(
                f"ID: {item['id']} | "
                f"Name: {item['name']} | "
                f"Quantity: {item['quantity']} | "
                f"Price: {item['price']}"
            )
    else:
        print("Error:", response.json())
def view_one_item():
    item_id = input("Enter inventory ID: ")
    response = requests.get(
        f"{BASE_URL}/inventory/{item_id}"
    )
    if response.status_code == 200:
        item = response.json()
        print("\n--- Inventory Item ---")
        print(f"ID: {item['id']}")
        print(f"Name: {item['name']}")
        print(f"Barcode: {item['barcode']}")
        print(f"Brand: {item['brand']}")
        print(f"Ingredients: {item['ingredients']}")
        print(f"Price: {item['price']}")
        print(f"Quantity: {item['quantity']}")
    else:
        print("Error:", response.json())
def add_inventory_item():
    print("\n--- Add Inventory Item ---")
    data = {
        "name": input("Name: "),
        "barcode": input("Barcode: "),
        "brand": input("Brand: "),
        "ingredients": input("Ingredients: "),
        "price": float(input("Price: ")),
        "quantity": int(input("Quantity: "))
    }
    response = requests.post(
        f"{BASE_URL}/inventory",
        json=data
    )
    print(response.json())
def update_inventory_item():
    item_id = input("Enter inventory ID to update: ")
    print("Leave a field empty if you don't want to change it.")
    data = {}
    name = input("New name: ")
    barcode = input("New barcode: ")
    brand = input("New brand: ")
    ingredients = input("New ingredients: ")
    price = input("New price: ")
    quantity = input("New quantity: ")
    if name:
        data["name"] = name
    if barcode:
        data["barcode"] = barcode
    if brand:
        data["brand"] = brand
    if ingredients:
        data["ingredients"] = ingredients
    if price:
        data["price"] = float(price)
    if quantity:
        data["quantity"] = int(quantity)
    response = requests.patch(
        f"{BASE_URL}/inventory/{item_id}",
        json=data
    )
    print(response.json())
def delete_inventory_item():
    item_id = input("Enter inventory ID to delete: ")
    response = requests.delete(
        f"{BASE_URL}/inventory/{item_id}"
    )
    print(response.json())
def find_openfoodfacts_product():
    barcode = input("Enter product barcode: ")
    response = requests.get(
        f"{BASE_URL}/products/{barcode}"
    )
    if response.status_code == 200:
        product = response.json()
        print("\n--- OpenFoodFacts Product ---")
        print(f"Name: {product['name']}")
        print(f"Barcode: {product['barcode']}")
        print(f"Brand: {product['brand']}")
        print(f"Category: {product['category']}")
        print(f"Ingredients: {product['ingredients']}")
    else:
        print("Error:", response.json())
def add_openfoodfacts_product():
    barcode = input("Enter product barcode: ")
    price = float(input("Enter price: "))
    quantity = int(input("Enter quantity: "))
    data = {
        "price": price,
        "quantity": quantity
    }
    response = requests.post(
        f"{BASE_URL}/inventory/from-api/{barcode}",
        json=data
    )
    print(response.json())
def show_menu():
    print("\n==============================")
    print(" Inventory Management System")
    print("==============================")
    print("1. View all inventory")
    print("2. View one item")
    print("3. Add inventory item")
    print("4. Update inventory item")
    print("5. Delete inventory item")
    print("6. Find product on OpenFoodFacts")
    print("7. Add product from OpenFoodFacts")
    print("8. Exit")
def main():
    while True:
        show_menu()
        choice = input("\nChoose an option: ")
        if choice == "1":
            view_all_inventory()
        elif choice == "2":
            view_one_item()
        elif choice == "3":
            add_inventory_item()
        elif choice == "4":
            update_inventory_item()
        elif choice == "5":
            delete_inventory_item()
        elif choice == "6":
            find_openfoodfacts_product()
        elif choice == "7":
            add_openfoodfacts_product()
        elif choice == "8":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
if __name__ == "__main__":
    main()