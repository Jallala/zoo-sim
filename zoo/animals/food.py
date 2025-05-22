from dataclasses import dataclass
from enum import Enum, auto

from typing import Protocol


class FoodType(Enum):
    INEDABLE = auto()
    VEGETARIAN = auto()
    MEAT = auto()


class CanBeEaten(Protocol):
    energy: int
    food_type: FoodType

    def be_consumed(self, requested: int) -> int:
        raise NotImplementedError


@dataclass
class Food(CanBeEaten):
    energy: int
    food_type: FoodType

    def be_consumed(self, requested: int) -> int:
        energy = min(requested, self.energy)
        self.energy -= energy
        assert self.energy >= 0
        return energy


class Grass(CanBeEaten):
    """Infinite grass source"""
    energy: -1
    energy_per_action = 20
    food_type = FoodType.VEGETARIAN

    @classmethod
    def be_consumed(cls, requested: int) -> int:
        # pylint: disable=arguments-differ
        return min(requested, cls.energy_per_action)
