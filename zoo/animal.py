from dataclasses import dataclass, field

from .util import generate_name


@dataclass
class Animal:
    name: str = field(default_factory=generate_name)
    energy: int = 100

    def eat(self):
        raise NotImplementedError

    def sleep(self):
        raise NotImplementedError


@dataclass
class Herbivore(Animal):
    pass


@dataclass
class Carnivore(Animal):
    pass


@dataclass
class Omniore(Carnivore, Herbivore):
    pass


__ALL__ = [Animal, Carnivore, Herbivore, Omniore]
