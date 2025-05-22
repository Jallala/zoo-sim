import random


from .animals import Herbivore, Carnivore, Omnivore, Lion, Bear
from .simulation import Simulation
from .visitor import Visitor


if __name__ == '__main__':
    import logging
    import os
    log_level = os.environ.get('LOGLEVEL', 'INFO').upper()
    logging.basicConfig(level=log_level)
    _LOGGER = logging.getLogger('main')
    MAX_TICKS = 5000

    sim = Simulation(
        carnivores=[Carnivore(max_fullness=200, max_age=max(1, int(random.gauss(20, 3))))
                    for _ in range(10)] + [Lion() for _ in range(2)],
        herbivores=[Herbivore(food_value=50) for _ in range(50)],
        omnivores=[Omnivore(food_value=50) for _ in range(20)],
        visitors=[Visitor() for _ in range(100)]
    )

    import matplotlib.pyplot as plt
    import numpy as np
    label_order = ('Carnivores', 'Herbivores', 'Omnivores', 'Lions')

    i = 0
    stats = np.zeros(shape=(200, len(label_order)), dtype=int)

    def append_stats(s):
        stat_size, col_length = s.shape
        if stat_size <= i:
            new_shape = (min(int(stat_size * 1.5), MAX_TICKS), col_length)
            _LOGGER.info('Resize stats from %s to %s', s.shape, new_shape)
            s = np.resize(s, new_shape)
        s[i] = [
            len(sim.carnivores),
            len(sim.herbivores),
            len(sim.omnivores),
            sum(isinstance(c, Lion) for c in sim.carnivores)
        ]
        return s

    stats = append_stats(stats)
    while sim.has_animals_that_are_still_alive() and (i := i + 1) < MAX_TICKS:
        _LOGGER.info('tick %s', sim.time)
        sim.tick()
        stats = append_stats(stats)

    fig, ax = plt.subplots()
    tp = np.transpose(stats)
    plt.xlabel('Tick')
    plt.ylabel('Animals')
    for idx, label in enumerate(label_order):
        line, = ax.plot(np.arange(stats.shape[0]), tp[idx])
        line.set_label(label)

    ax.legend()
    plt.show()
