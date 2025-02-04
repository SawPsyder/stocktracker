import uuid

class Rule:

    IN_STOCK = "In Stock"
    OUT_OF_STOCK = "Out of Stock"

    def __init__(self):
        self._identifier = uuid.uuid4()
        self._name = "unknown"
        self._status: None|str|bool = None
        self._last_status: None|str|bool = None
        self._last_run: str|None = None

    def check(self) -> bool:
        raise NotImplementedError("Check method not implemented")

    def to_dict(self):
        return {
            'class': self.__class__.__name__,
            'name': self.name,
        }

    @classmethod
    def from_dict(cls, data):
        raise NotImplementedError("from_dict method not implemented")

    @property
    def identifier(self):
        return self._identifier

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def status(self):
        return str(self.IN_STOCK if self._status else self.OUT_OF_STOCK if self._status is not None else None)

    @status.setter
    def status(self, status: None|str|bool):
        self._status = status

    @property
    def last_status(self):
        return str(self.IN_STOCK if self._last_status else self.OUT_OF_STOCK if self._last_status is not None else None)

    @property
    def last_run(self):
        return str(self._last_run)

    @property
    def information(self):
        return ""