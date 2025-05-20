from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Protocol, ClassVar
from .util import generate_name


def action_with(energy_cost=0, fullness_cost=0, min_energy=0, min_fullness=0):
    def dectorator(func):
        def inner(self, *args, **kwargs):
            if self.can_do_action(
                    energy_cost=energy_cost, fullness_cost=fullness_cost,
                    min_energy=min_energy, min_fullness=min_fullness):
                self.energy -= energy_cost
                self.fullness -= fullness_cost
                func(self, *args, **kwargs)
        return inner
    return dectorator


class FoodType(Enum):
    INEDABLE = auto()
    VEGETARIAN = auto()
    MEAT = auto()


class CanBeEaten(Protocol):
    @property
    def energy(self):
        raise NotImplementedError

    @property
    def food_type(self):
        raise NotImplementedError


@dataclass
class Animal(CanBeEaten):
    name: str = field(default_factory=generate_name)
    age: int = 0
    energy: int = 100
    max_energy: int = energy
    fullness: int = 100
    max_fullness: int = fullness

    alive: bool = True
    allowed_food_types: ClassVar[set[FoodType]] = field(default_factory=set)
    food_type: ClassVar[FoodType] = FoodType.MEAT

    def eat(self, food: CanBeEaten):
        if self.can_eat(food):
            # TODO
            pass
        raise NotImplementedError

    def can_eat(self, food: CanBeEaten) -> bool:
        return food.food_type in self.allowed_food_types

    def sleep(self):
        self.energy = max(self.energy + 50, self.max_energy)

    def can_do_action(self, energy_cost: int = 0, fullness_cost: int = 0, min_energy=0, min_fullness=0) -> bool:
        return self.energy - energy_cost > 0 and self.fullness - fullness_cost > 0


@dataclass
class Herbivore(Animal):
    allowed_food_types = {FoodType.VEGETARIAN}


@dataclass
class Carnivore(Animal):
    allowed_food_types = {FoodType.MEAT}


@dataclass
class Omniore(Carnivore, Herbivore):
    allowed_food_types = {FoodType.MEAT, FoodType.VEGETARIAN}


__all__ = ['Animal', 'Carnivore', 'Herbivore', 'Omniore']
