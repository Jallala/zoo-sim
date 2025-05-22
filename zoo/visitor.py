import logging

from dataclasses import dataclass, field
from .animals import Animal, Food
from .util import generate_name

_LOGGER = logging.getLogger(__name__)


@dataclass
class Visitor:
    name: str = field(default_factory=generate_name)
    age: int = 0

    def feed(self, animal: Animal, food: Food):
        restored = animal.eat(food)
        _LOGGER.debug('Visitor %r fed %s with %s that restored %s fullness',
                      self.name, animal, food, restored)
