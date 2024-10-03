import matplotlib.pyplot as plt
import random

from src import ga
from src.model.Grad import Grad


def main():
    List_of_cities = []

    for i in range(0, 20):
        List_of_cities.append(Grad(x=int(random.random() * 200), y=int(random.random() * 200)))
    best = []
    for i in range(3):
        plt.figure()
        best.append(ga.geneticAlgorithm(population=List_of_cities, population_size=100, number_of_elite=10,
                                             mutation_chance=0.02,
                                             generations=400))

    print("\n\n\n\nShortest paths through iterations:")
    for i in range(len(best)):
        print(str(i + 1) + ". Final distance: " + str(best[i]))
    plt.show()


if __name__ == '__main__':
    main()
