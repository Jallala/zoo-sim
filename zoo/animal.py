from dataclasses import dataclass, field

from .util import generate_name


def action_with(cost):
    def dectorator(func):
        def inner(self, *args, **kwargs):
            if self.can_do_action(cost):
                self.energy -= cost
                func(self, *args, **kwargs)
    return dectorator


@dataclass
class Animal:
    name: str = field(default_factory=generate_name)
    energy: int = 100
    max_energy: int = energy

    def eat(self):
        raise NotImplementedError

    def sleep(self):
        self.energy = max(self.energy + 50, self.max_energy)

    def can_do_action(self, cost: int):
        return self.energy - cost > 0


@dataclass
class Herbivore(Animal):
    pass


@dataclass
class Carnivore(Animal):
    pass


@dataclass
class Omniore(Carnivore, Herbivore):
    pass


__all__ = ['Animal', 'Carnivore', 'Herbivore', 'Omniore']
