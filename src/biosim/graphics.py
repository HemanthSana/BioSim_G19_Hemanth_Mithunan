# -*- coding: utf-8 -*-

"""
Does all the graphics stuff
"""

__author__ = "Hemanth Sana & Mithunan Sivagnanam"
__email__ = "hesa@nmbu.no & misi@nmbu.no"

import numpy as np
import matplotlib.colors as mcolors


class Graphics:
    map_colors = {
        "O": mcolors.to_rgba("navy"),
        "J": mcolors.to_rgba("forestgreen"),
        "S": mcolors.to_rgba("springgreen"),
        "D": mcolors.to_rgba("navajowhite"),
        "M": mcolors.to_rgba("lightslategrey"),
    }
    map_labels = {
        "O": "Ocean",
        "J": "Jungle",
        "S": "Savannah",
        "D": "Desert",
        "M": "Mountain",
    }

    def __init__(self, map_layout, figure, map_dims):
        self.map_layout = map_layout
        self.fig = figure
        self.map_dims = map_dims
        self.map_colors = Graphics.map_colors
        self.map_graph = None
        self.herbivore_curve = None
        self.carnivore_curve = None
        self.herbivore_dist = None
        self.carnivore_dist = None
        self.mean_ax = None
        self.herbivore_image_axis = None
        self.carnivore_image_axis = None

    def generate_map(self):
        """
        Change the string to image array
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

    def generate_island_graph(self):
        """
        Generates a map for island in subplot (2, 2, 1)
        """
        if self.map_graph is None:
            self.map_graph = self.fig.add_subplot(2, 2, 1)
            self.map_graph.imshow(self.generate_map())
            self.map_graph.set_title('Island')

    def generate_herbivore_graph(self, final_year, recreate=False):
        """
        Generates a line graph for herbivores
        """
        if (self.herbivore_curve is None) or recreate:
            plot = self.mean_ax.plot(np.arange(0, final_year),
                                     np.full(final_year, np.nan))
            self.herbivore_curve = plot[0]
        else:
            x_data, y_data = self.herbivore_curve.get_data()
            x_new = np.arange(x_data[-1] + 1, final_year)
            if len(x_new) > 0:
                y_new = np.full(x_new.shape, np.nan)
                self.herbivore_curve.set_data(np.hstack((x_data, x_new)),
                                              np.hstack((y_data, y_new)))

    def generate_carnivore_graph(self, final_year, recreate=False):
        """
        Generates a line graph for carnivores
        """
        if (self.carnivore_curve is None) or recreate:
            plot = self.mean_ax.plot(np.arange(0, final_year),
                                     np.full(final_year, np.nan))
            self.carnivore_curve = plot[0]
        else:
            x_data, y_data = self.carnivore_curve.get_data()
            x_new = np.arange(x_data[-1] + 1, final_year)
            if len(x_new) > 0:
                y_new = np.full(x_new.shape, np.nan)
                self.carnivore_curve.set_data(np.hstack((x_data, x_new)),
                                              np.hstack((y_data, y_new)))

    def update_graphs(self, year, herb_count, carn_count):
        """
        Updates graphs according to number of years and animals count
        in subplot(2, 2, 2)
        """
        herb_ydata = self.herbivore_curve.get_ydata()
        herb_ydata[year] = herb_count
        self.herbivore_curve.set_ydata(herb_ydata)

        carn_ydata = self.carnivore_curve.get_ydata()
        carn_ydata[year] = carn_count
        self.carnivore_curve.set_ydata(carn_ydata)

    def generate_animal_graphs(self, final_year, y_lim, recreate=False):
        """
        Generates separate line graphs for Herbivores and Carnivores
        """
        if self.mean_ax is None:
            self.mean_ax = self.fig.add_subplot(2, 2, 2)
            self.mean_ax.set_ylim(0, y_lim)

        self.mean_ax.set_xlim(0, final_year + 1)
        self.generate_herbivore_graph(final_year, recreate=recreate)
        self.generate_carnivore_graph(final_year, recreate=recreate)
        self.mean_ax.set_title('Animal Graphs')

    def animal_dist_graphs(self):
        """
        Creates the distribution graphs for herbivore and
        carnivore distribution
        """
        if self.herbivore_dist is None:
            self.herbivore_dist = self.fig.add_subplot(2, 2, 3)
            self.herbivore_image_axis = None

        if self.carnivore_dist is None:
            self.carnivore_dist = self.fig.add_subplot(2, 2, 4)
            self.carnivore_image_axis = None

    def update_herbivore_dist(self, distribution):
        """
        Updates herbivore distribution in subplot (2, 2, 3)
        """
        if self.herbivore_image_axis is not None:
            self.herbivore_image_axis.set_data(distribution)
        else:
            y, x = self.map_dims
            self.herbivore_dist.imshow(distribution,
                                       interpolation='nearest',
                                       vmin=0, vmax=5)
            # self.herbivore_dist.set_xticks(range(0, x, 5))
            # self.herbivore_dist.set_xticklabels(range(1, x + 1, 5))
            # self.herbivore_dist.set_yticks(range(0, y, 5))
            # self.herbivore_dist.set_yticklabels(range(1, y + 1, 5))
            self.herbivore_dist.set_title('Herbivore Distribution')

    def update_carnivore_dist(self, distribution):
        """
        updates Carnivore distribution subplot (2, 2, 4)
        """
        if self.carnivore_image_axis is not None:
            self.carnivore_image_axis.set_data(distribution)
        else:
            y, x = self.map_dims
            self.carnivore_dist.imshow(distribution,
                                       interpolation='nearest',
                                       vmin=0, vmax=5)
            # self.carnivore_dist.set_xticks(range(0, x, 5))
            # self.carnivore_dist.set_xticklabels(range(1, 1 + x, 5))
            # self.carnivore_dist.set_yticks(range(0, y, 5))
            # self.carnivore_dist.set_yticklabels(range(1, 1 + y, 5))
            self.carnivore_dist.set_title('Carnivore Distribution')

    def set_year(self, year):
        """
        Set the year on the Figure
        """
        self.fig.suptitle('Graphics for Year: ' + str(year), x=0.5)
