from dataclasses import dataclass, field
from .animal import Animal
from .util import generate_name


@dataclass
class Visitor:
    name: str = field(default_factory=generate_name)
    age: int = 0

    def feed(self, animal: Animal):
        raise NotImplementedError
