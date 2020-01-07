# -*- coding: utf-8 -*-

"""
"""
_author_ = "Hemanth Sana & Mithunan Sivagnanam"
_email_ = "hesa@nmbu.no & misi@nmbu.no"

import math


class Fauna:
    def __init__(
            self,
            age,
            weight,
            phi_age,
            phi_weight,
            fit
    ):
        self.age = age
        self.weight = weight
        self.a_half = age/2
        self.w_half = weight/2
        self.phi_age = phi_age
        self.phi_weight = phi_weight
        self.fit = fit

    def fitness(self):
        if self.weight > 0:
            self.fit = (1/(1 + math.e**(self.phi_age
                                        (self.age - self.a_half)))) * \
                       (1/(1 + math.e**(-(self.phi_weight
                                        (self.weight - self.w_half)))))
        else:
            self.fit = 0

    def migration(self):
        pass

    def birth(self):
        pass

    def death(self):
        pass


class Carnivore:
    pass


class Herbivore:
    def __init__(self):
        pass