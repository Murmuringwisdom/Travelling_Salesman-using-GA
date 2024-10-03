from math import floor

import matplotlib.pyplot as plt
import numpy as np
import operator
import pandas as pd
import random

from src.model.Fitness import Fitness
from src.model.Grad import Grad


def makePath(list_of_cities):
    return random.sample(list_of_cities, len(list_of_cities))


def initialpopulation(population_size, list_of_cities):
    pop = []
    for i in range(population_size):
        pop.append(makePath(list_of_cities))
    return pop


def rankPath(pop):
    fitness_scores = {}
    for i in range(len(pop)):
        fitness_scores[i] = Fitness(pop[i]).fitnessPath()
    return sorted(fitness_scores.items(), key=operator.itemgetter(1), reverse=True)


def selection(pop_ranked, number_of_elite):
    selection_result = []
    df = pd.DataFrame(np.array(pop_ranked), columns=["Index", "Fitness"])
    df['cumulative_sum'] = df.Fitness.cumsum()
    df['cumulative_perc'] = 100 * df.cumulative_sum / df.Fitness.sum()

    for i in range(0, number_of_elite):
        selection_result.append(pop_ranked[i][0])
    for i in range(len(pop_ranked) - number_of_elite):
        selected = 100 * random.random()
        for i in range(len(pop_ranked)):
            if selected <= df.iat[i, 3]:
                selection_result.append(pop_ranked[i][0])
                break
    return selection_result


def selection_crossover(pop, selection_result):
    selected = []
    for i in range(len(selection_result)):
        selected.append(pop[selection_result[i]])
    return selected


def hybridization(parent1, parent2):
    first_part = []

    gen_a = int(random.random() * len(parent1))
    gen_b = int(random.random() * len(parent2))

    initial_gen = min(gen_a, gen_b)
    end_gen = max(gen_a, gen_b)

    for i in range(initial_gen, end_gen):
        first_part.append(parent1[i])

    other_part = [gen for gen in parent2 if gen not in first_part]
    child = other_part[:initial_gen] + first_part + other_part[initial_gen:]
    # return first_part + other_part
    return child


def matingPopulations(selected_for_mating, number_of_elite):
    deca = []
    dozen = len(selected_for_mating) - number_of_elite
    selection = random.sample(selected_for_mating, len(selected_for_mating))

    for i in range(0, number_of_elite):
        deca.append(selected_for_mating[i])

    for i in range(dozen):
        deca.append(hybridization(selection[i], selection[len(selected_for_mating) - 1 - i]))
    return deca


def mutate(path, mutation_chance):
    for replaced in range(len(path)):
        if random.random() < mutation_chance:
            have_been_replaced = int(random.random() * len(path))

            path[replaced], path[have_been_replaced] = path[have_been_replaced], path[replaced]
    return path


def mutatePopulation(pop, mutation_chance):
    mutirana_pop = []

    for i in range(len(pop)):
        mutirana_pop.append(mutate(pop[i], mutation_chance))
    return mutirana_pop


def nextgeneration(current_gen, number_of_elite, mutation_chance):
    ranked_pop = rankPath(current_gen)
    selection_result = selection(ranked_pop, number_of_elite)
    selected_za_hybridization = selection_crossover(current_gen, selection_result)
    deca = matingPopulations(selected_za_hybridization, number_of_elite)
    next_gen = mutatePopulation(deca, mutation_chance)
    return next_gen


def showMap(list_of_cities, ITERATION=None):
    plt.clf()
    prev = Grad(0, 0)
    if ITERATION:
        plt.title("ITERATION: " + str(ITERATION))
    for i in list_of_cities:
        plt.plot(i.x, i.y, 'ro')
        plt.plot(prev.x, prev.y, 'k-')
        if prev.x == 0 and prev.y == 0:
            prev = i
            plt.plot([prev.x, list_of_cities[-1].x], [prev.y, list_of_cities[-1].y], 'k-')
            continue
        else:
            plt.plot([prev.x, i.x], [prev.y, i.y], 'k-')
            prev = i

    plt.pause(0.0000001)


def geneticAlgorithm(population, population_size, number_of_elite, mutation_chance, generations):
    pop = initialpopulation(population_size, population)
    print("Initial distance: " + str(1 / rankPath(pop)[0][1]))
    interval = floor(generations * 0.05)  
    threshold = 50  
    for i in range(generations):
        pop = nextgeneration(pop, number_of_elite, mutation_chance)
        index_best_path = rankPath(pop)[0][0]
        best_path = pop[index_best_path]
        if i < threshold:
            print("ITERATION " + str(i))
            showMap(best_path, i)
        elif i < 2 * threshold:
            if i % interval == 0:
                print("ITERATION " + str(i))
                showMap(best_path, i)

        elif i % (interval * 2) == 0:
            print("ITERATION " + str(i))
            showMap(best_path, i)
    final_distance = 1 / rankPath(pop)[0][1]
    print("Final distance: " + str(final_distance))
    index_best_path = rankPath(pop)[0][0]
    best_path = pop[index_best_path]
    showMap(best_path, str(generations) + "\nPath length: " + str(final_distance))
    return final_distance
