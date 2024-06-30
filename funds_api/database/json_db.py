import json

from .base import AbstractDb


class JsonDb(AbstractDb):
    """Database abstraction to connect to a JSON file."""
    def __init__(self):
        self._data = {}

    def connect(self, path):
        with open(path) as handler:
            data = json.load(handler)
            # Convert the IDs back to int because JSON saves the IDs keys as string.
            self._data = {int(key): value for key, value in data.items()}

        self._path = path

    def get_all_ids(self):
        return list(self._data.keys())

    def get_all(self):
        return list(self._data.values())

    def add_fund(self, fund_data):
        self._data[fund_data['id']] = fund_data
        self._commit()

    def update_fund(self, id, data):
        self._data[id] = data
        self._commit()

    def get_fund(self, id):
        return self._data.get(id)

    def delete_fund(self, id):
        if id not in self._data:
            print(f'Cannot find {id}, no entry deleted.')
            return

        del self._data[id]
        self._commit()

    def _commit(self):
        """Writes data into the JSON file."""
        with open(self._path, 'w') as handler:
            json.dump(self._data, handler, indent=4)
            