# -*- coding: utf-8 -*-

"""
Contains Data of each cell, fodder functions and
animal list in each cell
"""

__author__ = "Hemanth Sana & Mithunan Sivagnanam"
__email__ = "hesa@nmbu.no & misi@nmbu.no"

from biosim.fauna import *
# from biosim.fauna import Herbivore
# from biosim.fauna import Carnivore

import math
import operator
import numpy as np


class Landscape:
    """
    Parent class for type of landscape
    """
    parameters = {}
    remaining_food = {}

    def __init__(self, animals_list):
        """

        :param animals_list: list of animals in the cell
        """
        self.sorted_animal_fitness = {}
        self.fauna_list = animals_list
        # self.remaining_food = {}

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

    def food_type(self, animal):
        species = animal.__class__.__name__
        return self.remaining_food[species]

    def give_birth(self, animal):
        num_animals = len(self.fauna_list[animal.__class__.__name__])
        if np.random.random() > animal.probability_of_birth(num_animals):
            baby_animal = animal.__class__.__name__()
            if animal.weight > (baby_animal.weight *
                                baby_animal.parameters['xi']):
                self.add_animal(baby_animal)
                animal.weight -= baby_animal * baby_animal.parameters['xi']

    def add_animal(self, animal):
        species = animal.__class__.__name__
        self.fauna_list[species].append(animal)

    def remove_animal(self, animal):
        species = animal.__class__.__name__
        self.fauna_list[species].remove(animal)

    def relative_abundance_fodder(self, animal):
        species = animal.__class__.__name__
        return self.food_type(animal) / ((len(self.fauna_list[species]) + 1)
                                         * animal.parameters['F'])

    def propensity_to_move(self, animal):
        if isinstance(self, Mountain) or isinstance(self, Ocean):
            return 0
        else:
            return math.exp(animal.parameters['lambda'] *
                            self.relative_abundance_fodder(animal))

    def move_probability(self, dest_cell, adj_cells, species):
        # ToDo
        # where to get cell information
        propensity_sum = 0
        for _ in adj_cells:
            propensity_sum += self.move_propensity(dest_cell, species)
        return self.move_propensity(dest_cell, species)/propensity_sum

    def herbivore_eats(self):
        self.order_by_fitness(self.fauna_list, 'Herbivore')
        for herb in self.sorted_animal_fitness['Herbivore']:
            herb_remaining_fodder = self.remaining_food['Herbivore']
            if herb_remaining_fodder == 0:
                break
            elif herb_remaining_fodder >= herb.parameters['F']:
                herb.animal_eats(herb.parameters['F'])
            elif 0 < herb_remaining_fodder < herb.parameters['F']:
                herb.animal_eats(herb_remaining_fodder)
                self.remaining_food['Herbivore'] = 0

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

    def animal_eats(self):
        self.update_fodder()
        self.herbivore_eats()
        self.carnivore_eats()

    def update_animal_weight_age(self):
        for animal in self.fauna_list:
            animal.animal_grows()

    def animal_gives_birth(self):
        for animal in self.fauna_list:
            if np.random.random() > animal.probability_of_birth:
                species = type(animal)
                offspring = species()
                animal.update_weight_after_birth(offspring)

    def animal_dies(self):
        for animal in self.fauna_list:
            if np.random.random() > animal.probability_of_death():
                self.remove_animal(animal)


class Jungle(Landscape):
    """
        Represents landscape covered by jungle cells
        There is no risk of over grazing
        Every year available fodder is maximum fodder(f_max)
    """
    is_migratable = True
    parameters = {'f_max': 800.0}

    def __init__(self, animals_list, given_params=None):
        # child class of Landscape
        super().__init__(animals_list)
        if given_params is not None:
            self.set_parameters(given_params)
        self.parameters = Jungle.parameters
        self.remaining_food['Herbivore'] = self.parameters['f_max']
        self.remaining_food['Carnivore'] = sum(herb.weight for herb in
                                               self.fauna_list['Herbivore'])

    @staticmethod
    def set_parameters(given_params):
        for param in given_params:
            if param in Jungle.parameters:
                Jungle.parameters[param] = \
                    given_params[param]
            else:
                raise ValueError('Parameter not in list' + str(param))

    def update_fodder(self):
        # There is no overgrazing in jungle cells
        self.remaining_food['Herbivore'] = self.parameters['f_max']


class Savannah(Landscape):
    """
    Represents the landscape  covered by savannah cells
    Here there is risk of over grazing
    Every year available folder in each cell is calculated manually
    """
    is_migratable = True
    parameters = {'f_max': 300.0, 'alpha': 0.3}

    def __init__(self, animals_list, given_params=None):
        # child class of Landscape
        super().__init__(animals_list)
        if given_params is not None:
            self.set_parameters(given_params)
        self.parameters = Savannah.parameters
        self.remaining_food['Herbivore'] = self.parameters['f_max']
        self.remaining_food['Carnivore'] = sum(herb.weight for herb in
                                               self.fauna_list['Herbivore'])

    @staticmethod
    def set_parameters(given_params):
        for param in given_params:
            if param in Savannah.parameters:
                Savannah.parameters[param] = \
                    given_params[param]
            else:
                raise ValueError('Parameter not in list' + str(param))

    def update_fodder(self):
        self.remaining_food['Herbivore'] += self.parameters['alpha'] * \
                                 (self.parameters['f_max'] -
                                  self.remaining_food['Herbivore'])


class Desert(Landscape):
    """
        Represents the landscape covered by desert cells
        In these cells animals can migrate but there is no fodder available
    """
    is_migratable = True
    remaining_food = {'Herbivore': 0}

    def __init__(self, animals_list):
        # child class of Landscape
        super().__init__(animals_list)
        self.f_max = 0
        self.remaining_food['Herbivore'] = Desert.remaining_food['Herbivore']
        self.remaining_food['Carnivore'] = sum(herb.weight for herb in
                                               self.fauna_list['Herbivore'])


class Mountain(Landscape):
    """
        Represents the landscape covered by mountain cells
        In these cells animals cannot migrate and there is no fodder
    """
    is_migratable = False
    remaining_food = {'Herbivore': 0, 'Carnivore': 0}
    animals_list = {'Herbivore': [], 'Carnivore': []}

    def __init__(self, animals_list=None):
        # child class of Landscape
        super().__init__(animals_list)
        if animals_list is not None:
            raise ValueError('Animals cannot be in Mountain')
        self.remaining_food['Herbivore'] = Mountain.remaining_food['Herbivore']
        self.remaining_food['Carnivore'] = Mountain.remaining_food['Carnivore']
        self.animals_list['Herbivore'] = Mountain.animals_list['Herbivore']
        self.animals_list['Carnivore'] = Mountain.animals_list['Carnivore']


class Ocean(Landscape):
    """
    Represents landscape covered by ocean cells
    In these cells animals cannot migrate and there is no fodder
    """
    is_migratable = False
    remaining_food = {'Herbivore': 0, 'Carnivore': 0}
    animals_list = {'Herbivore': [], 'Carnivore': []}

    def __init__(self, animals_list=None):
        # child class of Landscape
        super().__init__(animals_list)
        if animals_list is not None:
            raise ValueError('Animals cannot be in Ocean')
        self.remaining_food['Herbivore'] = Ocean.remaining_food['Herbivore']
        self.remaining_food['Carnivore'] = Ocean.remaining_food['Carnivore']
        self.animals_list['Herbivore'] = Ocean.animals_list['Herbivore']
        self.animals_list['Carnivore'] = Ocean.animals_list['Carnivore']
