from dataclasses import dataclass

from .animal import action_with, Carnivore, Animal


@dataclass
class Lion(Carnivore):
    @action_with(energy_cost=10)
    def roar(self):
        print('Roar!')

    @action_with(min_energy=30, energy_cost=20, fullness_cost=5)
    def hunt(self, other: Animal):
        raise NotImplementedError
