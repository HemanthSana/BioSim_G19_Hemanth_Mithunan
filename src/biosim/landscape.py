# -*- coding: utf-8 -*-

"""
Contains Data of each cell, fodder functions and
animal list in each cell
"""

__author__ = "Hemanth Sana & Mithunan Sivagnanam"
__email__ = "hesa@nmbu.no & misi@nmbu.no"


import math
import operator
import numpy as np


class Landscape:
    """
    Parent class for type of landscapes Jungle, Savannah,
    Mountain, Desert, Ocean
    """
    parameters = {}

    def __init__(self):
        """
        """
        self.sorted_animal_fitness = {}
        self.fauna_list = {'Herbivore': [], 'Carnivore': []}
        self.new_fauna_list = {'Herbivore': [], 'Carnivore': []}
        self._remaining_food = {'Herbivore': 0, 'Carnivore': 0}

    def save_fitness(self, animals, species):
        """
        Updates fitness value
        """
        animal_fitness = {}
        for animal in animals[species]:
            animal_fitness[animal] = animal.fitness
        self.sorted_animal_fitness[species] = animal_fitness

    def order_by_fitness(self):
        """
        Sorts animal_objects according to the fitness
        """
        self.fauna_list['Herbivore'].sort(key=operator.
                                          attrgetter('animal_fitness'))
        self.fauna_list['Carnivore'].sort(key=operator.
                                          attrgetter('animal_fitness'),
                                          reverse=True)

    def relevant_food(self, animal):
        """
        Returns relevant food remaining in cell (f_k)
        This is different for Carnivores and Herbivores
        """
        species = animal.__class__.__name__
        return self.remaining_food[species]

    def add_animal(self, animal):
        """
        Adds animal(object) to the species list of cell
        """
        species = animal.__class__.__name__
        self.fauna_list[species].append(animal)

    def remove_animal(self, animal):
        """
        Removes animal(object) from list of same species for cell
        """
        species = animal.__class__.__name__
        self.fauna_list[species].remove(animal)

    def relative_abundance_fodder(self, animal):
        """
        Calculates "Relative Abundance of Fodder" (E_k) by relevant fodder,
        number of animals of same species and the F
        """
        species = animal.__class__.__name__
        return self.relevant_food(animal) / (
                (len(self.fauna_list[species]) + 1) * animal.parameters['F'])

    def propensity_to_move(self, animal):
        """
        Returns Propensity to move from a cell to adjacent cell
        If the adjacent cell is Mountain or Landscape it returns 0
        """
        if isinstance(self, Mountain) or isinstance(self, Ocean):
            return 0
        else:
            return math.exp(animal.parameters['lambda'] *
                            self.relative_abundance_fodder(animal))

    def probability_move_to_cell(self, animal, total_propensity):
        """
        Calculates the probability to move from one cell to another
        """
        return self.propensity_to_move(animal) / total_propensity

    def animal_eats(self):
        """
        Feeding the animals in the cell in the order
        Grow the fodder, Herbivore eat fodder, Carnivore eats Herbivore
        """
        self.update_fodder()
        self.herbivore_eats()
        self.carnivore_eats()

    def herbivore_eats(self):
        """
        Herbivores eat according to their fitness. Animal with
        highest fitness eats first
        If there is no fodder available in cell animal doesnt eat
        if the available fodder is greater than the food
        required animal eats the required amount. We calculate the
        remaining fodder in cell
        if fodder available is less than food required animal eates
        available food. And update remaining fodder as 0
        """
        self.order_by_fitness()
        for herb in self.fauna_list['Herbivore']:
            herb_remaining_fodder = self.remaining_food['Herbivore']
            if herb_remaining_fodder == 0:
                break
            elif herb_remaining_fodder >= herb.parameters['F']:
                herb.animal_eats(herb.parameters['F'])
                self.remaining_food['Herbivore'] -= herb.parameters['F']
            elif 0 < herb_remaining_fodder < herb.parameters['F']:
                herb.animal_eats(herb_remaining_fodder)
                self.remaining_food['Herbivore'] = 0

    def carnivore_eats(self):
        """
        Carnivores with highest fitness eat first. Herbivores with least
        fitness will be eaten first.
        if there is enough weight for carnivore to eat it eats the
        required food F, Else it eats food equal to weight of herbivores
        """
        self.order_by_fitness()
        for carn in self.fauna_list['Carnivore']:
            food_required = carn.parameters['F']
            amount_to_eat = 0
            not_eaten_animals = []
            for i, herb in enumerate(self.fauna_list['Herbivore']):
                if food_required <= amount_to_eat:
                    not_eaten_animals.extend(self.fauna_list['Herbivore'][i:])
                    break
                elif np.random.random() < carn.probability_of_kill(herb):
                    if food_required - amount_to_eat < herb.weight:
                        amount_to_eat += herb.weight
                    elif food_required - amount_to_eat > herb.weight:
                        amount_to_eat += food_required - amount_to_eat
                else:
                    not_eaten_animals.append(herb)
            carn.animal_eats(amount_to_eat)
            self.fauna_list['Herbivore'] = not_eaten_animals

    def update_fodder(self):
        """
        Method to update fodder in cells. Overridden in Jungle and Savannah
        """
        pass

    def update_animal_weight_age(self):
        """
        Each year animal increases in age by 1 and loses weight by factor eta
        """
        for species in self.fauna_list:
            for animal in self.fauna_list[species]:
                animal.animal_grows()

    def animals_gives_birth(self):
        """
        Compare the probability_of_birth with random value generated
        If its greater animal gives birth. Create offspring of same species
        and decrease weight of animal
        """
        for species, animals in self.new_fauna_list.items():
            for i in range(math.floor(len(self.new_fauna_list[species])/2)):
                animal = animals[i]
                if animal.probability_of_birth(len(animals)):
                    offspring_species = animal.__class__
                    offspring = offspring_species()
                    animal.update_weight_after_birth(offspring)
                    if animal.gives_birth:
                        self.fauna_list[species].append(offspring)
                        animal.gives_birth = False

    def add_offspring_to_adult_animals(self):
        """
        After the breeding stage, the new babies are added to the cell
        animals dictionary and remove it from the baby fauna dictionary.
        adult_fauna as input to calculate the giving birth probability.
        """

        self.new_fauna_list = self.fauna_list

    def animal_dies(self):
        """
        If generated random number is greater than probability_of_death
        We remove the animal from dictionary
        """
        for species, animals in self.fauna_list.items():
            for animal in animals:
                if animal.probability_of_death:
                    self.remove_animal(animal)

    def animal_migrates(self, adj_cells):
        """
        We calculate the probability as propensity/sum of propensity
        for each adj cells. Animal migrates to the cell with highest
        probability to move. We add the animal to the newly moved cell and
        remove it from old cell.
        """
        for species, animals in self.fauna_list.items():
            for animal in animals:
                if animal.probability_of_move:
                    propensity = [cell.propensity_to_move(animal)
                                  for cell in adj_cells]
                    total_propensity = sum(propensity)
                    if total_propensity != 0:
                        probability = [cell.probability_move_to_cell(
                            animal, total_propensity)
                            for cell in adj_cells]
                        cum_probability = np.cumsum(probability)
                        i = 0
                        while np.random.random() > cum_probability[i]:
                            i += 1
                        cell_to_migrate = adj_cells[i]
                        if cell_to_migrate.is_migratable:
                            if animal.is_animal_moved_already is False:
                                cell_to_migrate.add_animal(animal)
                                self.remove_animal(animal)
                                animal.is_animal_moved_already = True

    def grow_all_animals(self):
        """
        Growing all animals
        """
        for species in self.fauna_list:
            for animal in self.fauna_list[species]:
                animal.animal_grows()

    @property
    def cell_fauna_count(self):
        """
        Returns count of fauna type as dictionary
        """
        herb_count = len(self.fauna_list['Herbivore'])
        carn_count = len(self.fauna_list['Carnivore'])
        return {'Herbivore': herb_count, 'Carnivore': carn_count}

    @property
    def total_herb_weight(self):
        """
        Returns the total herbivore weight
        """
        return sum(herb.weight for herb in self.fauna_list['Herbivore'])

    @property
    def remaining_food(self):
        """
        Gives remaining food for animals according to cells
        """
        if isinstance(self, (Ocean, Mountain)):
            raise ValueError('There are no fodder available in this cell')
        elif isinstance(self, Desert):
            self._remaining_food = {'Herbivore': 0,
                                    'Carnivore': self.total_herb_weight}
        else:
            self._remaining_food = {'Herbivore': self.parameters['f_max'],
                                    'Carnivore': self.total_herb_weight}
        return self._remaining_food

    def reset_migration_flag(self):
        for species, animals in self.fauna_list.items():
            for animal in animals:
                animal.is_animal_moved_already = False


class Jungle(Landscape):
    """
        Represents landscape covered by jungle cells
        There is no risk of over grazing
        Every year available fodder is maximum fodder(f_max)
    """
    is_migratable = True
    parameters = {'f_max': 800.0}

    def __init__(self, given_params=None):
        # child class of Landscape
        super().__init__()
        if given_params is not None:
            self.set_parameters(given_params)
        self.parameters = Jungle.parameters
        self.remaining_food['Herbivore'] = self.parameters['f_max']
        self.remaining_food['Carnivore'] = sum(herb.weight for herb in
                                               self.fauna_list['Herbivore'])

    @staticmethod
    def set_parameters(given_params):
        for param in given_params:
            if param in Jungle.parameters:
                Jungle.parameters[param] = \
                    given_params[param]
            else:
                raise ValueError('Parameter not in list' + str(param))

    def update_fodder(self):
        """
        Updates the annual fodder. There is no overgrazing in Jungle so amount
        of available fodder will be equal to f_max
        """
        self.remaining_food['Herbivore'] = self.parameters['f_max']


class Savannah(Landscape):
    """
    Represents the landscape  covered by savannah cells
    Here there is risk of over grazing
    Every year available folder in each cell is calculated manually
    """
    is_migratable = True
    parameters = {'f_max': 300.0, 'alpha': 0.3}

    def __init__(self, given_params=None):
        super().__init__()
        if given_params is not None:
            self.set_parameters(given_params)
        self.parameters = Savannah.parameters
        self.remaining_food['Herbivore'] = self.parameters['f_max']
        self.remaining_food['Carnivore'] = sum(herb.weight for herb in
                                               self.fauna_list['Herbivore'])

    @staticmethod
    def set_parameters(given_params):
        for param in given_params:
            if param in Savannah.parameters:
                Savannah.parameters[param] = \
                    given_params[param]
            else:
                raise ValueError('Parameter not in list' + str(param))

    def update_fodder(self):
        """
        Updates the fodder available in Savannah cells. Available fodder is
        calculated by formula  available fodder = available fodder +
        alpha(f_max - available fodder)
        """
        self.remaining_food['Herbivore'] += self.parameters['alpha'] * (
                self.parameters['f_max'] - self.remaining_food['Herbivore'])


class Desert(Landscape):
    """
        Represents the landscape covered by desert cells
        In these cells animals can migrate but there is no fodder available
    """
    is_migratable = True
    remaining_food = {'Herbivore': 0}

    def __init__(self):
        # child class of Landscape
        super().__init__()
        self.f_max = 0
        self.remaining_food['Herbivore'] = Desert.remaining_food['Herbivore']
        self.remaining_food['Carnivore'] = sum(herb.weight for herb in
                                               self.fauna_list['Herbivore'])


class Mountain(Landscape):
    """
        Represents the landscape covered by mountain cells
        In these cells animals cannot migrate and there is no fodder
    """
    is_migratable = False
    remaining_food = {'Herbivore': 0, 'Carnivore': 0}
    animals_list = {'Herbivore': [], 'Carnivore': []}

    def __init__(self):
        # child class of Landscape
        super().__init__()
        self.remaining_food['Herbivore'] = Mountain.remaining_food['Herbivore']
        self.remaining_food['Carnivore'] = Mountain.remaining_food['Carnivore']
        self.animals_list['Herbivore'] = Mountain.animals_list['Herbivore']
        self.animals_list['Carnivore'] = Mountain.animals_list['Carnivore']


class Ocean(Landscape):
    """
    Represents landscape covered by ocean cells
    In these cells animals cannot migrate and there is no fodder
    """
    is_migratable = False
    remaining_food = {'Herbivore': 0, 'Carnivore': 0}
    animals_list = {'Herbivore': [], 'Carnivore': []}

    def __init__(self):
        # child class of Landscape
        super().__init__()
        self.remaining_food['Herbivore'] = Ocean.remaining_food['Herbivore']
        self.remaining_food['Carnivore'] = Ocean.remaining_food['Carnivore']
        self.animals_list['Herbivore'] = Ocean.animals_list['Herbivore']
        self.animals_list['Carnivore'] = Ocean.animals_list['Carnivore']
