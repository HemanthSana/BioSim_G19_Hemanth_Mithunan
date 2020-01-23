# -*- coding: utf-8 -*-

"""
Tests for landscape.py
"""

__author__ = "Hemanth Sana & Mithunan Sivagnanam"
__email__ = "hesa@nmbu.no & misi@nmbu.no"

import pytest
from biosim.landscape import Desert, Ocean, Mountain, Savannah, Jungle
from biosim.fauna import Herbivore, Carnivore
import numpy as np


class TestLandscape:

    @pytest.fixture
    def animal_objects(self):
        np.random.seed(123)
        herb1 = Herbivore()
        herb2 = Herbivore()
        np.random.seed(123)
        carn1 = Carnivore()
        carn2 = Carnivore()
        print(herb1.weight, herb2.weight)
        return carn1, carn2, herb1, herb2

    @pytest.fixture
    def landscape_data(self, animal_objects):
        carn1, carn2, herb1, herb2 = animal_objects
        animals = {'Herbivore': [herb1, herb2], 'Carnivore': [carn1, carn2]}
        landscapes_dict = {'S': Savannah(),
                           'O': Ocean(),
                           'D': Desert(),
                           'M': Mountain(),
                           'J': Jungle()}
        for species, animals in animals.items():
            for animal in animals:
                landscapes_dict['S'].add_animal(animal)
                landscapes_dict['D'].add_animal(animal)
                landscapes_dict['J'].add_animal(animal)
        return landscapes_dict

    def test_order_by_fitness_herbivore(self, landscape_data):
        savannah = landscape_data['S']
        savannah.order_by_fitness()
        herb1 = savannah.fauna_list['Herbivore'][0]
        herb2 = savannah.fauna_list['Herbivore'][1]
        assert herb1.animal_fitness <= herb2.animal_fitness

    def test_order_by_fitness_carnivore(self, landscape_data):
        jungle = landscape_data['J']
        jungle.order_by_fitness()
        carn1 = jungle.fauna_list['Carnivore'][0]
        carn2 = jungle.fauna_list['Carnivore'][1]
        assert carn1.animal_fitness >= carn2.animal_fitness

    def test_add_animals(self, landscape_data):
        savannah = landscape_data['S']
        assert len(savannah.fauna_list['Herbivore']) == 2
        herb3 = Herbivore()
        savannah.add_animal(herb3)
        assert len(savannah.fauna_list['Herbivore']) == 3

    def test_remove_animal(self, landscape_data):
        savannah = landscape_data['S']
        herb3 = Herbivore()
        savannah.add_animal(herb3)
        assert len(savannah.fauna_list['Herbivore']) == 3
        savannah.remove_animal(herb3)
        assert len(savannah.fauna_list['Herbivore']) == 2

    def test_herbivore_eats_in_desert(self, landscape_data):
        desert = landscape_data['D']
        herb1 = desert.fauna_list['Herbivore'][0]
        # herb2 = desert.fauna_list['Herbivore'][1]
        herb1.weight_before_eat = herb1.weight
        desert.animal_eats()
        herb1.weight_after_eat = herb1.weight
        assert herb1.weight_after_eat == herb1.weight_before_eat

    def test_herbivore_eats_in_jungle_savannah(self, landscape_data):
        jungle = landscape_data['J']
        savannah = landscape_data['S']
        herb1 = jungle.fauna_list['Herbivore'][0]
        herb2 = savannah.fauna_list['Herbivore'][1]
        herb1.weight_before_eat = herb1.weight
        herb2.weight_before_eat = herb2.weight
        jungle.animal_eats()
        savannah.animal_eats()
        herb1.weight_after_eat = herb1.weight
        herb2.weight_after_eat = herb2.weight
        assert herb1.weight_after_eat >= herb1.weight_before_eat
        assert herb2.weight_after_eat >= herb2.weight_before_eat

    def test_relevant_food_herbivores(self, landscape_data):
        jungle = landscape_data['J']
        herb1 = jungle.fauna_list['Herbivore'][0]
        assert jungle.relevant_food(herb1) == jungle.remaining_food[
            'Herbivore']

    def test_relevant_food_carnivores(self, landscape_data):
        jungle = landscape_data['J']
        carn1 = jungle.fauna_list['Carnivore'][0]
        assert jungle.relevant_food(carn1) == sum(
            i.weight for i in jungle.fauna_list['Herbivore'])

    def test_relative_abundance_fodder_desert(self, landscape_data):
        desert = landscape_data['D']
        herb1 = desert.fauna_list['Herbivore'][0]
        assert desert.relative_abundance_fodder(herb1) == 0

    def test_propensity_to_move_ocean(self, landscape_data):
        ocean = landscape_data['O']
        desert = landscape_data['D']
        herb1 = desert.fauna_list['Herbivore'][0]
        assert ocean.propensity_to_move(herb1) == 0


class TestOcean:
    @pytest.fixture
    def ocean(self):
        return Ocean()

    def test_initiate_ocean(self, ocean):
        assert ocean

    def test_ocean_not_migratable(self, ocean):
        assert ocean.is_migratable is False

    def test_ocean_food_available(self, ocean):
        assert ocean.remaining_food['Herbivore'] == 0
        assert ocean.remaining_food['Carnivore'] == 0


class TestMountain:
    @pytest.fixture
    def mountain(self):
        return Mountain()

    def test_initiate_mountain(self, mountain):
        assert mountain

    def test_mountain_not_migratable(self, mountain):
        assert mountain.is_migratable is False

    def test_mountain_food_available(self, mountain):
        assert mountain.remaining_food['Herbivore'] == 0
        assert mountain.remaining_food['Carnivore'] == 0


class TestDesert:
    @pytest.fixture
    def desert(self):
        return Desert()

    def test_initiate_mountain(self, desert):
        assert desert

    def test_desert_not_migratable(self, desert):
        assert desert.is_migratable is True

    def test_desert_food_available(self, desert):
        assert desert.remaining_food['Herbivore'] == 0
        assert desert.remaining_food['Carnivore'] == 0
