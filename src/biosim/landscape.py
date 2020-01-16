# -*- coding: utf-8 -*-

"""
Contains Data of each cell, fodder functions and
animal list in each cell
"""

__author__ = "Hemanth Sana & Mithunan Sivagnanam"
__email__ = "hesa@nmbu.no & misi@nmbu.no"

from biosim.fauna import Fauna
from biosim.fauna import Herbivore
from biosim.fauna import Carnivore

import math
import operator
import numpy as np


class Landscape:
    """
    Parent class for type of landscape
    """
    parameters = {}

    def __init__(self, animals_list):
        """

        :param animals_list: list of animals in the cell
        """
        self.sorted_animal_fitness = {}
        self.fauna_list = animals_list
        self.remaining_fodder = 0

    def save_fitness(self, animals, species):
        animal_fitness = {}
        for animal in animals[species]:
            animal_fitness[animal] = animal.fitness
        self.sorted_animal_fitness[species] = animal_fitness

    def order_by_fitness(self, to_sort_objects, species, reverse=True):
        self.save_fitness(to_sort_objects, species)
        if reverse:
            self.sorted_animal_fitness[species] = dict(
                sorted(self.sorted_animal_fitness[species].items(),
                       key=operator.itemgetter(1), reverse=True))
        else:
            self.sorted_animal_fitness[species] = dict(
                sorted(self.sorted_animal_fitness[species].items(),
                       key=operator.itemgetter(1)))

    def give_birth(self, animal):
        num_animals = len(self.fauna_list[animal.__class__.__name__])
        if np.random.random() > animal.probability_of_birth(num_animals):
            baby_animal = animal.__class__.__name__()
            if animal.weight > (baby_animal.weight *
                                baby_animal.parameters['xi']):
                self.add_animal(baby_animal)
                animal.weight -= baby_animal * baby_animal.parameters['xi']

    def add_animal(self, animal):
        self.fauna_list[animal.__class__.__name__].append(animal)

    def remove_animal(self, animal):
        self.fauna_list[animal.__class__.__name__].remove(animal)

    def food_type(self, species):
        if species == 'Herbivore':
            return self.remaining_fodder
        elif species == 'Carnivore':
            herbivore_weight_total = 0
            for herb in self.fauna_list['Herbivore']:
                herbivore_weight_total += herb.weight
            return herbivore_weight_total

    def relative_abundance_fodder(self, species):
        return self.food_type(species) / ((len(self.fauna_list[species]) + 1)
                                          * species.parameters['F'])

    def move_propensity(self, dest_cell, species):
        if dest_cell == 'Mountain' or 'Ocean':
            return 0
        else:
            return math.exp(species.parameters['lambda'] *
                            self.relative_abundance_fodder(species))

    def move_probability(self, dest_cell, adj_cells, species):
        propensity_sum = 0
        for _ in adj_cells:
            propensity_sum += self.move_propensity(dest_cell, species)
        return self.move_propensity(dest_cell, species)/propensity_sum

    def herbivore_eats(self):
        self.order_by_fitness(self.fauna_list, 'Herbivore')
        for herb in self.sorted_animal_fitness['Herbivore']:
            if self.remaining_fodder == 0:
                break
            elif self.remaining_fodder >= herb.parameters['F']:
                herb.animal_eats(herb.parameters['F'])
            elif 0 < self.remaining_fodder < herb.parameters['F']:
                herb.animal_eats(self.remaining_fodder)
                self.remaining_fodder = 0

    def carnivore_eats(self):
        self.order_by_fitness(self.fauna_list, 'Carnivore')
        self.order_by_fitness(self.fauna_list, 'Herbivore', False)
        for carn in self.sorted_animal_fitness['Carnivore']:
            if len(self.sorted_animal_fitness['Herbivore']) > 0:
                for herb in self.sorted_animal_fitness['Herbivore']:
                    if np.random.random() > carn.probability_of_kill(herb):
                        if herb.weight >= carn.parameters['F']:
                            carn.animal_eats(carn.parameters['F'])
                        else:
                            carn.animal_eats(herb.weight)


class Jungle(Landscape):
    """
        Represents landscape covered by jungle cells
        There is no risk of over grazing
        Every year available fodder is maximum fodder(f_max)
    """
    is_migratable = True
    parameters = {'f_max': 800.0}

    def __init__(self, animals_list, given_params):
        # child class of Landscape
        super().__init__(animals_list)
        if given_params is not None:
            Fauna.set_parameters(given_params)
            self.parameters = Jungle.parameters
            self.remaining_fodder = self.parameters['f_max']

    def update_annual_fodder(self):
        # There is no overgrazing in jungle cells
        self.remaining_fodder = self.f_max


class Savannah(Landscape):
    """
    Represents the landscape  covered by savannah cells
    Here there is risk of over grazing
    Every year available folder in each cell is calculated manually
    """
    is_migratable = True

    def __init__(self, animals_list):
        # child class of Landscape
        super().__init__(animals_list)
        self.f_max = 300
        self.alpha = 0.3

        # At the start amount of fodder is maximum available
        self.remaining_fodder = self.f_max

    def update_annual_fodder(self):
        self.remaining_fodder += self.alpha * \
                                 (self.f_max - self.remaining_fodder)


class Desert(Landscape):
    """
        Represents the landscape covered by desert cells
        In these cells animals can migrate but there is no fodder available
    """
    is_migratable = True

    def __init__(self, animals_list):
        # child class of Landscape
        super().__init__(animals_list)
        self.f_max = 0
        self.remaining_fodder = self.f_max


class Mountain(Landscape):
    """
        Represents the landscape covered by mountain cells
        In these cells animals cannot migrate and there is no fodder
    """
    is_migratable = False

    def __init__(self, animals_list):
        # child class of Landscape
        super().__init__(animals_list)


class Ocean(Landscape):
    """
    Represents landscape covered by ocean cells
    In these cells animals cannot migrate and there is no fodder
    """
    is_migratable = False

    def __init__(self, animals_list):
        # child class of Landscape
        super().__init__(animals_list)
