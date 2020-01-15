# -*- coding: utf-8 -*-

"""
"""
__author__ = "Hemanth Sana & Mithunan Sivagnanam"
__email__ = "hesa@nmbu.no & misi@nmbu.no"

import math
import numpy as np


class Fauna:
    def __init__(self):
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

    def animal_eats(self, food_eaten):
        self.weight += self.parameters['beta'] * food_eaten

    def animal_dies(self):
        pass

    @property
    def animal_fitness(self):
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

    @property
    def probability_of_move(self):
        return self.parameters['mu'] * self.animal_fitness

    @property
    def probability_of_birth(self):
        num_animals = self.num_animals
        if self.weight >= self.parameters['zeta'] * \
                (self.parameters['w_birth'] + self.parameters['sigma_birth']):
            return min(1, self.parameters['gamma'] * self.animal_fitness *
                             (num_animals - 1))
        else:
            return 0

    @property
    def probability_of_death(self):
        if self.animal_fitness == 0:
            return 1
        else:
            return self.weight * (1 - self.animal_fitness)


class Carnivore(Fauna):
    def __init__(self):
        super().__init__()
        self.parameters = {'w_birth': 6.0, 'sigma_birth': 1.0, 'beta': 0.75,
                           'eta': 0.125, 'a_half': 60.0, 'phi_age': 0.4,
                           'w_half': 4.0, 'phi_weight': 0.4, 'mu': 0.4,
                           'lambda': 1.0, 'gamma': 0.8, 'zeta': 3.5,
                           'xi': 1.1, 'omega': 0.9, 'F': 50.0,
                           'DeltaPhiMax' : 10.0}

        if self.weight is None:
            self.weight = np.random.normal(self.parameters['w_birth'],
                                           self.parameters['sigma_birth'])

    def probability_of_kill(self, herb):
        if self.fitness <= herb.fitness:
            return 0
        elif 0 < self.fitness - herb < self.parameters['DeltaPhiMax']:
            return (self.fitness - herb.fitness)/self.parameters['DeltaPhiMax']
        else:
            return 1


class Herbivore(Fauna):
    def __init__(self):
        super().__init__()
        self.parameters = {'w_birth': 8.0, 'sigma_birth': 1.5, 'beta': 0.9,
                           'eta': 0.05, 'a_half': 40.0, 'phi_age': 0.2,
                           'w_half': 10.0, 'phi_weight': 0.1, 'mu': 0.25,
                           'lambda': 1.0, 'gamma': 0.2, 'zeta': 3.5,
                           'xi': 1.2, 'omega': 0.4, 'F': 10.0}

        if self.weight is None:
            self.weight = np.random.normal(self.parameters['w_birth'],
                                           self.parameters['sigma_birth'])
