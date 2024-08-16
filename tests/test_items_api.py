import requests
import pytest

BASE_URL = 'http://localhost:3001/api/item'
VALIDATE_URL = 'http://127.0.0.1:3001/api/validation/validate'

def add_item(name, description, mobile_number=None):
    response = requests.post(f'{BASE_URL}/add', json={
        'name': name,
        'description': description,
    })
    return response

def update_item(item_id, name, description, mobile_number=None):
    response = requests.put(f'{BASE_URL}/update', json={
        'id': item_id,
        'name': name,
        'description': description,
        'mobileNumber': mobile_number
    })
    return response

def delete_item(item_id):
    response = requests.delete(f'{BASE_URL}/delete', json={
        'id': item_id
    })
    return response

def get_all_items():
    response = requests.get(f'{BASE_URL}/items')
    return response

def test_add_item():
    response = add_item('Test Item', 'This is a test item')
    assert response.status_code == 201
    assert 'name' in response.json()
    assert 'description' in response.json()

def test_update_item():

    add_response = add_item('Update Test Item', 'This is an item to update')
    item_id = add_response.json().get('_id')

    update_response = update_item(item_id, 'Updated Item', 'Updated description')
    assert update_response.status_code == 200
    assert update_response.json().get('name') == 'Updated Item'

def test_delete_item():

    add_response = add_item('Delete Test Item', 'This is an item to delete')
    item_id = add_response.json().get('_id')

    delete_response = delete_item(item_id)
    assert delete_response.status_code == 200

    get_response = requests.get(f'{BASE_URL}/items')
    assert item_id not in [item['_id'] for item in get_response.json()]

def test_get_all_items():

    add_item('Get Test Item', 'This is an item to retrieve')
    response = get_all_items()
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_add_item_with_invalid_mobile_number():
    def mock_validate_phone_number(_):
        return {
            'isValid': False
        }

    global validatePhoneNumber
    validatePhoneNumber = mock_validate_phone_number
    response = add_item('Item with Invalid Phone Number', 'This should fail validation', '1234567890')
    assert response.status_code == 400
    assert response.json().get('error') == 'invalid number'
