from jsonschema import validate, ValidationError

from . import exceptions


fund_schema = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "manager_name": {"type": "string"},
        "description": {"type": "string"},
        "nav": {"type": "number"},
        "date": {"type": "string"},
        "performance": {"type": "number"}
    },
    "required": ["id", "name", "manager_name", "description", "nav", "date", "performance"]
}


class Fund:
    def __init__(self, fund_data: dict):
        try:
            validate(fund_data, fund_schema)
        except ValidationError as error:
            raise exceptions.InvalidFundDataInput('Invalid fund input') from error
        else:
            self._id = fund_data['id']
            self._name = fund_data['name']
            self._manager_name = fund_data['manager_name']
            self._description = fund_data['description']
            self._nav = fund_data['nav']
            self._date = fund_data['date']
            self._performance = fund_data['performance']

    @property
    def details(self) -> dict:
        return {
            'id': self._id,
            'name': self._name,
            'manager_name': self._manager_name,
            'description': self._description,
            'nav': self._nav,
            'date': self._date,
            'performance': self._performance
        }