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
        self.island_map = self.string_to_np_array(island_map)
        self.check_surrounded_by_ocean(self.island_map)

        self.landscape_dict = {'O': Ocean,
                               'M': Mountain,
                               'D': Desert,
                               'S': Savannah,
                               'J': Jungle}
        self.fauna_dict = {'Herbivore': Herbivore,
                           'Carnivore': Carnivore}

        self._cells = self.create_array_with_landscape_objects()

    @property
    def cells(self):
        return self._cells

    @property
    def map_dimensions(self):
        rows = self._cells.shape[0]
        cols = self._cells.shape[1]
        return rows, cols

    def instantiate_cell(self, cell_letter):
        return self.landscape_dict[cell_letter]()

    @staticmethod
    def string_to_np_array(map_str):
        map_str_clean = map_str.replace(' ', '')
        char_map = np.array(
            [[col for col in row] for row in map_str_clean.splitlines()])
        return char_map

    @staticmethod
    def edges(map_array):
        rows, cols = map_array.shape[0], map_array.shape[1]
        map_edges = [map_array[0, :cols], map_array[rows - 1, :cols],
                     map_array[:rows - 1, 0], map_array[:rows - 1, cols - 1]]
        return map_edges

    def check_surrounded_by_ocean(self, map_array):
        edges = self.edges(map_array)
        for edge in edges:
            if not np.all(edge == 'O'):
                raise ValueError('Edges of the map should have only '
                                 'Ocean cells')

    def create_array_with_landscape_objects(self):
        cell_type_array = np.empty(self.island_map.shape, dtype=object)
        for row in np.arange(self.island_map.shape[0]):
            for col in np.arange(self.island_map.shape[1]):
                cell_type = self.island_map[row][col]
                cell_type_array[row][col] = self.instantiate_cell(cell_type)
        return cell_type_array

    def adjacent_cells(self, hor, ver):
        rows, cols = self.map_dimensions
        adj_cell_list = []
        if hor > 0:
            adj_cell_list.append(self._cells[hor - 1, ver])
        if hor + 1 < rows:
            adj_cell_list.append(self._cells[hor + 1, ver])
        if ver > 0:
            adj_cell_list.append(self._cells[hor, ver - 1])
        if ver + 1 < cols:
            adj_cell_list.append(self._cells[hor, ver + 1])
        return adj_cell_list

    def add_animals(self, pop):
        for animal_group in pop:
            loc = animal_group['loc']
            animals = animal_group['pop']
            for animal in animals:
                species = animal['species']
                age = animal['age']
                weight = animal['weight']
                species_class = self.fauna_dict[species]
                animal_object = species_class(age=age, weight=weight)
                cell = self._cells[loc]
                cell.add_animal(animal_object)

    def total_animals_per_species(self, species):
        num_animals = 0
        rows, cols = self.map_dimensions
        for hor in range(rows):
            for ver in range(cols):
                cell = self._cells[hor, ver]
                num_animals += len(cell.fauna_list[species])
        return num_animals

    def update(self):
        rows, cols = self.map_dimensions
        annual_cycle = ['cell.animal_eats', 'cell.animal_gives_birth',
                        'cell.animal_migrates', 'cell.grow_all_animals',
                        'cell.animal_dies']
        for life_event in annual_cycle:
            for row in range(rows):
                for col in range(cols):
                    cell = self._cells[row, col]
                    stage_to_call = eval(life_event)

    def life_cycle(self):
        print('year')
        for [x, y], cell in np.ndenumerate(self._cells):
            cell.animals_eat()
            cell.animal_gives_birth()
            cell.animal_migrates()
            cell.grow_all_animals()
            cell.animal_dies()