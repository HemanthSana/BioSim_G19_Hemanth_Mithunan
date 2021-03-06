# -*- coding: utf-8 -*-

"""
Simulates the whole project
"""

__author__ = "Hemanth Sana & Mithunan Sivagnanam"
__email__ = "hesa@nmbu.no & misi@nmbu.no"

import os
import random

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import subprocess

from biosim.island import Island
from biosim.landscape import Ocean, Savannah, Desert, Jungle, Mountain
from biosim.fauna import Carnivore, Herbivore
from biosim.graphics import Graphics

DEFAULT_GRAPHICS_DIR = os.path.join('results/')
DEFAULT_GRAPHICS_NAME = 'biosim'
DEFAULT_MOVIE_FORMAT = 'mp4'

FFMPEG_BINARY = 'ffmpeg'
CONVERT_BINARY = 'magick'


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
        self.landscapes = {'O': Ocean,
                           'S': Savannah,
                           'M': Mountain,
                           'J': Jungle,
                           'D': Desert}
        self.landscapes_with_parameters = [Savannah, Jungle]

        self.animal_species = {'Carnivore': Carnivore, 'Herbivore': Herbivore}

        for char in island_map.replace('\n', ''):
            if char not in self.landscapes:
                raise ValueError('This given string contains unknown '
                                 'geographies')

        lengths = [len(line) for line in island_map.splitlines()]
        if len(set(lengths)) > 1:
            raise ValueError('This given string is not uniform')
        self.island_map = island_map
        self._map = Island(island_map)
        random.seed(seed)
        self.add_population(ini_pop)

        if ymax_animals is None:
            self.ymax_animals = 20000
        else:
            self.ymax_animals = ymax_animals

        if cmax_animals is None:
            self.cmax_animals = {'Herbivore': 5, 'Carnivore': 5}
        else:
            self.cmax_animals = cmax_animals

        if img_base is None:
            self.img_base = DEFAULT_GRAPHICS_DIR + DEFAULT_GRAPHICS_NAME
        else:
            self.img_base = img_base

        self.img_fmt = img_fmt
        self.img_counter = 0

        self.vis = None
        self._year = 0
        self.final_year = None

    def set_animal_parameters(self, species, params):
        """
        Set parameters for animal species.

        :param species: String, name of animal species
        :param params: Dict with valid parameter specification for species
        """
        if species in self.animal_species:
            species_type = self.animal_species[species]
            animal = species_type()
            animal.set_parameters(params)
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
                    self.landscapes_with_parameters:
                landscape_type.set_parameters(params)
            else:
                raise ValueError(landscape + ' parameter is not valid')

        else:
            raise TypeError(landscape + ' parameters can\'t be assigned, '
                                        'there is no such data type')

    def simulate(self, num_years, vis_years=200, img_years=None):
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

        self.final_year = self._year + num_years
        self.setup_graphics()
        if self._year > 1:
            self.vis.generate_animal_graphs(self.final_year,
                                            self.ymax_animals,
                                            recreate=True)

        while self._year < self.final_year:
            if self._year % vis_years == 0:
                self.update_graphics()

            if (self._year + 1) % img_years == 0:
                self.save_graphics()

            self._map.life_cycle()
            self._year += 1

            df = self.animal_distribution
            df.to_csv('results/data.csv', sep='\t', encoding='utf-8')

    def setup_graphics(self):
        """
        Setup the graphics
        """
        map_dims = self._map.map_dims

        if self.vis is None:
            fig = plt.figure()
            self.vis = Graphics(self.island_map,
                                fig, map_dims)

            self.vis.generate_island_graph()
            self.vis.generate_animal_graphs(self.final_year, self.ymax_animals)

            self.vis.animal_dist_graphs()

    def update_graphics(self):
        """
        Updates graphics with current data.
        """
        df = self.animal_distribution
        rows, cols = self._map.map_dims
        dist_matrix_carnivore = np.array(df[['Carnivore']]).reshape(rows, cols)
        dist_matrix_herbivore = np.array(df[['Herbivore']]).reshape(rows, cols)

        # updates the line graphs
        herb_count, carn_count = list(self.num_animals_per_species.values())
        self.vis.update_graphs(self._year, herb_count, carn_count)

        self.vis.update_herbivore_dist(dist_matrix_herbivore)
        self.vis.update_carnivore_dist(dist_matrix_carnivore)
        plt.pause(1e-6)
        self.vis.set_year(self._year)

    def save_graphics(self):
        """
        Save the graphics
        """
        if self.img_base is None:
            return

        plt.savefig('{base}_{num:05d}.{type}'.format(base=self.img_base,
                                                     num=self.img_counter,
                                                     type=self.img_fmt))
        self.img_counter += 1

    def add_population(self, population):
        """
        Add a population to the island

        :param population: List of dictionaries specifying population
        """
        self._map.add_animals(population)

    def make_movie(self, movie_fmt=DEFAULT_MOVIE_FORMAT):
        """Create MPEG4 movie from visualization images saved."""
        if self.img_base is None:
            raise RuntimeError('No filename defines')

        if movie_fmt == 'mp4':
            try:
                subprocess.check_call([FFMPEG_BINARY,
                                       '-i',
                                       '{}_%05d.png'.format(self.img_base),
                                       '-y',
                                       '-profile:v', 'baseline',
                                       '-level', '3.0',
                                       '-pix_fmt', 'yuv420p',
                                       '{}.{}'.format(self.img_base,
                                                      movie_fmt)])
            except subprocess.CalledProcessError as err:
                raise RuntimeError('Error: ffmpeg failed with: {}'.format(err))
        elif movie_fmt == 'gif':
            try:
                subprocess.check_call([CONVERT_BINARY,
                                       '-delay', '1',
                                       '-loop', '0',
                                       '{}_*.png'.format(self.img_base),
                                       '{}.{}'.format(self.img_base,
                                                      movie_fmt)])
            except subprocess.CalledProcessError as err:
                raise RuntimeError(
                    'Error: convert failed with: {}'.format(err))
        else:
            raise ValueError('Unknown movie format')

    @property
    def year(self):
        """Last year simulated."""
        return self._year

    @property
    def num_animals(self):
        """Total number of animals on island."""
        animal_count = 0
        for species in self.animal_species:
            animal_count += self._map.total_animals_per_species(species)
            return animal_count

    @property
    def num_animals_per_species(self):
        """Number of animals per species in island, as dictionary."""
        num_fauna_per_species = {}
        for species in self.animal_species:
            num_fauna_per_species[species] = self._map.\
                total_animals_per_species(species)
        return num_fauna_per_species

    @property
    def animal_distribution(self):
        """Pandas DataFrame with animal count per species for each cell
        on island."""
        animal_df = []
        rows, cols = self._map.map_dims
        for row in range(rows):
            for col in range(cols):
                cell = self._map.cells[row, col]
                animal_count = cell.cell_fauna_count
                animal_df.append({'Row': row, 'Col': col,
                                  'Herbivore': animal_count['Herbivore'],
                                  'Carnivore': animal_count['Carnivore']})
        return pd.DataFrame(animal_df)
