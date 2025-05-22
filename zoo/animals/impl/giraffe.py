import logging

from dataclasses import dataclass, field

from zoo.util import gauss_with_min
from ..herbivore import Herbivore
from ..food import Tree

_LOGGER = logging.getLogger(__name__)


@dataclass
class Giraffe(Herbivore):
    max_age: int = field(default_factory=gauss_with_min(120, 50))
    max_fullness: int = 400
    hungry_when: int = 100

    def eat_trees(self):
        self.eat(Tree)
        logging.debug('%s ate trees', self)

    def do_tick(self):
        if self.is_hungry():
            self.eat_trees()
        super().do_tick()
