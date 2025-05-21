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
        carnivores=[Carnivore(max_fullness=200, max_age=random.randint(50, 200))
                    for _ in range(10)] + [Lion() for _ in range(2)],
        herbivores=[Herbivore(food_value=50) for _ in range(500)],
        omnivores=[Omnivore(food_value=50) for _ in range(200)],
        visitors=[Visitor() for _ in range(100)]
    )

    import matplotlib.pyplot as plt
    import numpy as np
    stats = np.zeros(shape=(200, 3), dtype=int)
    i = 0
    stats[i] = [len(sim.carnivores), len(sim.herbivores), len(sim.omnivores)]
    while sim.has_animals_that_are_still_alive() and (i := i + 1) < len(stats):
        logging.getLogger(__name__).info('tick %s', sim.time)
        sim.tick()
        stats[i] = [len(sim.carnivores), len(
            sim.herbivores), len(sim.omnivores)]
    fig, ax = plt.subplots()
    tp = np.transpose(stats)
    plt.xlabel('Tick')
    plt.ylabel('Animals')
    line, = ax.plot(np.arange(200), tp[0])
    line.set_label('Carnivores')
    line, = ax.plot(np.arange(200), tp[1])
    line.set_label('Herbivores')
    line, = ax.plot(np.arange(200), tp[2])
    line.set_label('Omnivores')
    ax.legend()
    plt.show()
