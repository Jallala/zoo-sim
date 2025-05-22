import logging
import random

from dataclasses import dataclass, field
from .animals import Animal, Food
from .util import generate_name

_LOGGER = logging.getLogger(__name__)


@dataclass
class Visitor:
    name: str = field(default_factory=generate_name)
    age: int = 0

    def feed(self, animal: Animal, food: Food = None):
        if not animal.is_hungry():
            return
        if food is None:
            energy = int(random.uniform(10, 50))
            food_type = random.choice(list(animal.allowed_food_types))
            food = Food(energy=energy, food_type=food_type)
        restored = animal.eat(food)
        if restored is not None:
            _LOGGER.info('Visitor %r fed %s with %s that restored %s fullness',
                        self.name, animal, food, restored)

    def pet(self, animal: Animal):
        _LOGGER.info('Visitor %r pet %s', self.name, animal)
