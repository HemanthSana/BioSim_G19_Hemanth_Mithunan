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
    @pytest.fixture
    def animal_objects(self):
        np.random.seed(123)
        herb = Herbivore()
        herb.set_parameters(Herbivore.parameters)
        np.random.seed(123)
        carn = Carnivore()
        carn.set_parameters(Carnivore.parameters)
        return herb, carn

    def test_animal_birth_weight(self, animal_objects):
        """
        Test if calculated weight is correctly calculated
        """
        herb, carn = animal_objects
        assert herb.weight == 6.3715540950491585
        assert carn.weight == 4.914369396699438

    def test_age_increase(self, animal_objects):
        """
        Testing increase in weight as animal grows
        """
        herb, carn = animal_objects
        assert herb.age == 0
        assert carn.age == 0
        for _ in range(5):
            herb.animal_grows()
        for _ in range(4):
            carn.animal_grows()
        assert herb.age == 5
        assert carn.age == 4

    def test_animal_growth_decrease_weight(self, animal_objects):
        """
        Check if animal weight is decreased after growing
        """
        herb, carn = animal_objects
        herb_initial_weight = herb.weight
        carn_initial_weight = carn.weight
        herb.animal_grows()
        carn.animal_grows()
        herb_final_weight = herb.weight
        carn_final_weight = carn.weight
        assert herb_final_weight < herb_initial_weight
        assert carn_final_weight < carn_initial_weight

    def test_decrease_weight(self, animal_objects):
        """
        Test if animal weight is decreased by the factor given
        """
        herb, carn = animal_objects
        herb_initial_weight = herb.weight
        carn_initial_weight = carn.weight
        herb.decrease_animal_weight(0.5)
        carn.decrease_animal_weight(0.5)
        herb_final_weight = herb.weight
        carn_final_weight = carn.weight
        assert herb_final_weight == 0.5 * herb_initial_weight
        assert carn_final_weight == 0.5 * carn_initial_weight

    def test_animal_eats_and_increase_weight(self, animal_objects):
        """
        Check if animal weight increases after eating
        """
        herb, carn = animal_objects
        herb_initial_weight = herb.weight
        carn_initial_weight = carn.weight
        herb.animal_eats(10)
        carn.animal_eats(10)
        herb_final_weight = herb.weight
        carn_final_weight = carn.weight
        assert herb_final_weight > herb_initial_weight
        assert carn_final_weight > carn_initial_weight

    def test_animal_fitness_value_between_0_and_1(self, animal_objects):
        """
        Check if fitness value is between 0 and 1
        """
        herb, carn = animal_objects
        assert 0 <= herb.animal_fitness <= 1
        assert 0 <= carn.animal_fitness <= 1

    def test_probability_of_birth_if_only_one_animal(self, animal_objects):
        """
        Testing probability of birth returns False when only
        one animal is present
        """
        herb, carn = animal_objects
        assert carn.probability_of_birth(1) is False
        assert herb.probability_of_birth(1) is False

    def test_probability_of_birth_for_more_than_2(self, animal_objects):
        herb, carn = animal_objects
        np.random.seed(123)
        carn.set_parameters({'gamma': 1000})
        herb.set_parameters({'gamma': 0.000001})
        assert carn.probability_of_birth(20) is True
        assert herb.probability_of_birth(30) is True

    def test_probability_of_death(self, animal_objects):
        """
        testing probability of death by manipulating the value of mu
        """
        herb, carn = animal_objects
        carn.set_parameters({'mu': 100})
        herb.set_parameters({'mu': 0.0001})
        assert carn.probability_of_death()
        assert not herb.probability_of_death()

    def test_probability_of_move(self, animal_objects):
        """
        Testing by setiing mu higher so that probability_of_move
        will return True
        """
        herb, carn = animal_objects
        assert not herb.probability_of_move
        carn.set_parameters({'mu': 100})
        assert carn.probability_of_move

    def test_set_parameters(self, animal_objects):
        """
        testing set_parameters method by changing the parameters and comparing
        before and after set values
        """
        herb, carn = animal_objects
        eta_before_set = Herbivore.parameters['eta']
        xi_before_set = Carnivore.parameters['xi']
        herb_param = {'eta': 0.4}
        carn_param = {'xi': 1.1}
        herb.set_parameters(herb_param)
        carn.set_parameters(carn_param)
        assert eta_before_set != herb.parameters['eta']
        assert xi_before_set == carn.parameters['xi']


class TestHerbivore:
    """
    Tests for Herbivore class
    """
    pass


class TestCarnivore(TestFauna):
    """
    Tests for Carnivore class
    """
    def test_kill_probability(self, animal_objects):
        """
        The given weights shows that the herb is more fit than the carn.
        so, the probability should be false.

        """
        np.random.seed(123)
        carn = Carnivore(weight=10)
        herb = Herbivore(weight=100)
        assert not carn.probability_of_kill(herb)
