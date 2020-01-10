# -*- coding: utf-8 -*-

"""
"""
author = "Hemanth Sana & Mithunan Sivagnanam"
email = "hesa@nmbu.no & misi@nmbu.no"

import math
import numpy as np


class Fauna:
    w_birth = None

    def __init__(self, cell):
        self.cell = cell
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

    def decrease_weight(self):
        eta = self.parameters['eta']
        self.weight -= eta * self.weight

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

    def birth(self, num_animals):
        if self.weight >= self.parameters['zeta'] * \
                (self.parameters['w_birth'] + self.parameters['sigma_birth']):
            prob_birth = min(1,
                             self.parameters['gamma'] * self.fitness *
                             (num_animals - 1))
        else:
            prob_birth = 0

        return prob_birth > np.random.random()

    @property
    def death(self):
            return True
        if self.fitness == 0:
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


class Herbivore(Fauna):
    def __init__(self, cell):
        super().__init__(cell)
        self.parameters = {'w_birth': 8.0, 'sigma_birth': 1.5, 'beta': 0.9,
                           'eta': 0.05, 'a_half': 40.0, 'phi_age': 0.2,
                           'w_half': 10.0, 'phi_weight': 0.1, 'mu': 0.25,
                           'lambda': 1.0, 'gamma': 0.2, 'zeta': 3.5,
                           'xi': 1.2, 'omega': 0.4, 'F': 10.0}

        if self.weight is None:
            self.weight = np.random.normal(self.parameters['w_birth'], self.parameters['sigma_birth'])