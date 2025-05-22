import random
import logging

from dataclasses import dataclass, field
from .animals import Animal, Carnivore, Herbivore, Omnivore
from .visitor import Visitor


@dataclass
class Simulation:
    carnivores: list[Carnivore] = field(default_factory=list)
    herbivores: list[Herbivore] = field(default_factory=list)
    omnivores: list[Omnivore] = field(default_factory=list)
    visitors: list[Visitor] = field(default_factory=list)
    time: int = 0
    times_fed: int = 0
    times_pet: int = 0
    times_hunted: int = 0

    def tick(self):
        # TODO Refactor
        logging.getLogger(__name__).debug('%s', self)
        self.time += 1
        self.carnivores: list[Carnivore] = self.do_tics_for(self.carnivores)
        self.herbivores: list[Herbivore] = self.do_tics_for(self.herbivores)
        self.omnivores: list[Omnivore] = self.do_tics_for(self.omnivores)
        if not self.has_animals_that_are_still_alive():
            return

        all_animals = [*self.carnivores, *self.herbivores, *self.omnivores]

        # Visitors have chance to feed once per tick
        for visitor in self.visitors:
            if abs(random.gauss()) > 1.2:
                animal: Animal = self.pick_random(all_animals)
                self.times_fed += 1
                visitor.feed(animal)
            if abs(random.gauss()) > 1.4:
                animal: Animal = self.pick_random(all_animals)
                self.times_pet += 1
                visitor.pet(animal)

        for carnivore in self.carnivores:
            if carnivore.is_hungry():
                if self.herbivores or self.omnivores:
                    random_pray = self.pick_random(
                        self.herbivores, self.omnivores)
                    self.times_hunted += 1
                    carnivore.hunt(random_pray)
                    self.remove(random_pray)

        for omnivore in self.omnivores:
            if omnivore.is_hungry():
                if (self.carnivores or self.herbivores) and abs(random.gauss()) > 1.2:
                    # Chance for omnivore to hunt
                    random_pray = self.pick_random(
                        self.herbivores, self.carnivores)
                    self.times_hunted += 1
                    omnivore.hunt(random_pray)
                    self.remove(random_pray)
                else:
                    omnivore.eat_grass()

    def remove(self, animal: Animal):
        for animal_seq in (self.carnivores, self.herbivores, self.omnivores):
            try:
                animal_seq.remove(animal)
                break
            except ValueError:
                pass
        else:
            raise ValueError(f'Cannot find {animal} in {self}')

    @staticmethod
    def pick_random(*args):
        args = [arg for arg in args if arg]
        if len(args) == 1:
            return random.choice(args[0])
        return random.choice([item for arg in args for item in arg])

    def do_tics_for(self, animals: list[Animal]):
        for animal in animals:
            animal.do_tick()
        return [animal for animal in animals if animal.alive]

    def has_animals_that_are_still_alive(self) -> bool:
        return bool(self.carnivores or self.herbivores or self.omnivores)
