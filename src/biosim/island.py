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
    This is to represent the given map string as a array of objects
    """
    def __init__(self, island_map):
        self.map = island_map
        self.island_map = self.string_to_array()
        self.check_surrounded_by_ocean(self.island_map)

        self.landscape_dict = {'O': Ocean,
                               'M': Mountain,
                               'D': Desert,
                               'S': Savannah,
                               'J': Jungle}
        self.fauna_dict = {'Herbivore': Herbivore,
                           'Carnivore': Carnivore}

        self._cells = self.create_array_with_landscape_objects()

        rows = self._cells.shape[0]
        cols = self._cells.shape[1]
        self.map_dims = rows, cols

    @property
    def cells(self):
        """

        :return: Landscape objects
        """
        return self._cells

    def string_to_array(self):
        """
        This is to get a numpy array from the given multidimensional string
        :return: Numpy array
        """
        map_str_clean = self.map.replace(' ', '')
        char_map = np.array(
            [[col for col in row] for row in map_str_clean.splitlines()])
        return char_map

    @staticmethod
    def edges(map_array):
        """
        Gets the edges of the Map
        :param map_array: array
        :return: Edges of the map
        """
        rows, cols = map_array.shape[0], map_array.shape[1]
        map_edges = [map_array[0, :cols], map_array[rows - 1, :cols],
                     map_array[:rows - 1, 0], map_array[:rows - 1, cols - 1]]
        return map_edges

    def check_surrounded_by_ocean(self, map_array):
        """
        To check if the edge cells are only ocean
        :param map_array: island_map
        :return: Value error if edge is not Ocean
        """
        edges = self.edges(map_array)
        for edge in edges:
            if not np.all(edge == 'O'):
                raise ValueError('Edges of the map should have only '
                                 'Ocean cells')

    def create_array_with_landscape_objects(self):
        """
        To create an array of same size of the map but with
        objects of the classes according to the Cell letter
        :return: Array with landscape objects
        """
        cell_type_array = np.empty(self.island_map.shape, dtype=object)
        for row in np.arange(self.island_map.shape[0]):
            for col in np.arange(self.island_map.shape[1]):
                cell_type = self.island_map[row][col]
                cell_type_array[row][col] = self.landscape_dict[cell_type]()
        return cell_type_array

    def adjacent_cells(self, hor, ver):
        """
        This is to get the immediate adjacent cells of cell (hor, ver)
        :param hor: Number of rows
        :param ver: Number of cols
        :return: List with the 4 adj cells
        """
        rows, cols = self.map_dims
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
        """
        This is to add animals to the cells
        :param pop: Number of animals
        """
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
        """
        To get total number of Herbivores and Carnivores in all cells
        :param species: Str i.e, Herbivore or Carnivore
        :return:Number of animals
        """
        num_animals = 0
        rows, cols = self.map_dims
        for hor in range(rows):
            for ver in range(cols):
                cell = self._cells[hor, ver]
                num_animals += len(cell.fauna_list[species])
        return num_animals

    def life_cycle(self):
        """
        This iterates through all the cells and performs life cycle events
        this should be called every year
        """
        print('New Year')
        rows, cols = self.map_dims
        for row in range(rows):
            for col in range(cols):
                if self._cells[row, col].is_migratable:
                    self._cells[row, col].animal_eats()
                    self._cells[row, col].animals_gives_birth()
                    self._cells[row, col].animal_migrates(
                        self.adjacent_cells(row, col))
                    self._cells[row, col].grow_all_animals()
                    self._cells[row, col].animal_dies()
