"""Test the API."""
import pytest

from funds_api import create_app
from funds_api.bp import funds


class FakeDb:
    def __init__(self):
        self._data = {
            1001: {
                "id": 1001,
                "name": "Growth Fund",
                "manager_name": "Alice Johnson",
                "description": "A fund focusing on long-term growth investments.",
                "nav": 150.25,
                "date": "2021-05-01",
                "performance": 12.5
            },
            3210: {
                "id": 3210,
                "name": "Income Fund",
                "manager_name": "Bob Smith",
                "description": "A fund aiming to provide steady income through dividends.",
                "nav": 95.75,
                "date": "2019-08-15",
                "performance": 7.8
            },
        }

    def get_all_ids(self):
        return list(self._data.keys())

    def get_all(self):
        return list(self._data.values())

    def add_fund(self, fund_data):
        self._data[fund_data['id']] = fund_data

    def update_fund(self, id, data):
        self._data[id] = data

    def get_fund(self, id):
        return self._data.get(id)

    def delete_fund(self, id):
        if id not in self._data:
            print(f'Cannot find {id}, no entry deleted.')
            return

        del self._data[id]


# monkeypatched requests.get moved to a fixture
@pytest.fixture
def mock_db(monkeypatch):
    """Monkey patch blueprint module to use FakeDb instance instead of real database connection."""
    fake_db = FakeDb()
    def get_fake_db(*args, **kwargs):
        return fake_db

    monkeypatch.setattr(funds, "get_db", get_fake_db)
    return fake_db


@pytest.fixture()
def client():
    app = create_app()
    return app.test_client()


def test_get_all(client, mock_db):
    """Test the get all endpoint."""
    response = client.get('/funds')
    assert response.status_code == 200
    assert len(response.json) == 2


def test_get_single_fund(client, mock_db):
    """Test get single fund endpoint."""
    response = client.get('/funds/1001')
    assert response.status_code == 200
    assert sorted(response.json.items()) == sorted({
        "id": 1001,
        "name": "Growth Fund",
        "manager_name": "Alice Johnson",
        "description": "A fund focusing on long-term growth investments.",
        "nav": 150.25,
        "date": "2021-05-01",
        "performance": 12.5
    }.items())


def test_get_single_fund_not_found(client, mock_db):
    """Test get fund endpoint with non-existent id."""
    response = client.get('/funds/1')
    assert response.status_code == 404
    # Ensure the 'error' key is in the response.
    assert 'error' in response.json


def test_update_performance(client, mock_db):
    """Test update performance endpoint."""
    response = client.patch('/funds/1001', json={'performance': 22.5})
    assert response.status_code == 200
    assert sorted(response.json.items()) == sorted({
        "id": 1001,
        "name": "Growth Fund",
        "manager_name": "Alice Johnson",
        "description": "A fund focusing on long-term growth investments.",
        "nav": 150.25,
        "date": "2021-05-01",
        "performance": 22.5
    }.items())
    assert mock_db._data[1001]['performance'] == 22.5


def test_update_performance_invalid_input(client, mock_db):
    """Test update performance endpoint with invalid body input."""
    # Test performance as a string input.
    response = client.patch('/funds/1001', json={'performance': '22.5'})
    assert response.status_code == 400
    assert 'error' in response.json

    # Test body data has more than one entries.
    response = client.patch('/funds/1001', json={'performance': 22.5, 'name': 'test'})
    assert response.status_code == 400
    assert 'error' in response.json

    # Test body data does not have the 'performance' key.
    response = client.patch('/funds/1001', json={'name': 'test'})
    assert response.status_code == 400
    assert 'error' in response.json


def test_update_performance_fund_not_found(client, mock_db):
    """Test update performance endpoint with non existent fund."""
    response = client.patch('/funds/1', json={'performance': 22.5})
    assert response.status_code == 404
    assert 'error' in response.json


def test_create_new_fund(client, mock_db):
    """Test create new fund endpoint."""
    new_fund = {
        "id": 413,
        "name": "Balanced Fund",
        "manager_name": "Carol Williams",
        "description": "A fund balancing between growth and income.",
        "nav": 110.5,
        "date": "2020-02-20",
        "performance": 9.3
    }
    response = client.post('/funds', json=new_fund)
    assert response.status_code == 201
    assert response.json == 413
    # Checks whether the newly created fund is written in database.
    assert mock_db._data[413] == new_fund


def test_create_new_fund_with_duplicated_id(client, mock_db):
    """Test create new fund where id already exists in database."""
    new_fund = {
        "id": 1001,
        "name": "Balanced Fund",
        "manager_name": "Carol Williams",
        "description": "A fund balancing between growth and income.",
        "nav": 110.5,
        "date": "2020-02-20",
        "performance": 9.3
    }
    response = client.post('/funds', json=new_fund)
    assert response.status_code == 400
    assert 'error' in response.json
    assert len(mock_db._data) == 2


def test_create_new_fund_with_invalid_fund_data(client, mock_db):
    """Test create new fund where fund data is invalid."""
    # Data has attributes in wrong data types.
    new_fund = {
        "id": "413",
        "name": "Balanced Fund",
        "manager_name": "Carol Williams",
        "description": "A fund balancing between growth and income.",
        "nav": 110.5,
        "date": "2020-02-20",
        "performance": "9.3"
    }
    response = client.post('/funds', json=new_fund)
    assert response.status_code == 400
    assert 'error' in response.json
    assert len(mock_db._data) == 2

    # Data has incomplete attributes.
    new_fund = {
        "id": 413,
        "name": "Balanced Fund",
        "manager_name": "Carol Williams",
    }
    response = client.post('/funds', json=new_fund)
    assert response.status_code == 400
    assert 'error' in response.json
    assert len(mock_db._data) == 2


def test_delete_fund(client, mock_db):
    """Test delete fund endpoint."""
    response = client.delete('/funds/1001')
    assert response.status_code == 204
    assert 1001 not in mock_db._data


def test_delete_non_existent_fund(client, mock_db):
    """Test delete fund where fund id does not exist."""
    response = client.delete('/funds/413')
    assert response.status_code == 404
    assert 'error' in response.json
    