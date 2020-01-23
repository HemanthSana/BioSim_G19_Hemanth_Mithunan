# -*- coding: utf-8 -*-

"""
Tests for landscape.py
"""

__author__ = "Hemanth Sana & Mithunan Sivagnanam"
__email__ = "hesa@nmbu.no & misi@nmbu.no"

import pytest

from biosim.landscape import Ocean, Mountain
from biosim.island import Island


class TestIsland:
    def test_string_to_array(self):
        """
        testing the string_to_array method by verifying the individual cell
        and also by looking at the type of output
        """
        map_str = """   OOOOOOOOOOOO
                        OMSOODOOSMMO
                        OOOOOOOOOOOO"""
        island = Island(map_str)
        assert island.string_to_array()[0][0] == 'O'
        assert island.string_to_array()[1][10] == 'M'
        assert type(island.string_to_array()).__name__ == 'ndarray'

    def test_create_array_with_landscape_objects(self):
        """
        Testing create_array_with_landscape_objects by manually verifying
        if it returns instantiates correct cell object
        """
        map_str = """   OOOOOOOOOOOO
                        OMSOOOOOSMMO
                        OOOOOOOOOOOO"""
        island = Island(map_str)
        assert isinstance(island.create_array_with_landscape_objects()[0][0],
                          Ocean)
        assert isinstance(island.create_array_with_landscape_objects()[1][10],
                          Mountain)

    def test_adjacent_cells(self):
        """
        Testing if the adjacent_cells output is in the list of adjacent cells
        """
        map_str = """   OOOOOOOOOOOO
                        OMSOOOOOSMMO
                        OOOOOOOOOOOO"""
        island = Island(map_str)
        island.string_to_array()
        assert all(j in island.adjacent_cells(0, 0) for j in ['O', 'O'])

    def test_check_surrounded_by_ocean(self):
        """
        verifying if value error is raised when edges dont contain ocean cells
        """
        map_str = """   OOOOOOOJOOOO
                        OMSOOOOOSMMO
                        OOOOOOOOOOOO"""
        with pytest.raises(ValueError) as err:
            Island(map_str)
            assert err.type is ValueError

    def test_add_animals(self):
        """
        Testing add_animals and total_animals_per_species methods
        """
        map_str = """   OOOOOOOOOOOO
                        OMSOOOOOSMMO
                        OOOOOOOOOOOO"""
        island = Island(map_str)
        animals = [
            {
                "loc": (1, 1),
                "pop": [
                    {"species": "Herbivore", "age": 10, "weight": 10.0},
                    {"species": "Carnivore", "age": 11, "weight": 11.0},
                ],
            },
            {
                "loc": (1, 2),
                "pop": [
                    {"species": "Herbivore", "age": 10, "weight": 10.0},
                    {"species": "Herbivore", "age": 11, "weight": 11.0},
                    {"species": "Carnivore", "age": 12, "weight": 12.0},
                ],
            },
        ]
        island.add_animals(animals)
        assert island.total_animals_per_species('Herbivore') == 3
        assert island.total_animals_per_species('Carnivore') == 2
