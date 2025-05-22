from dataclasses import dataclass

from .abc import Animal
from .food import FoodType, Grass


@dataclass
class Herbivore(Animal):
    allowed_food_types = {FoodType.VEGETARIAN}

    def eat_grass(self):
        """Eat from the endless zoo grass"""
        self.eat(Grass)

    def do_tick(self):
        if self.is_hungry():
            self.eat_grass()
        super().do_tick()
