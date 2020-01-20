# -*- coding: utf-8 -*-

"""
Simulates the whole project
"""

__author__ = "Hemanth Sana & Mithunan Sivagnanam"
__email__ = "hesa@nmbu.no & misi@nmbu.no"

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from biosim.island import Island
from biosim.landscape import Ocean, Savannah, Desert, Jungle, Mountain
from biosim.fauna import Herbivore, Carnivore
from biosim.graphics import Graphics


class BioSim:
    def __init__(
        self,
        island_map,
        ini_pop,
        seed,
        ymax_animals=None,
        cmax_animals=None,
        img_base=None,
        img_fmt="png",
    ):
        """
        :param island_map: Multi-line string specifying island geography
        :param ini_pop: List of dictionaries specifying initial population
        :param seed: Integer used as random number seed
        :param ymax_animals: Number specifying y-axis limit for graph showing
        animal numbers
        :param cmax_animals: Dict specifying color-code limits for animal
        densities
        :param img_base: String with beginning of file name for figures,
        including path
        :param img_fmt: String with file type for figures, e.g. 'png'

        If ymax_animals is None, the y-axis limit should be adjusted
        automatically.

        If cmax_animals is None, sensible, fixed default values should be used.
        cmax_animals is a dict mapping species names to numbers, e.g.,
           {'Herbivore': 50, 'Carnivore': 20}

        If img_base is None, no figures are written to file.
        Filenames are formed as

            '{}_{:05d}.{}'.format(img_base, img_no, img_fmt)

        where img_no are consecutive image numbers starting from 0.
        img_base should contain a path and beginning of a file name.
        """
        self.island_map = island_map
        self.map = Island(island_map)
        np.random.seed(seed)
        self.add_population(ini_pop)

        if ymax_animals is None:
            self.ymax_animals = None
        else:
            self.ymax_animals = ymax_animals

        self.animal_species = ['Carnivore', 'Herbivore']
        self.landscapes = {'O': Ocean,
                           'S': Savannah,
                           'M': Mountain,
                           'J': Jungle,
                           'D': Desert}
        self.landscape_with_parameters = [Savannah, Jungle]
        self.vis = None
        self.current_year = 0
        self.final_year = None

        self.fig = None
        self.img_axis = None

    def set_animal_parameters(self, species, params):
        """
        Set parameters for animal species.

        :param species: String, name of animal species
        :param params: Dict with valid parameter specification for species
        """
        if species in self.animal_species:
            species_type = eval(species)
            species_type.set_parameters(params)
        else:
            raise TypeError(species + ' parameters can\'t be assigned, '
                                      'there is no such data type')

    def set_landscape_parameters(self, landscape, params):
        """
        Set parameters for landscape type.

        :param landscape: String, code letter for landscape
        :param params: Dict with valid parameter specification for landscape
        """
        if landscape in self.landscapes:
            landscape_type = self.landscapes[landscape]
            if landscape_type in \
                    self.landscape_with_parameters:
                landscape_type.set_parameters(params)
            else:
                raise ValueError(landscape + ' parameter is not valid')

        else:
            raise TypeError(landscape + ' parameters can\'t be assigned, '
                                        'there is no such data type')

    def simulate(self, num_years, vis_years=1, img_years=None):
        """
        Run simulation while visualizing the result.

        :param num_years: number of years to simulate
        :param vis_years: years between visualization updates
        :param img_years: years between visualizations saved to files
        (default: vis_years)

        Image files will be numbered consecutively.
        """
        if img_years is None:
            img_years = vis_years

        self.final_year = self.current_year + num_years
        self.setup_graphics()

        while self.current_year < self.final_year:
            if self.current_year % vis_years == 0:
                self.update_graphics()

            if self.current_year % img_years == 0:
                self.save_graphics()

            self.map.update()
            self.current_year += 1

    def setup_graphics(self):
        map_dims = self.map.map_dimensions

        if self.fig is None:
            self.fig = plt.figure()
            self.vis = Graphics(self, self.island_map,
                                self.fig, map_dims)

            self.vis.generate_island_graph()
            self.vis.generate_animal_graphs(self.final_year)

            self.vis.animal_dist_graphs()

    def update_graphics(self):
        pass

    def save_graphics(self):
        pass

    def add_population(self, population):
        """
        Add a population to the island

        :param population: List of dictionaries specifying population
        """
        self.map.add_animals(population)

    @property
    def year(self):
        """Last year simulated."""
        return self.current_year

    @property
    def num_animals(self):
        """Total number of animals on island."""
        animal_count = 0
        for species in self.animal_species:
            animal_count += self.map.total_animals_per_species(species)
            return animal_count

    @property
    def num_animals_per_species(self):
        """Number of animals per species in island, as dictionary."""
        num_fauna_per_species = {}
        for species in self.animal_species:
            num_fauna_per_species[species] = self.map.\
                total_animals_per_species(species)
        return num_fauna_per_species

    @property
    def animal_distribution(self):
        """Pandas DataFrame with animal count per species for each cell
        on island."""
        animal_df = []
        rows, cols = self.map.map_dimensions
        for row in range(rows):
            for col in range(cols):
                cell = self.map.cell_type_map[row, col]
                animal_count = cell.cell_fauna_count
                animal_df.append({'row': row, 'col': col,
                                  'carnivores': animal_count['Carnivore'],
                                  'herbivores': animal_count['Herbivore']})
        return pd.DataFrame(animal_df)

    def make_movie(self):
        """Create MPEG4 movie from visualization images saved."""
