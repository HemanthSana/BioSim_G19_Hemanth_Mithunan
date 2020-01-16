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


class Island:
    """
    Type of cell in island can be O for Ocean, S for Savannah,
    M for Mountain, J for Jungle, D for Desert
    """
    def __init__(self, geo_multiline_string, fauna_instance):
        """

        :param geo_multiline_string: Multiline String with characters
        ex: O, S, M, J, D
        """

        # better to use different file and
        # numpy array as discussed with daniel removethis

        self.geo_multiline_string = geo_multiline_string

        self.island_object_dict = {'O': Ocean, 'M': Mountain, 'D': Desert,
                                   'S': Savannah, 'J': Jungle}
        self.fauna_instance = fauna_instance

    def get_array_from_string(self):
        # cleaning to avoid garbage data
        geo_string = self.geo_multiline_string.replace(' ', '')

        # converting string to numpy 2D array
        geo_string_rows = geo_string.splitlines()
        geo_array = np.array([[col for col in row]
                              for row in geo_string_rows])

        # creating a numpy array with data type as object from landscape class
        geo_cell_type_array = np.empty(geo_array.shape, dtype=object)

        # changing the characters in array to objects
        # iterate through each element in the array
        for rows in np.arange(geo_array.shape[0]):
            for columns in np.arange(geo_array.shape[1]):
                # maps the char to class object to know which cell
                cell_type = self.island_object_dict[geo_array[rows][columns]]
                # instantiate the object of respective classes in the array
                geo_cell_type_array[rows][columns] = cell_type(
                    self.fauna_instance)

        return geo_cell_type_array

    def migrate(self):
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




        if 0:
            # splitting input string to lines i.e., rows
            self.rows = self.input_map.splitlines()

            # Check if all the cells are valid
            for row in self.rows:
                for cell in row:
                    if cell not in self.cell_list:
                        raise ValueError("Invalid Cell Type")

            # Check if all rows have equal length
            row_lengths = [len(row) for row in self.rows]
            for length in row_lengths:
                if length != row_lengths[0]:
                    raise ValueError("All rows must be of same length")

            # Check if the edge cells are Ocean
            # ToDo
            for row in self.rows:
                for cell in row[0, len(self.rows)-1]:
                    if cell != 'O':
                        raise ValueError("Ocean is not on the edges")
