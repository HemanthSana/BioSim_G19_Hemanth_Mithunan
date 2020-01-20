# -*- coding: utf-8 -*-

"""
Does all the graphics stuff
"""

_author_ = "Hemanth Sana & Mithunan Sivagnanam"
_email_ = "hesa@nmbu.no & misi@nmbu.no"

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np


class Graphics:
    map_colors = {
        "O": mcolors.to_rgba("navy"),
        "J": mcolors.to_rgba("forestgreen"),
        "S": mcolors.to_rgba("#e1ab62"),
        "D": mcolors.to_rgba("salmon"),
        "M": mcolors.to_rgba("lightslategrey"),
    }
    map_labels = {
        "O": "Ocean",
        "J": "Jungle",
        "S": "Savannah",
        "D": "Desert",
        "M": "Mountain",
    }

    def __init__(self, map_layout, figure, map_dimensions):
        self.map_layout = map_layout
        self.fig = figure
        self.map_dims = map_dimensions
        self.map_colors = Graphics.map_colors
        self.map_graph = None

    def generate_map_array(self):
        """
        Change the string to rgb image array
        :return: array
        """
        lines = self.map_layout.splitlines()
        if len(lines[-1]) == 0:
            lines = lines[:-1]

        num_cells = len(lines[0])
        map_array = []
        for line in lines:
            map_array.append([])
            if num_cells != len(line):
                raise ValueError(
                    "All lines in the map must have the same number of cells."
                )
            for letter in line:
                if letter not in self.map_colors:
                    raise ValueError('Not a valid landscape type')
                map_array[-1].append(self.map_colors[letter])

        return map_array

    def visualise_map(self):
        """
        create a map for island
        :return:
        """
        if self.map_graph is None:
            self.map_graph = self.fig.add_subplot(2, 2, 1)
            b, a = self.map_dims
            self.map_graph.imshow(self.generate_map_array())
            self.map_graph.set_xticks(range(0, a, 5))
            self.map_graph.set_xticklabels(range(0, a, 5))
            self.map_graph.set_yticks(range(0, b, 5))
            self.map_graph.set_yticklabels(range(0, b, 5))
            self.map_graph.set_title('Island')