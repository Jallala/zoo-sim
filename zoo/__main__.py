import random


from .animal import Herbivore, Carnivore, Omnivore
from .lion import Lion
from .simulation import Simulation
from .visitor import Visitor


if __name__ == '__main__':
    import logging
    import os
    log_level = os.environ.get('LOGLEVEL', 'INFO').upper()
    logging.basicConfig(level=log_level)
    vistor = Visitor()

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
    stats = np.zeros(shape=(200, len(label_order)), dtype=int)
    
    i = 0
    def append_stats():
        stats[i] = [
            len(sim.carnivores),
            len(sim.herbivores),
            len(sim.omnivores),
            sum(isinstance(c, Lion) for c in sim.carnivores)
        ]

    append_stats()
    while sim.has_animals_that_are_still_alive() and (i := i + 1) < len(stats):
        logging.getLogger(__name__).info('tick %s', sim.time)
        sim.tick()
        append_stats()

    fig, ax = plt.subplots()
    tp = np.transpose(stats)
    plt.xlabel('Tick')
    plt.ylabel('Animals')
    for idx, label in enumerate(label_order):
        line, = ax.plot(np.arange(200), tp[idx])
        line.set_label(label)

    ax.legend()
    plt.show()
