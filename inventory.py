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
def get_next_id():
    return max(
        [item["id"] for item in inventory],
        default=0
    ) + 1