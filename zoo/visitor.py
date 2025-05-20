from dataclasses import dataclass, field
from .animal import Animal


@dataclass
class Visitor:
    name: str
    age: str

    def feed(self, animal: Animal):
        raise NotImplementedError
