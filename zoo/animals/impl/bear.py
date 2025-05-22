import random
import logging

from dataclasses import dataclass

from .. import Omnivore

_LOGGER = logging.getLogger(__name__)


@dataclass
class Bear(Omnivore):
    max_fullness: int = 150
    food_value: int = 400
    is_hibernating: bool = False

    @property
    def energy_consumption_per_tick(self) -> int:
        return -1 if self.is_hibernating else self._energy_consumption_per_tick

    @energy_consumption_per_tick.setter
    def energy_consumption_per_tick(self, value: int):
        self._energy_consumption_per_tick = value

    @property
    def hunger_per_tick(self) -> int:
        return 5 if self.is_hibernating else self._hunger_per_tick

    @hunger_per_tick.setter
    def hunger_per_tick(self, value: int):
        self._hunger_per_tick = value

    def wake_up(self):
        _LOGGER.info('%s woke up from hibernation', self)
        assert self.is_hibernating
        self.is_hibernating = False

    def hibernate(self):
        if self.is_hibernating:
            return
        _LOGGER.info('%s hibernates', self)
        self.is_hibernating = True

    def hunt(self, other):
        if self.is_hibernating:
            return
        super().hunt(other)

    def eat(self, food):
        if self.is_hibernating:
            return None
        return super().eat(food)

    def do_tick(self):
        super().do_tick()
        if self.alive:
            if self.is_hibernating and self.is_hungry():
                self.wake_up()
            else:
                close_to_max_fullness = 20 > self.max_fullness - self.fullness
                if close_to_max_fullness and random.randint(0, 20) > 10:
                    self.hibernate()
