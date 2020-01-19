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
    def __init__(self, island_map, ini_pop=None):
        """

        :param geo_multiline_string: Multiline String with characters
        ex: O, S, M, J, D
        """
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
        self.add_animals(ini_pop)

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

    # def adjacent_cells(self, map_array, x, y):
    #     rows = map_array.shape[0]
    #     cols = map_array.shape[1]


    def animal_migrates(self):
        island_array = self.get_array_from_string()
        horizontal = island_array[0]
        vertical = island_array[1]
        for x_cord in range(horizontal):
            for y_cord in range(vertical):
                current_cell = island_array[x_cord, y_cord]
                for animal in current_cell.animal_list:
                    if np.random.random() > animal.probability_of_move:
                        adj_cells = [island_array[x_cord - 1, y_cord],
                                     island_array[x_cord + 1, y_cord],
                                     island_array[x_cord, y_cord - 1],
                                     island_array[x_cord, y_cord + 1]]
                        list_of_probabilities = [
                            current_cell.move_probability
                            (cell, adj_cells, animal)
                            for cell in adj_cells]
                        max_probable_index = list_of_probabilities.index(
                            max(list_of_probabilities))
                        max_probable_cell = adj_cells[max_probable_index]

                        current_cell.remove_animal(animal)
                        max_probable_cell.add_animal(animal)
