import uuid
import datetime
from checks.models.rule import Rule
from typing import TYPE_CHECKING

if TYPE_CHECKING:#
    from checks.checker import Checker

class Check:

    IN_STOCK = "In Stock"
    OUT_OF_STOCK = "Out of Stock"

    def __init__(self):
        self._identifier = uuid.uuid4()
        self._name: str = "unknown"
        self._rules: list[Rule] = []
        self._status: None|str|bool = None
        self._last_status: None|str|bool = None
        self._last_run: str|None = None

    def add_rule(self, rule: Rule):
        self._rules.append(rule)

    def check(self, checker: "Checker") -> bool|str:
        self._last_status = self._status
        result = False

        for rule in self.rules:
            if rule.check() == rule.IN_STOCK:
                result = True
            self._last_run = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self._status = result
            checker.print_status()

        return self.status

    def to_dict(self):
        return {
            'class': self.__class__.__name__,
            'name': self.name,
            'rules': [rule.to_dict() for rule in self.rules],
        }

    @classmethod
    def from_dict(cls, data):
        check = cls()
        check.name = data['name']
        for rule in data['rules']:
            from checks.models.rule_website import RuleWebsite
            if isinstance(rule, RuleWebsite):
                check.add_rule(rule)
            else:
                raise NotImplementedError(f"Rule class {rule['class']} not implemented")
        return check

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
    def rules(self):
        return self._rules

    @property
    def status(self) -> str:
        return str(self.IN_STOCK if self._status else self.OUT_OF_STOCK if self._status is not None else None)

    @status.setter
    def status(self, status: None|str|bool):
        self._status = status

    @property
    def last_status(self) -> str:
        return str(self.IN_STOCK if self._last_status else self.OUT_OF_STOCK if self._last_status is not None else None)

    @property
    def last_run(self) -> str:
        return str(self._last_run)
