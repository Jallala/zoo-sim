import logging

from dataclasses import dataclass, field
from typing import ClassVar

from zoo.util import generate_name, gauss_with_min
from .food import CanBeEaten, FoodType

_LOGGER = logging.getLogger(__name__)


def action_with(energy_cost=0, fullness_cost=0, min_energy=0, min_fullness=0, or_else=None):
    def dectorator(func):
        def inner(self, *args, **kwargs):
            can_do_action = self.can_do_action(
                energy_cost=energy_cost, fullness_cost=fullness_cost,
                min_energy=min_energy, min_fullness=min_fullness)
            _LOGGER.debug('dec %s, %s, can do action %s',
                          self, func, can_do_action)
            if can_do_action:
                self.energy -= energy_cost
                self.fullness -= fullness_cost
                func(self, *args, **kwargs)
            elif or_else:
                or_else(self)
        return inner
    return dectorator


def _die(obj: 'Animal'):
    assert obj.alive
    if obj.fullness <= 0:
        reason = 'of starvation'
    elif obj.age >= obj.max_age:
        reason = 'of old age'
    else:
        reason = 'being prayed upon'
    obj.alive = False
    obj.energy = 0
    obj.fullness = 0
    _LOGGER.info('%s died %s', obj, reason)


@dataclass
class Animal(CanBeEaten):
    name: str = field(default_factory=generate_name)
    age: int = 0
    max_age: int = field(default_factory=gauss_with_min(100, 10))
    energy: int = 100
    max_energy: int = energy
    energy_consumption_per_tick: int = 10
    tired_when: int = 50

    fullness: int = 100
    max_fullness: int = fullness
    hunger_per_tick: int = 10
    hungry_when: int = 20

    alive: bool = True
    food_value: int = 100
    allowed_food_types: ClassVar[set[FoodType]] = {}
    food_type: ClassVar[FoodType] = FoodType.MEAT
    _ID: ClassVar[int] = 0

    def eat(self, food: CanBeEaten) -> int:
        """Eat some food, returns fullness restored by eating"""
        assert self is not food, 'Should never try to eat it self.'
        fullness_restored = 0
        if self.can_eat(food):
            fullness_restored = food.be_consumed(
                self.max_fullness - self.fullness)
            self.fullness += fullness_restored
        _LOGGER.debug('%s ate %s that restored %i fullness',
                      self, food, fullness_restored)
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
        return _die(self)

    def can_eat(self, food: CanBeEaten) -> bool:
        return food.food_type in self.allowed_food_types

    def sleep(self):
        _LOGGER.debug('%s went to sleep', self)
        self.energy = max(self.energy + 50, self.max_energy)

    def can_do_action(
            self, energy_cost: int = 0, fullness_cost: int = 0,
            min_energy: int = 0, min_fullness: int = 0) -> bool:
        minimums_are_met = min_energy < self.energy and min_fullness < self.fullness
        costs_does_not_bring_values_below_zero = (
            self.energy - energy_cost > 0 and self.fullness - fullness_cost > 0)

        return minimums_are_met and costs_does_not_bring_values_below_zero

    def is_tired(self):
        return self.energy < self.tired_when

    def is_hungry(self):
        return self.fullness < self.hungry_when

    def should_die(self):
        return self.fullness < 0 or self.age >= self.max_age

    def do_tick(self):
        self.age += 1
        self.energy -= self.energy_consumption_per_tick
        self.fullness -= self.hunger_per_tick
        if self.should_die():
            self.die()
            return
        if self.is_tired():
            self.sleep()

    def __str__(self):
        return f'{self.__class__.__name__} {self.name!r} ({self.age})'
