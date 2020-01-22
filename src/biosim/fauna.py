# -*- coding: utf-8 -*-

"""
"""
__author__ = "Hemanth Sana & Mithunan Sivagnanam"
__email__ = "hesa@nmbu.no & misi@nmbu.no"

import math
import numpy as np


class Fauna:
    """
    Fauna Base Class for Herbivore and Carnivore
    """
    parameters = {}

    def __init__(self, age=None, weight=None):
        """
        Constructor for base class
        weight of the animal at birth is calculated accordingly
        :param age: age is of type integer
        :param weight: weight can be floating point value
        """
        if age is None:
            self.age = 0
        else:
            self.age = age
        if weight is None:
            self.weight = np.random.normal(self.parameters['w_birth'],
                                           self.parameters['sigma_birth'])
        else:
            self.weight = weight
        self.fitness = 0
        self.gives_birth = False

    @property
    def animal_weight(self):
        """

        :return: value of weight
        """
        return self.weight

    def increase_animal_weight(self, fodder_eaten):
        """
        Calculates the increase in animal weight according to the food eaten
        :param fodder_eaten: Amount of fodder ate by animal in a year
        :return: amount of increase in weight
        """
        self.weight += self.parameters['beta'] * fodder_eaten

    def decrease_animal_weight(self, const):
        """
        Every year weight of animal decreases by certain factor
        :param const: factor by which weight decreases every year(eta)
        :return: Reduced weight
        """
        self.weight -= const * self.weight

    def animal_grows(self):
        """
        age increases by one and weight decreases by a factor of eta annually
        """
        self.age += 1
        self.decrease_animal_weight(self.parameters['eta'])

    def animal_eats(self, food_eaten):
        """
        Increases animal weight according to food eaten
        :param food_eaten: amount of food depends on species
        :return: increased weight
        """
        self.increase_animal_weight(food_eaten)

    @property
    def animal_fitness(self):
        """
        Calculates and returns fitness value of animal.
        It is calculated by the formula given in instructions
        Phi = q(-1, a, a_half, phi_age)*q(+1, w, w_half, phi_weight)
        Uses parameters phi_age, a_half, phi_weight, w_half to calculate
        :return: fitness value
        """
        if self.weight > 0:
            q_age = 1 / (1 + math.exp(self.parameters['phi_age'] *
                                      (self.age - self.parameters['a_half'])))
            q_weight = 1 / (1 + math.exp(-1 * (self.parameters['phi_weight'] *
                                               (self.weight -
                                                self.parameters['w_half']))))
            return q_age * q_weight
        else:
            return 0

    def probability_of_birth(self, num_animals):
        """
        Probability by which animal gives birth is calculated
        It should be calculated only if atleast 2 animals of same species are
        in cell
        :param num_animals: Number of animals of same species in cell
        :return: Bool
        """
        if num_animals >= 2 and self.weight >= self.parameters['zeta'] * \
                (self.parameters['w_birth'] + self.parameters['sigma_birth']):
            return np.random.random() < min(1, self.parameters['gamma'] *
                                            self.animal_fitness *
                                            (num_animals - 1))
        else:
            return False

    def update_weight_after_birth(self, offspring):
        """
        Weight of the animal decreases xi times the weight of offspring
        :param offspring: object either Herbivore or Carnivore
        :return: decreased weight after birth
        """
        if self.weight > offspring.weight * offspring.parameters['xi']:
            self.weight -= offspring.weight * offspring.parameters['xi']
        self.gives_birth = True

    def probability_of_death(self):
        """
        Death probability depends on the fitness of the animal
        If the fitness is 0 probability is 1
        :return: a floating point value
        """
        if self.animal_fitness == 0:
            return False
        else:
            return np.random.random() < self.parameters['omega'] * \
                   (1 - self.animal_fitness)

    @property
    def probability_of_move(self):
        """

        :return: probability value in floating point
        """
        return np.random.random() < self.parameters['mu'] * self.animal_fitness

    @classmethod
    def set_parameters(cls, given_params):
        """
        Sets the parameters given according to classes called
        :param given_params: a dictionary of user provided parameters
        :return: Assigns the parameters to respective classes
        """
        for param in given_params:
            if param in cls.parameters:
                if given_params[param] <= 0:
                    raise ValueError('Parameter value should be positive')
                else:
                    cls.parameters[param] = given_params[param]
            else:
                raise ValueError('Parameter not in class parameter list')


class Carnivore(Fauna):
    """
    Child class of Fauna
    """
    parameters = {'w_birth': 6.0, 'sigma_birth': 1.0, 'beta': 0.75,
                  'eta': 0.125, 'a_half': 60.0, 'phi_age': 0.4,
                  'w_half': 4.0, 'phi_weight': 0.4, 'mu': 0.4,
                  'lambda': 1.0, 'gamma': 0.8, 'zeta': 3.5,
                  'xi': 1.1, 'omega': 0.9, 'F': 50.0,
                  'DeltaPhiMax': 10.0}

    def __init__(self, age=None, weight=None):
        super().__init__(age, weight)
        self.parameters = Carnivore.parameters

    def probability_of_kill(self, herb):
        """
        Returns the probability with which carnivore kills herbivore
        If fitness of carnivore less than herbivore we return 0
        If the difference in fitness is > 0 and < DeltaPhiMax then it is
        calculated as Difference/ DeltaPhiMax
        :param herb: Herbivore class object
        :return:probability value
        """
        if self.animal_fitness <= herb.animal_fitness:
            return 0
        elif 0 < self.animal_fitness - herb.animal_fitness < \
                self.parameters['DeltaPhiMax']:
            return (self.animal_fitness - herb.animal_fitness) / \
                   self.parameters['DeltaPhiMax']
        else:
            return 1


class Herbivore(Fauna):
    """
    Child class of Fauna
    """
    parameters = {'w_birth': 8.0, 'sigma_birth': 1.5, 'beta': 0.9,
                  'eta': 0.05, 'a_half': 40.0, 'phi_age': 0.2,
                  'w_half': 10.0, 'phi_weight': 0.1, 'mu': 0.25,
                  'lambda': 1.0, 'gamma': 0.2, 'zeta': 3.5,
                  'xi': 1.2, 'omega': 0.4, 'F': 10.0}

    def __init__(self, age=None, weight=None):
        super().__init__(age, weight)
        self.parameters = Herbivore.parameters
