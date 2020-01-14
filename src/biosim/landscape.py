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

import operator

class Landscape:
    """
    Parent class for type of landscape
    """
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
        

    def update_fodder(self):
        # each time herbivore eats available fodder should be calculated
        consumed_fodder = 0
        required_fodder = Herbivore(cell).parameters['F']

        if required_fodder <= self.available_fodder:
            consumed_fodder = required_fodder
            self.remaining_fodder = self.remaining_fodder - required_fodder
        else:
            consumed_fodder = self.available_fodder
            self.remaining_fodder = 0

        return consumed_fodder, self.remaining_fodder

    @property
    def available_fodder(self):
        return self.remaining_fodder


class Jungle(Landscape):
    """
        Represents landscape covered by jungle cells
        There is no risk of over grazing
        Every year available fodder is maximum fodder(f_max)
    """
    is_migratable = True

    def __init__(self, animals_list):
        # child class of Landscape
        super().__init__(animals_list)
        self.f_max = 800

        # At the start amount of fodder is maximum available
        self.remaining_fodder = self.f_max

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
