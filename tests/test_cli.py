from unittest.mock import patch, Mock
import cli

@patch("cli.requests.get")
def test_view_all_inventory(mock_get, capsys):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [
        {
            "id": 1,
            "name": "Test Milk",
            "quantity": 10,
            "price": 300
        }
    ]
    mock_get.return_value = mock_response
    cli.view_all_inventory()
    output = capsys.readouterr().out
    assert "Test Milk" in output
    assert "Quantity: 10" in output

@patch("cli.requests.get")
@patch("builtins.input", return_value="1")
def test_view_one_item(mock_input, mock_get, capsys):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "id": 1,
        "name": "Test Milk",
        "barcode": "555555555",
        "brand": "Test Brand",
        "ingredients": "Milk",
        "price": 300,
        "quantity": 10
    }
    mock_get.return_value = mock_response
    cli.view_one_item()
    output = capsys.readouterr().out
    assert "Test Milk" in output
    assert "Test Brand" in output

@patch("cli.requests.post")
@patch(
    "builtins.input",
    side_effect=[
        "Test Bread",
        "555555555",
        "Test Brand",
        "Flour, water",
        "200",
        "5"
    ]
)
def test_add_inventory_item(mock_input, mock_post, capsys):
    mock_response = Mock()
    mock_response.json.return_value = {
        "message": "Inventory item added successfully"
    }
    mock_post.return_value = mock_response
    cli.add_inventory_item()
    mock_post.assert_called_once()
    output = capsys.readouterr().out
    assert "Inventory item added successfully" in output

@patch("cli.requests.patch")
@patch(
    "builtins.input",
    side_effect=[
        "1",
        "Updated Milk",
        "",
        "",
        "",
        "350",
        "20"
    ]
)
def test_update_inventory_item(mock_input, mock_patch, capsys):
    mock_response = Mock()
    mock_response.json.return_value = {
        "message": "Inventory item updated successfully"
    }
    mock_patch.return_value = mock_response
    cli.update_inventory_item()
    mock_patch.assert_called_once()
    output = capsys.readouterr().out
    assert "Inventory item updated successfully" in output

@patch("cli.requests.delete")
@patch("builtins.input", return_value="1")
def test_delete_inventory_item(mock_input, mock_delete, capsys):
    mock_response = Mock()
    mock_response.json.return_value = {
        "message": "Inventory item deleted successfully"
    }
    mock_delete.return_value = mock_response
    cli.delete_inventory_item()
    mock_delete.assert_called_once()
    output = capsys.readouterr().out
    assert "Inventory item deleted successfully" in output

@patch("cli.requests.get")
@patch("builtins.input", return_value="3017624010701")
def test_find_openfoodfacts_product(mock_input, mock_get, capsys):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "name": "Test Chocolate",
        "barcode": "3017624010701",
        "brand": "Test Brand",
        "category": "Chocolate",
        "ingredients": "Cocoa, sugar"
    }

    mock_get.return_value = mock_response
    cli.find_openfoodfacts_product()
    output = capsys.readouterr().out
    assert "Test Chocolate" in output
    assert "Test Brand" in output

@patch("cli.requests.post")
@patch(
    "builtins.input",
    side_effect=[
        "3017624010701",
        "650",
        "10"
    ]
)
def test_add_openfoodfacts_product(mock_input, mock_post, capsys):
    mock_response = Mock()
    mock_response.json.return_value = {
        "message": (
            "Product fetched from OpenFoodFacts "
            "and added to inventory"
        )
    }
    mock_post.return_value = mock_response
    cli.add_openfoodfacts_product()
    mock_post.assert_called_once()
    output = capsys.readouterr().out
    assert "Product fetched from OpenFoodFacts" in output