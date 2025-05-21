import random
import logging

from dataclasses import dataclass, field
from .animal import Animal, Carnivore, Herbivore, Omnivore, Food
from .visitor import Visitor


@dataclass
class Simulation:
    carnivores: list[Carnivore] = field(default_factory=list)
    herbivores: list[Herbivore] = field(default_factory=list)
    omnivores: list[Omnivore] = field(default_factory=list)
    visitors: list[Visitor] = field(default_factory=list)
    time: int = 0

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
                animal = random.choice(all_animals)
                food = Food(int(random.uniform(10, 50)),
                            food_type=random.choice(list(animal.allowed_food_types)))
                visitor.feed(animal, food)

        for carnivore in self.carnivores:
            if carnivore.is_hungry():
                targets = [*self.herbivores, *self.omnivores]
                if not targets:
                    break
                random_pray = self.pick_random(targets)
                carnivore.hunt(random_pray)
                try:
                    self.herbivores.remove(random_pray)
                except ValueError:
                    self.omnivores.remove(random_pray)

        for omnivore in self.omnivores:
            if omnivore.is_hungry():
                if self.carnivores and self.herbivores and abs(random.gauss()) > 1.2:
                    # Chance for omnivore to hunt
                    random_pray = self.pick_random(
                        [*self.herbivores, *self.carnivores])
                    omnivore.hunt(random_pray)
                    try:
                        self.herbivores.remove(random_pray)
                    except ValueError:
                        self.carnivores.remove(random_pray)
                else:
                    omnivore.eat_grass()

    @staticmethod
    def pick_random(seq):
        return random.choice(seq)

    def do_tics_for(self, animals: list[Animal]):
        for animal in animals:
            animal.do_tick()
        return [animal for animal in animals if animal.alive]

    def has_animals_that_are_still_alive(self) -> bool:
        return bool(self.carnivores or self.herbivores or self.omnivores)
