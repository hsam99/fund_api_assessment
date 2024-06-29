"""Test the service layer."""
import pytest

from funds_api.services import exceptions, services


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


def test_add_fund():
    """Test adding a fund."""
    db = FakeDb()
    new_fund = {
        "id": 412, 
        "name": "Balanced Fund", 
        "manager_name": "Carol Williams", 
        "description": "A fund balancing between growth and income.", 
        "nav": 110.50, 
        "date": "2020-02-20", 
        "performance": 9.3
    }

    added_fund = services.add_fund(db, new_fund)
    assert added_fund == 412
    assert 412 in db._data


def test_add_fund_empty_data():
    """Add an empty fund."""
    db = FakeDb()
    new_fund = {}
    with pytest.raises(exceptions.InvalidInputError):
        services.add_fund(db, new_fund)


def test_add_fund_incomplete_data():
    """Add a new fund data that does not follow the model's schema attributes."""
    db = FakeDb()
    new_fund = {
        "id": 412, 
        "name": "Balanced Fund", 
    }
    with pytest.raises(exceptions.InvalidInputError):
        services.add_fund(db, new_fund)


def test_add_fund_invalid_data_type():
    """Add a new fund data that does not follow the model's schema data type."""
    db = FakeDb()
    new_fund = {
        "id": '412', 
        "name": 123, 
        "manager_name": "Carol Williams", 
        "description": "A fund balancing between growth and income.", 
        "nav": 110.50, 
        "date": "2020-02-20", 
        "performance": '9.3'
    }

    with pytest.raises(exceptions.InvalidInputError):
        services.add_fund(db, new_fund)


def test_add_fund_duplicated_id():
    """Add a new fund data where the fund id already exists."""
    db = FakeDb()
    new_fund = {
        "id": 1001, 
        "name": "Balanced Fund", 
        "manager_name": "Carol Williams", 
        "description": "A fund balancing between growth and income.", 
        "nav": 110.50, 
        "date": "2020-02-20", 
        "performance": 9.3
    }

    with pytest.raises(exceptions.InvalidInputError):
        services.add_fund(db, new_fund)


def test_get_fund():
    """Test get fund by id."""
    db = FakeDb()
    expected_result = {
        "id": 3210,
        "name": "Income Fund",
        "manager_name": "Bob Smith",
        "description": "A fund aiming to provide steady income through dividends.",
        "nav": 95.75,
        "date": "2019-08-15",
        "performance": 7.8
    }
    assert services.get_fund(db, 3210) == expected_result


def test_get_fund_non_existent_id():
    """Test get fund by providing a non-existent id."""
    db = FakeDb()
    with pytest.raises(exceptions.NotFoundError):
        services.get_fund(db, 1)


def test_get_fund_invalid_id_type():
    """Test get fund by providing a string id."""
    db = FakeDb()
    with pytest.raises(exceptions.NotFoundError):
        services.get_fund(db, '3210')


def test_update_performance():
    """Test update performance."""
    db = FakeDb()
    update_value = {"performance": 7.869}
    expected_result = {
        "id": 3210,
        "name": "Income Fund",
        "manager_name": "Bob Smith",
        "description": "A fund aiming to provide steady income through dividends.",
        "nav": 95.75,
        "date": "2019-08-15",
        "performance": 7.869
    }
    # Check performance value before update.
    assert db._data[3210]['performance'] == 7.8

    result = services.update_performance(db, 3210, update_value)
    assert result == expected_result
    # Check performance value after update.
    assert db._data[3210]['performance'] == 7.869


def test_update_performance_non_existent_id():
    """Test updating a non-existent fund."""
    db = FakeDb()
    update_value = {'performance': 7.869}
    with pytest.raises(exceptions.NotFoundError):
        services.update_performance(db, 1, update_value)


def test_update_performance_invalid_input():
    """Test update performance with invalid inputs."""
    db = FakeDb()
    wrong_inputs = [
        {},
        {'performance': 7.869, 'name': 'John Doe'},
        {'name': 7.869}
    ]

    for input in wrong_inputs:
        with pytest.raises(exceptions.InvalidInputError):
            services.update_performance(db, 3210, input)


def test_update_performance_invalid_performance_data():
    """Test update performance with invalid performance data type."""
    db = FakeDb()
    update_value = {'performance': '1.2345'}

    with pytest.raises(exceptions.InvalidInputError):
        services.update_performance(db, 3210, update_value)


def test_delete_fund():
    """Test delete fund."""
    db = FakeDb()
    fund_id = 3210
    # Check fund exists before delete.
    assert fund_id in db._data

    result = services.delete_fund(db, fund_id)
    assert result == ''
    # Check fund exists after delete.
    assert fund_id not in db._data


def test_delete_fund_invalid_id_type():
    """Test delete fund by providing a string id."""
    db = FakeDb()
    fund_id = '3210'

    with pytest.raises(exceptions.NotFoundError):
        services.delete_fund(db, fund_id)


def test_delete_fund_non_existent_id():
    """Test delete a non-existent fund."""
    db = FakeDb()
    fund_id = 1

    with pytest.raises(exceptions.NotFoundError):
        services.delete_fund(db, fund_id)


def test_combined_services():
    """Test integrated service functions."""
    db = FakeDb()
    new_fund = {
        "id": 412, 
        "name": "Balanced Fund", 
        "manager_name": "Carol Williams", 
        "description": "A fund balancing between growth and income.", 
        "nav": 110.50, 
        "date": "2020-02-20", 
        "performance": 9.3
    }

    _ = services.add_fund(db, new_fund)

    # Test get fund after adding fund.
    assert services.get_fund(db, 412) == new_fund

    new_performance = {'performance': 11.34}
    _ = services.update_performance(db, 412, new_performance)

    # Test get fund after updating fund.
    assert services.get_fund(db, 412) == {
        "id": 412, 
        "name": "Balanced Fund", 
        "manager_name": "Carol Williams", 
        "description": "A fund balancing between growth and income.", 
        "nav": 110.50, 
        "date": "2020-02-20", 
        "performance": 11.34
    }

    _ = services.delete_fund(db, 412)
    # Test get fund after deleting fund.
    with pytest.raises(exceptions.NotFoundError):
        services.get_fund(db, 412)
