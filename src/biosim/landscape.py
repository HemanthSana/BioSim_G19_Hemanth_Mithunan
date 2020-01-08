# -*- coding: utf-8 -*-

"""
"""

__author__ = "Hemanth Sana & Mithunan Sivagnanam"
__email__ = "hesa@nmbu.no & misi@nmbu.no"


class Landscape:
    """
    Contains common attributes for other classes
    """
    def __init__(
            self,
            is_grazable,
            is_migratable
    ):
        self.is_grazable = is_grazable
        self.is_migratable = is_migratable


class Ocean(Landscape):
    """
        This represents the cells covered by ocean
    """
    def __init__(
            self,
            is_grazable,
            is_migratable
    ):
        super().__init__(is_grazable=False, is_migratable=False)


class Jungle:
    """
        This represents the cells covered by jungle
    """
    fodder_max = 800

    def __init__(
            self,
            is_grazable,
            is_migratable
    ):
        super().__init__(is_grazable=True, is_migratable=True)


class Savannah:
    """
    This represents the cells covered by savannah
    """
    fodder_max = 300

    def __init__(
            self,
            is_grazable,
            is_migratable
    ):
        super().__init__(is_grazable=True, is_migratable=True)


class Desert:
    """
        This represents the cells covered by desert
    """
    def __init__(
            self,
            is_grazable,
            is_migratable
    ):
        super().__init__(is_grazable=False, is_migratable=True)


class Mountain:
    """
        This represents the cells covered by mountain
    """
    def __init__(
            self,
            is_grazable,
            is_migratable
    ):
        super().__init__(is_grazable=False, is_migratable=False)
