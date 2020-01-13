# -*- coding: utf-8 -*-

"""
Tests for landscape.py
"""

__author__ = "Hemanth Sana & Mithunan Sivagnanam"
__email__ = "hesa@nmbu.no & misi@nmbu.no"

import pytest

from biosim.landscape import Landscape
from biosim.landscape import Desert
from biosim.landscape import Ocean
from biosim.landscape import Mountain
from biosim.landscape import Savannah
from biosim.landscape import Jungle


class TestLandscape:
    pass


class TestJungle:
    pass


class TestSavannah:
    pass


class TestDesert:
    def test_fodder_unavailable(self):
        """No fodder available in the desert"""
        pass


class TestMountain:
    def test_fodder_unavailable(self):
        """No fodder available in the desert"""
        pass


class TestOcean:
    def test_fodder_unavailable(self):
        """No fodder available in the desert"""
        pass
