# -*- coding: utf-8 -*-

"""
Simulates the whole project
"""

__author__ = "Hemanth Sana & Mithunan Sivagnanam"
__email__ = "hesa@nmbu.no & misi@nmbu.no"

import matplotlib.pyplot as plt
import numpy as np

from biosim.island import Island
from biosim.landscape import Ocean, Savannah, Desert, Jungle, Mountain


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
        self.animal_species = ['Carnivore', 'Herbivore']
        self.landscapes = {'O': Ocean,
                           'S': Savannah,
                           'M': Mountain,
                           'J': Jungle,
                           'D': Desert}
        self.landscape_with_parameters = [Savannah, Jungle]
        self.step = 0
        self.final_step = None

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

        self.final_step = self.step + num_years
        self.setup_graphics()

        while self.step < self.final_step:
            if self.step % vis_years == 0:
                self.update_graphics()

            if self.step % img_years == 0:
                self.save_graphics()

            self.map.update()
            self.step += 1

    def setup_graphics(self):
        map_dimensions = self.map.map_dimensions

        if self.fig is None:
            self.fig = plt.figure()
            self.vis = Graphics

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
        return self.step

    @property
    def num_animals(self):
        """Total number of animals on island."""
        animal_count = 0
        for animal in self.animal_species:
            animal_count += len(animal['pop'])
            return animal_count

    @property
    def num_animals_per_species(self):
        """Number of animals per species in island, as dictionary."""
        animal_count_dict = {'Herbivore': 0, 'Carnivore': 0}
        for animal in self.ini_pop:
            if animal['pop'][0]['species'] == 'Herbivore':
                animal_count_dict['Herbivore'] += len(animal['pop'])
            elif animal['pop'][0]['species'] == 'Carnivore':
                animal_count_dict['Carnivore'] += len(animal['pop'])
        return animal_count_dict

    @property
    def animal_distribution(self):
        """Pandas DataFrame with animal count per species for each cell
        on island."""
        pass

    def make_movie(self):
        """Create MPEG4 movie from visualization images saved."""
