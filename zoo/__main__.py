
from .animal import Herbivore, Carnivore
from .simulation import Simulation
from .visitor import Visitor


if __name__ == '__main__':
    import logging
    import os
    log_level = os.environ.get('LOGLEVEL', 'INFO').upper()
    logging.basicConfig(level=log_level)
    vistor = Visitor()
    herbivore = Herbivore()
    carnivore = Carnivore(max_fullness=200)

    sim = Simulation(
        carnivores=[carnivore],
        herbivores=[herbivore],
        visitors=[Visitor()]
    )
    while sim.has_animals_that_are_still_alive():
        sim.tick()
