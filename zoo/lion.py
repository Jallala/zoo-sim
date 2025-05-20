from dataclasses import dataclass

from .animal import action_with, Carnivore


class Lion(Carnivore):
    @action_with(cost=10)
    def roar(self):
        print('Roar!')
