# -*- coding: utf-8 -*-

"""
Island class gives a geographical structure of the multiline string provided
It returns a numpy array with cell information
equal to no of characters in the given string
"""

__author__ = "Hemanth Sana & Mithunan Sivagnanam"
__email__ = "hesa@nmbu.no & misi@nmbu.no"

from biosim.landscape import *
import numpy as np
from biosim.fauna import Herbivore, Carnivore


class Island:
    """
    Type of cell in island can be O for Ocean, S for Savannah,
    M for Mountain, J for Jungle, D for Desert
    """
    def __init__(self, island_map):
        self.landscape_dict = {'O': Ocean,
                               'M': Mountain,
                               'D': Desert,
                               'S': Savannah,
                               'J': Jungle}
        self.fauna_dict = {'Herbivore': Herbivore,
                           'Carnivore': Carnivore}
        self.island_map = self.string_to_np_array(island_map)
        self.edge_condition(self.island_map)
        self.cell_type_map = self.create_array_with_landscape_objects()

    @property
    def map_dimensions(self):
        rows = self.cell_type_map.shape[0]
        cols = self.cell_type_map.shape[1]
        return rows, cols

    @staticmethod
    def string_to_np_array(map_str):
        map_str_clean = map_str.replace(' ', '')
        char_map = np.array(
            [[col for col in row] for row in map_str_clean.splitlines()])
        return char_map

    @staticmethod
    def edge_condition(map_array):
        rows = map_array.shape[0]
        cols = map_array.shape[1]
        map_edges = [map_array[0, :cols], map_array[rows - 1, :cols],
                     map_array[:rows - 1, 0], map_array[:rows - 1, cols - 1]]
        for edge in map_edges:
            if not np.all(edge == 'O'):
                raise ValueError('Edges of the map should have only '
                                 'Ocean cells')

    def create_array_with_landscape_objects(self):
        cell_type_array = np.empty(self.island_map.shape, dtype=object)
        for row in np.arange(self.island_map.shape[0]):
            for col in np.arange(self.island_map.shape[1]):
                cell_type = self.island_map[row][col]
                cell_type_array[row][col] = self.landscape_dict[cell_type]
        return cell_type_array

    def adjacent_cells(self, hor, ver):
        rows, cols = self.map_dimensions
        adj_cell_list = []
        if hor > 0:
            adj_cell_list.append(self.cell_type_map[hor - 1, ver])
        if hor + 1 < rows:
            adj_cell_list.append(self.cell_type_map[hor + 1, ver])
        if ver > 0:
            adj_cell_list.append(self.cell_type_map[hor, ver - 1])
        if ver + 1 < cols:
            adj_cell_list.append(self.cell_type_map[hor, ver + 1])
        return adj_cell_list

    @staticmethod
    def total_adj_cell_propensity(cells, animal):
        total_propensity = 0
        for cell in cells:
            total_propensity += cell.propensity_to_move(animal)
        return total_propensity

    def add_animals(self, pop):
        for animal_group in pop:
            loc = list(animal_group['loc'])
            animals = animal_group['pop']
            for animal in animals:
                species = animal['species']
                age = animal['age']
                weight = animal['weight']
                species_class = self.fauna_dict[species]
                animal_object = species_class(age, weight)
                cell = self.cell_type_map[loc]
                cell.add_animal(animal_object)

    def total_animals_per_species(self, species):
        num_animals = 0
        rows, cols = self.map_dimensions
        for hor in range(rows):
            for ver in range(cols):
                cell = self.cell_type_map[hor, ver]
                num_animals += len(cell.fauna_list[species])
        return num_animals

    def update(self):
        pass



