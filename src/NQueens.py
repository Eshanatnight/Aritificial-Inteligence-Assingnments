from enum import Enum
import random
from scipy import special as sc
import itertools

class Constants(Enum):
    """ Enum class for the constants """
    NUMBER_OF_QUEENS = 8
    POPULATION_SIZE = 10
    MIXING_NUMBER = 2
    MUTATION_RATE = 0.05


def fitness_score(individual: list) -> int:
    """
    Calculate the fitness score of an individual
    @param individual:
    @return: score: int
    """
    score = 0
    for row in range(Constants.NUMBER_OF_QUEENS.value):
        col = individual[row]
        for other_row in range(Constants.NUMBER_OF_QUEENS.value):
            if other_row == row:
                continue
            if individual[other_row] == col:
                continue
            if other_row + individual[other_row] == row + col:
                continue
            if other_row - individual[other_row] == row - col:
                continue
            # Score increements if the queen is not in conflict with any other queen
            score += 1
    return score / 2


def select_parents(population: list) -> list:
    """
    Select the parents of the population
    @param population:
    @return: parents: list
    """
    parents = []
    for individual in population:
        if random.randrange(sc.comb(Constants.NUMBER_OF_QUEENS.value, 2) * 2) < fitness_score(individual):
            parents.append(individual)
    return parents


def crossover(parents: list) -> list:
    cross_points = random.sample(range(Constants.NUMBER_OF_QUEENS.value), Constants.MIXING_NUMBER.value - 1)
    offsprings = []

    # List of all possible permutations of the parents
    listOfPermutations = list(itertools.permutations(parents, Constants.MIXING_NUMBER.value))

    for permutation in listOfPermutations:
        offspring= []

        # we need to track the starting index of the sublist
        start_pt = 0
        for parent_idx, cross_point in enumerate(cross_points):
            parent_part = permutation[parent_idx][start_pt:cross_point]
            offspring.append(parent_part)
            # Update the index
            start_pt = cross_point

        # Add the last part of the permutation
        last_parent = permutation[-1]
        parent_part = last_parent[cross_point:]
        offspring.append(parent_part)

        offsprings.append(list(itertools.chain(*offspring)))
    return offsprings


def mutate(seq: list) -> list:
    for row in range(len(seq)):
        if (random.random() < Constants.MUTATION_RATE.value):
            seq[row] = random.randrange(Constants.NUMBER_OF_QUEENS.value)
    return seq


def find_solution(population: list, to_print: bool = True) -> bool:
    for individual in population:
        score = fitness_score(individual)

        if to_print:
            print(f'{individual}.Score: {score}')
        if score == sc.comb(Constants.NUMBER_OF_QUEENS.value, 2):
            if to_print:
                print(f'Found solution: ')
            return True

    if to_print:
        print('No solution found')
    return False


def evolve(population: list) -> list:
    """
    Evolve the population
    @param population:
    @return: population: list
    """
    parents = select_parents(population)
    # Select the best individuals

    offsprings = crossover(parents)

    # Mutate the offspring
    offsprings = list(map(mutate, offsprings))

    # Introduce the top individuals to the population
    new_gen = offsprings

    for individual in population:
        new_gen.append(individual)

    new_gen = sorted(new_gen, key=lambda individual: fitness_score(individual), reverse=True)[:Constants.POPULATION_SIZE.value]
    return new_gen


def population_initialization() -> list:
    population = []

    for individual in range(Constants.POPULATION_SIZE.value):
        newIndividual =[random.randrange(Constants.NUMBER_OF_QUEENS.value) for _ in range(Constants.NUMBER_OF_QUEENS.value)]
        population.append(newIndividual)
    return population



def main() -> None:
    generation = 0

    # Initialize the population
    population = population_initialization()

    while not find_solution(population):
        print(f'Generation: {generation}')
        find_solution(population)
        population = evolve(population)
        generation += 1


if __name__ == '__main__':
    main()

