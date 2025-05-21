from dataclasses import dataclass, field
from .animal import action_with, Carnivore
from .util import gauss_with_min


@dataclass
class Lion(Carnivore):
    max_age: int = field(default_factory=gauss_with_min(100, 30))

    @action_with(energy_cost=10)
    def roar(self):
        print('Roar!')

    def do_tick(self):
        super().do_tick()
        self.roar()
