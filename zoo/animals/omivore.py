import logging
from dataclasses import dataclass

from .food import FoodType
from .carnivore import Carnivore
from .herbivore import Herbivore


_LOGGER = logging.getLogger(__name__)


@dataclass
class Omnivore(Carnivore, Herbivore):
    allowed_food_types = {FoodType.MEAT, FoodType.VEGETARIAN}
