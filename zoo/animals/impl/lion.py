import logging
import random
from dataclasses import dataclass, field

from zoo.util import gauss_with_min
from .. import action_with, Carnivore

_LOGGER = logging.getLogger(__name__)

@dataclass
class Lion(Carnivore):
    max_age: int = field(default_factory=gauss_with_min(100, 30))

    @action_with(energy_cost=10)
    def roar(self):
        _LOGGER.info('%s roars!', self)

    def do_tick(self):
        super().do_tick()
        if random.randint(0, 20) < 5:
            self.roar()
