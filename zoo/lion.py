from dataclasses import dataclass

from .animal import Carnivore


class Lion(Carnivore):
    def roar(self):
        
        print('Roar!')
