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
        """

        :return: Pass if weight after the function call is decreased
        """
        seed(123)
        herb = Herbivore(Herbivore.parameters)
        seed(123)
        carn = Carnivore(Carnivore.parameters)
        herb_initial_weight = herb.weight
        carn_initial_weight = carn.weight
        herb.animal_grows()
        carn.animal_grows()
        herb_final_weight = herb.weight
        carn_final_weight = carn.weight
        assert herb_final_weight < herb_initial_weight
        assert carn_final_weight < carn_initial_weight

    def test_age_increase(self):
        """

        :return: Pass if age increases by the as many times
        animal_grows() function called
        """
        herb = Herbivore(Herbivore.parameters)
        carn = Carnivore(Carnivore.parameters)
        assert herb.age == 0
        assert carn.age == 0
        for _ in range(5):
            herb.animal_grows()
        for _ in range(4):
            carn.animal_grows()
        assert herb.age == 5
        assert carn.age == 4

    def test_birth_weight(self):
        """

        :return: pass if weight after calling the class is equal to
        the calculated weight
        """
        seed(123)
        herb = Herbivore(Herbivore.parameters)
        seed(123)
        carn = Carnivore(Carnivore.parameters)
        assert herb.weight == np.random.normal(
            Herbivore.parameters['w_birth'],
            Herbivore.parameters['sigma_birth'])
        assert carn.weight == np.random.normal(
            Carnivore.parameters['w_birth'],
            Carnivore.parameters['sigma_birth'])

    def test_decrease_weight(self):
        """

        :return: Pass if weight after the function call is less by factor given
        """
        seed(123)
        herb = Herbivore(Herbivore.parameters)
        seed(123)
        carn = Carnivore(Carnivore.parameters)
        herb_initial_weight = herb.weight
        carn_initial_weight = carn.weight
        herb.decrease_animal_weight(0.5)
        carn.decrease_animal_weight(0.5)
        herb_final_weight = herb.weight
        carn_final_weight = carn.weight
        assert herb_final_weight == 0.5 * herb_initial_weight
        assert carn_final_weight == 0.5 * carn_initial_weight

    def test_animal_eats(self):
        """

        :return: Pass if weight after animal eats food is higher than before
        """
        seed(123)
        herb = Herbivore(Herbivore.parameters)
        seed(123)
        carn = Carnivore(Carnivore.parameters)
        herb_initial_weight = herb.weight
        carn_initial_weight = carn.weight
        herb.animal_eats(10)
        carn.animal_eats(10)
        herb_final_weight = herb.weight
        carn_final_weight = carn.weight
        assert herb_final_weight > herb_initial_weight
        assert carn_final_weight > carn_initial_weight

    def test_animal_fitness_value(self):
        """

        :return: Pass if fitness value is calculated correctly
        """
        seed(123)
        herb = Herbivore(Herbivore.parameters)
        seed(123)
        carn = Carnivore(Carnivore.parameters)
        assert 0 <= herb.animal_fitness <= 1
        assert 0 <= carn.animal_fitness <= 1

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
