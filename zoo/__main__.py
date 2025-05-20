from .animal import Herbivore
from .visitor import Visitor


if __name__ == '__main__':
    herb = Herbivore()
    visitor = Visitor('Bob', 42)
    visitor.feed(herb)
