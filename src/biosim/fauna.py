# -*- coding: utf-8 -*-

"""
"""
__author__ = "Hemanth Sana & Mithunan Sivagnanam"
__email__ = "hesa@nmbu.no & misi@nmbu.no"

import math
import numpy as np


class Fauna:
    def __init__(self, cell):
        """

        :param cell: We get this from landscape and put new animals
        """
        self.cell = cell
        # At the start age is zero
        self.age = 0
        self.weight = None
        self.parameters = None

    @property
    def weight(self):
        return self.weight

    @weight.setter
    def weight(self, value):
        self.weight = value

    def increase_weight(self, fodder_eaten):
        """

        :param fodder_eaten: Amount of fodder ate by animal in a year
        :return: amount of increase in weight
        """
        beta = self.parameters['beta']
        self.weight += beta * fodder_eaten

    def decrease_weight(self, const):
        self.weight -= const * self.weight

    def animal_grows(self):
        """
        age increases by one and weight decreases by a factor of eta annually
        """
        self.age += 1
        self.decrease_weight(self.parameters['eta'])

    @property
    def fitness(self):
        if self.weight > 0:
            q_age = 1 / (1 + math.e ** (self.parameters['phi_age'] *
                                        (self.age -
                                         self.parameters['a_half'])))
            q_weight = 1 / (1 + math.e ** (-(self.parameters['phi_weight'] *
                                             (self.weight -
                                              self.parameters['w_half']))))
            return q_age * q_weight
        else:
            return 0

    def migration(self):
        pass

    def animal_gives_birth(self, num_animals):
        num_animals = self.cell.num
        if self.weight >= self.parameters['zeta'] * \
                (self.parameters['w_birth'] + self.parameters['sigma_birth']):
            prob_birth = min(1,
                             self.parameters['gamma'] * self.fitness *
                             (num_animals - 1))
        else:
            prob_birth = 0

        # if prob_birth > np.random.random():
        #    return self.__class__()
        return prob_birth > np.random.random()

    # def changes_after_birth(self):
    #     if self.animal_gives_birth:
    #         self.num_animals += 1
    #         self.decrease_weight(self.parameters['xi'])

    @property
    def check_animal_dies(self):
        if self.fitness == 0:
            return True
        else:
            prob_death = self.parameters['omega'] * (1 - self.fitness)
            if prob_death > np.random.random():
                return True


class Carnivore(Fauna):
    def __init__(self, cell):
        super().__init__(cell)
        self.parameters = {'w_birth': 6.0, 'sigma_birth': 1.0, 'beta': 0.75,
                           'eta': 0.125, 'a_half': 60.0, 'phi_age': 0.4,
                           'w_half': 4.0, 'phi_weight': 0.4, 'mu': 0.4,
                           'lambda': 1.0, 'gamma': 0.8, 'zeta': 3.5,
                           'xi': 1.1, 'omega': 0.9, 'F': 50.0}

        if self.weight is None:
            self.weight = np.random.normal(self.parameters['w_birth'],
                                           self.parameters['sigma_birth'])


class Herbivore(Fauna):
    def __init__(self, cell):
        super().__init__(cell)
        self.parameters = {'w_birth': 8.0, 'sigma_birth': 1.5, 'beta': 0.9,
                           'eta': 0.05, 'a_half': 40.0, 'phi_age': 0.2,
                           'w_half': 10.0, 'phi_weight': 0.1, 'mu': 0.25,
                           'lambda': 1.0, 'gamma': 0.2, 'zeta': 3.5,
                           'xi': 1.2, 'omega': 0.4, 'F': 10.0}

        if self.weight is None:
            self.weight = np.random.normal(self.parameters['w_birth'],
                                           self.parameters['sigma_birth'])
