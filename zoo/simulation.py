import random

from dataclasses import dataclass, field
from .animal import Animal, Carnivore, Herbivore, Omnivore, Food, FoodType
from .visitor import Visitor


@dataclass
class Simulation:
    carnivores: list[Carnivore] = field(default_factory=list)
    herbivores: list[Herbivore] = field(default_factory=list)
    omnivores: list[Omnivore] = field(default_factory=list)
    visitors: list[Visitor] = field(default_factory=list)
    time: int = 0

    def run(self):
        raise NotImplementedError

    def tick(self):
        self.time += 1
        self.carnivores = self.do_tics_for(self.carnivores)
        self.herbivores = self.do_tics_for(self.herbivores)
        self.omnivores = self.do_tics_for(self.omnivores)
        if self.carnivores:
            for visitor in self.visitors:
                visitor: Visitor = visitor
                if abs(random.gauss()) > 1.2:
                    carnivore = random.choice(self.carnivores)
                    food = Food(int(random.uniform(10, 50)),
                                food_type=FoodType.MEAT)
                    visitor.feed(carnivore, food)

    def do_tics_for(self, animals: list[Animal]):
        for animal in animals:
            animal.do_tick()
        return [animal for animal in animals if animal.alive]

    def has_animals_that_are_still_alive(self) -> bool:
        return bool(self.carnivores or self.herbivores or self.omnivores)
