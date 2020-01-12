# -*- coding: utf-8 -*-

"""
Contains Data of each cell, fodder functions and
animal list in each cell
"""

__author__ = "Hemanth Sana & Mithunan Sivagnanam"
__email__ = "hesa@nmbu.no & misi@nmbu.no"

from biosim.fauna import Fauna


class Landscape:
    """
    Parent class for type of landscape
    """
    def __init__(self, rows, columns):
        """

        :param rows: row value of landscape
        :param columns: column value of landscape
        """
        self.rows = rows
        self.columns = columns


class Jungle(Landscape):
    """
        Represents landscape covered by jungle
    """
    migratable = True
    fodder_max = 800

    def __init__(
            self,
            rows,
            columns,
            no_of_carn,
            no_of_herb,
            f_ij=fodder_max
    ):
        """

        :param rows: Row value for Jungle cell
        :param columns: Column value for jungle cell
        :param no_of_carn: Number of carnivores in jungle cell
        :param no_of_herb: Number of herbivores in jungle cell
        :param f_ij: food in jungle cell
        """
        super().__init__(rows, columns)
        self.no_of_carn = no_of_carn
        self.no_of_herb = no_of_herb
        self.f_ij = f_ij


class Savannah(Landscape):
    """
    Represents the landscape  covered by savannah
    """
    migratable = True
    fodder_max = 300

    def __init__(
            self,
            rows,
            columns,
            no_of_carn,
            no_of_herb,
            f_ij=fodder_max,
            alpha=0.3
    ):
        """

        :param rows: Row value for Savannah Cell
        :param columns: Column value for Savannah Cell
        :param no_of_carn: No of Carnivores in Savannah cell
        :param no_of_herb: No of Herbivores in Savannah cell
        :param f_ij: Food in Savannah cell
        :param alpha: constant for calculation
        """
        super().__init__(rows, columns)
        self.no_of_carn = no_of_carn
        self.no_of_herb = no_of_herb
        self.f_ij = f_ij
        self.alpha = alpha


class Desert(Landscape):
    """
        Represents the landscape covered by desert
    """
    migratable = False
    fodder_max = 0

    def __init__(
            self,
            rows,
            columns,
            no_of_carn,
            no_of_herb,
            f_ij=fodder_max
    ):
        """

        :param rows: Row value for Desert cell
        :param columns: Column value for Desert cell
        :param no_of_carn: Number of carnivores in Desert cell
        :param no_of_herb: Number of Herbivores in Desert cell
        :param f_ij: Fodder in Desert cell
        """
        super().__init__(rows, columns)
        self.no_of_carn = no_of_carn
        self.no_of_herb = no_of_herb
        self.f_ij = f_ij


class Mountain(Landscape):
    """
        Represents the landscape covered by mountain
    """
    migratable = False

    def __init__(self, rows, columns):
        """

        :param rows: Row index for Mountain cell
        :param columns: Column index for Mountain cell
        """
        super().__init__(rows, columns)


class Ocean(Landscape):
    """
    Represents landscape covered by ocean
    """
    migratable = False

    def __init__(self, rows, columns):
        """

        :param rows: Row index for Ocean cell
        :param columns: Column index for Ocean cell
        """
        super().__init__(rows, columns)



