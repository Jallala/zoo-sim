import random
import logging
import os
import matplotlib.pyplot as plt
import numpy as np

from .animals import Herbivore, Carnivore, Omnivore, Lion, Bear, Giraffe
from .simulation import Simulation
from .visitor import Visitor

MAX_TICKS = 5000


def main():

    log_level = os.environ.get('LOGLEVEL', 'INFO').upper()
    logging.basicConfig(level=log_level)
    _logger = logging.getLogger('main')

    sim = Simulation(
        carnivores=[
            Carnivore(
                max_fullness=200,
                max_age=max(1, int(random.gauss(20, 3)))
            ) for _ in range(5)] + [Lion() for _ in range(5)],
        herbivores=[Herbivore(food_value=200) for _ in range(25)] + [Giraffe() for _ in range(25)],
        omnivores=[Omnivore(food_value=50) for _ in range(4)] + [Bear() for _ in range(2)],
        visitors=[Visitor() for _ in range(15)]
    )
    label_order = ('Carnivores', 'Herbivores', 'Omnivores', 'Lions', 'Giraffes', 'Bears')

    i = 0
    stats = []

    def append_stats(s):
        s.append([
            len(sim.carnivores),
            len(sim.herbivores),
            len(sim.omnivores),
            sum(isinstance(c, Lion) for c in sim.carnivores),
            sum(isinstance(c, Giraffe) for c in sim.herbivores),
            sum(isinstance(c, Bear) for c in sim.omnivores)
        ])
        return s

    stats = append_stats(stats)
    while sim.has_animals_that_are_still_alive() and (i := i + 1) < MAX_TICKS:
        _logger.info('tick %s', sim.time)
        sim.tick()
        stats = append_stats(stats)

    _logger.info('Simulation end, %r', sim)
    
    _fig, ax = plt.subplots()
    tp = np.transpose(np.array(stats))
    plt.xlabel('Tick')
    plt.ylabel('Animals')
    for idx, label in enumerate(label_order):
        line, = ax.plot(range(len(stats)), tp[idx])
        line.set_label(label)

    ax.legend()
    plt.show()


if __name__ == '__main__':
    main()
