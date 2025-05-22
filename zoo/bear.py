from dataclasses import dataclass

from .animals import Omnivore


@dataclass
class Bear(Omnivore):
    max_fullness: int = 600
    food_value: int = 400
    is_hibernating: bool = False

    @property
    def energy_consumption_per_tick(self):
        return -1 if self.is_hibernating else self.energy_consumption_per_tick

    @property
    def hunger_per_tick(self):
        return 1 if self.is_hibernating else self.hunger_per_tick

    def wake_up(self):
        assert self.is_hibernating
