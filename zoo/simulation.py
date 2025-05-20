from dataclasses import dataclass

@dataclass
class Simulation:
    animals = []
    time: int = 0

    def run(self):
        raise NotImplementedError

    def tick(self):
        self.time += 1
        raise NotImplementedError
