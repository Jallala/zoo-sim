from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Protocol, ClassVar
from .util import generate_name


def action_with(energy_cost=0, fullness_cost=0, min_energy=0, min_fullness=0, fatal_error=False):
    def dectorator(func):
        def inner(self, *args, **kwargs):
            if self.can_do_action(
                    energy_cost=energy_cost, fullness_cost=fullness_cost,
                    min_energy=min_energy, min_fullness=min_fullness):
                self.energy -= energy_cost
                self.fullness -= fullness_cost
                func(self, *args, **kwargs)
            elif fatal_error:
                raise RuntimeError('Predicate fails')
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
    food_type = FoodType.VEGETARIAN

    @classmethod
    def be_consumed(cls, requested: int) -> int:
        # pylint: disable=arguments-differ
        return requested


@dataclass
class Animal(CanBeEaten):
    name: str = field(default_factory=generate_name)
    age: int = 0
    energy: int = 100
    max_energy: int = energy
    fullness: int = 100
    max_fullness: int = fullness

    alive: bool = True
    food_value: int = 100
    allowed_food_types: ClassVar[set[FoodType]] = {}
    food_type: ClassVar[FoodType] = FoodType.MEAT

    def eat(self, food: CanBeEaten) -> int:
        """Eat some food, returns fullness restored by eating"""
        fullness_restored = 0
        if self.can_eat(food):
            fullness_restored = food.be_consumed(self.max_fullness - self.fullness)
            self.fullness += fullness_restored
        return fullness_restored

    def be_consumed(self, requested: int):
        if not requested:
            return 0
        if self.alive:
            self.die()
        consumed_value = min(requested, self.food_value)
        self.food_value -= consumed_value
        return consumed_value

    def die(self):
        self.alive = False
        self.energy = 0
        self.fullness = 0

    def can_eat(self, food: CanBeEaten) -> bool:
        return food.food_type in self.allowed_food_types

    def sleep(self):
        self.energy = max(self.energy + 50, self.max_energy)

    def can_do_action(
            self, energy_cost: int = 0, fullness_cost: int = 0,
            min_energy: int = 0, min_fullness: int = 0) -> bool:
        minimums_are_met = min_energy > self.energy or min_fullness > self.fullness
        costs_does_not_bring_values_below_zero = (
            self.energy - energy_cost > 0 and self.fullness - fullness_cost > 0)

        return minimums_are_met and costs_does_not_bring_values_below_zero


@dataclass
class Herbivore(Animal):
    allowed_food_types = {FoodType.VEGETARIAN}

    def eat_grass(self):
        """Eat from the endless zoo grass"""
        self.eat(Grass)


@dataclass
class Carnivore(Animal):
    allowed_food_types = {FoodType.MEAT}


@dataclass
class Omniore(Carnivore, Herbivore):
    allowed_food_types = {FoodType.MEAT, FoodType.VEGETARIAN}


__all__ = ['Animal', 'Carnivore', 'Herbivore', 'Omniore']
