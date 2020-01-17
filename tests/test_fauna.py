# -*- coding: utf-8 -*-

"""
Unit tests for methods in fauna.py
"""

__author__ = "Hemanth Sana & Mithunan Sivagnanam"
__email__ = "hesa@nmbu.no & misi@nmbu.no"

import pytest
from biosim.fauna import Herbivore, Carnivore
from random import seed
import numpy as np


class TestFauna:
    def test_animal_grows(self):
        herb_params = {'eta': 0.05, 'w_birth': 8.0, 'sigma_birth': 1.5}
        seed(123)
        herb = Herbivore(herb_params)
        carn_params = {'eta': 0.125, 'w_birth': 6.0, 'sigma_birth': 1.1}
        seed(123)
        carn = Carnivore(carn_params)
        herb_initial = herb.weight
        carn_initial = carn.weight
        herb.animal_grows()
        carn.animal_grows()
        herb_final = herb.weight
        carn_final = carn.weight
        assert herb_final < herb_initial
        assert carn_final < carn_initial

    def test_age_increase(self):
        herb_params = {}
        herb = Herbivore(herb_params)
        carn_params = {}
        carn = Carnivore(carn_params)
        assert herb.age == 0
        assert carn.age == 0
        for _ in range(5):
            herb.animal_grows()
        for _ in range(4):
            carn.animal_grows()
        assert herb.age == 5
        assert carn.age == 4

    def test_birth_weight(self):
        seed(123)
        herb_params = {'w_birth': 8.0, 'sigma_birth': 1.5}
        herb = Herbivore(herb_params)
        seed(123)
        carn_params = {'w_birth': 6.0, 'sigma_birth': 1.1}
        carn = Carnivore(carn_params)
        assert herb.weight == np.random.normal(herb_params['w_birth'],
                                               herb_params['sigma_birth'])
        assert carn.weight == np.random.normal(carn_params['w_birth'],
                                               carn_params['sigma_birth'])

    def test_decrease_weight(self):
        herb_params = {'w_birth': 8.0, 'sigma_birth': 1.5}
        carn_params = {'w_birth': 6.0, 'sigma_birth': 1.1}
        herb = Herbivore(herb_params)
        carn = Carnivore(carn_params)
        herb_initial_weight = herb.weight
        carn_initial_weight = carn.weight
        herb.decrease_animal_weight(0.5)
        carn.decrease_animal_weight(0.5)
        herb_final_weight = herb.weight
        carn_final_weight = carn.weight
        assert herb_final_weight == 0.5 * herb_initial_weight
        assert carn_final_weight == 0.5 * carn_initial_weight

    def test_animal_eats(self):
        pass

    def test_animal_fitness(self):
        pass

    def test_probability_of_move(self):
        pass

    def test_probability_of_birth(self):
        pass

    def test_probability_of_death(self):
        pass

    def test_set_parameters(self):
        pass


class TestHerbivore:
    pass


class TestCarnivore:
    pass









