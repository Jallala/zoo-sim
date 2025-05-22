import logging
from dataclasses import dataclass

from .food import FoodType
from .abc import Animal


_LOGGER = logging.getLogger(__name__)


@dataclass
class Carnivore(Animal):
    allowed_food_types = {FoodType.MEAT}

    def hunt(self, other: Animal):
        _LOGGER.info('%s hunts %s', self, other)
        assert self is not other, 'Should never call hunt for self'
        if self.is_hungry():
            self.eat(other)
