from abc import abstractmethod, ABC


#  Data access abstraction layer such that other components do not rely on the underlying data storage.
class AbstractDb(ABC):
    @abstractmethod
    def get_all_ids(self):
        raise NotImplementedError

    @abstractmethod
    def add_fund(self, fund):
        raise NotImplementedError

    @abstractmethod
    def update_fund(self, id):
        raise NotImplementedError

    @abstractmethod
    def get_fund(self, id, data):
        raise NotImplementedError

    @abstractmethod
    def get_all(self):
        raise NotImplementedError

    @abstractmethod
    def delete_fund(self):
        raise NotImplementedError
        