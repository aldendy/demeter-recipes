# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 21:35:30 2024

@author: AldenYellowhorse

This file implements various classes and datastructures used by the recipe code
"""

import re
import unicodedata
from fractions import Fraction
from datetime import date
from recipe_scrapers import scrape_html
from pint import UnitRegistry, Quantity, Unit


ureg = UnitRegistry()
ureg.load_definitions('src\\cooking_units.txt')
units = dir(ureg)


class Unitless:
    def __init__(self, mass: Unit, volume: Unit):
        """Initialize the properties of unitless objects such as eggs. The
        inputs are
        mass (g)
        volume (mL)
        """
        self._mass = mass
        self._volume = volume

    def mass(self, _=None):
        """Getter for the mass."""
        return self._mass

    def volume(self, _=None):
        """Getter for the volume."""
        return self._volume


unitless = {'egg': Unitless(48, 44.3604),
            'garlic clove - chopped': Unitless(5.1 * ureg.g, 5 * ureg.mL),
            'garlic clove - minced': Unitless(5.1 * ureg.g, 2.5 * ureg.mL)
            }


class Number:
    """This class handles measurement numbers and their conversions between
    float values and fractions, mixed fractions, etc. It stores the exact
    number as a float and can portray various representations."""

    def __init__(self, value):
        """The assumption is that a int, float or string is supplied to
        initialize. The text is either a float or a fraction that is irrational
        or mixed."""
        values = str(value).strip().split()
        self.value = 0
        for number in values:
            self.value += Fraction(number)

    def __add__(self, other):
        """Implement addition."""
        return Number(self.value + float(other))

    def __sub__(self, other):
        """Implement subtraction."""
        return Number(self.value - float(other))

    def __mul__(self, other):
        """Implement multiplication."""
        return Number(self.value * float(other))

    def __rmul__(self, other):
        """Implement right multiplication."""
        return Number(self.value * float(other))

    def __truediv__(self, divisor):
        """Implements division with an integer."""
        return Number(str(self.value / divisor))

    def __repr__(self):
        """Show the data as a mixed fraction."""
        whole_number = str(self.value.numerator // self.value.denominator)
        fraction = self.value - Fraction(whole_number)
        text = f'{whole_number} {fraction.limit_denominator(8)}'
        return text.lstrip('0 ').rstrip(' 0')

    def __float__(self):
        """Get a float representation of the object."""
        return float(self.value)


def to_float(value: str) -> float:
    """Take string numbers and convert them to floats."""
    value = value.rstrip()
    nv = unicodedata.normalize('NFKC', value)

    whole_num = re.search('^[0-9]*', nv)
    if whole_num is None:
        whole_num = 0
    else:
        whole_num = float(whole_num.group())

    fraction = re.search('[0-9]+/[0-9]+$', nv).group()
    if fraction is None:
        fraction = 0
    else:
        pass
        
    swap_table = {'1/2': 0.5}


class Ingredient:
    """This class inherits from 'Conversion' to access methods for converting
    easily to other units."""

    def __init__(self, amount: Quantity = None, item: str = None,
                 text: str = None):
        """Initialize the object based on an amount (float), unit (str) and
        item (str) which holds the actual ingredient name."""
        if text is None:
            self.amount = Number(amount)
            self.item = item
        else:
            num_txt = re.search('^[^a-z]+', text)
            description = re.search('[ ,a-zA-Z]+$', text).group()
            measures = [word for word in description if word in units]
            if len(measures) > 0:
                self.amount = 'crazy'
            self.item = 'also crazy'

    def __add__(self, other):
        """Define the result when ingredients are added. The result takes the
        unit of this object (not other)."""
        if self.item == other.item:
            item_name = self.item
        else:
            item_name = self.item + ' + ' + other.item
        combined = self.amount + other.amount.to(self.amount.units)
        return Ingredient(combined, item_name)

    def __sub__(self, other):
        """Define subtraction between two ingredients. The item name is assumed
        to be the same as this object since it does not make sense to subtract
        different foods."""
        if self.item == other.item:
            item_name = self.item
        else:
            item_name = self.item + ' - ' + other.item
        difference = self.amount - other.amount.to(self.amounts.units)
        return Ingredient(difference, item_name)

    def __mul__(self, scalar: float):
        """Get a multiple of 'Ingredient' based on a scalar (float)."""
        return Ingredient(self.amount * scalar, self.item)

    def __rmul__(self, scalar: float):
        """Implement right multiplication with a scalar (float)."""
        return Ingredient(self.amount * scalar, self.item)

    def __truediv__(self, divisor: float):
        """Get the ingredient divided by a divisor (float)."""
        return Ingredient(self.amount / divisor, self.item)

    def __repr__(self):
        """Define how to represent this class."""
        if self.amount.magnitude != 1:
            return f'Ingredient({self.amount}s {self.item})'
        else:
            return f'Ingredient({self.amount} {self.item}'

    def to_unit(self, unit: Unit):
        """Given a unit (str) and the unit 'system' (metric, imperial, etc.)
        convert the class to the new unit."""
        return Ingredient(self.amount.to(unit), self.item)


class Recipe:
    """This class is an interface to the recipe scraper object that extends its
    capabilities to match the needs of this program."""

    def __init__(self, name: str, array: list, instructions: str = None):
        """The array is assumed to be 1D and filled with objects of type str
        and Ingredient. 'instructions' is a string of overall info. 'name'
        stores the name of the recipe (str)."""
        self.scraper = scrape_html

    @property
    def title(self) -> str:
        """Get the recipe title."""
        return self.scraper.title


class Library:
    """Organizes a collection of recipes into a names library where each recipe
    is associated with a name key in a dictionary. Multiple libraries are
    allowed."""

    def __init__(self, name: str):
        """Initialize the library with a name (str)."""
        self.name = name
        self.recipes = {}  # store key: recipe name, value: recipe object

    def add_recipe(self, recipe: Recipe):
        """Insert a recipe into the library."""
        self.recipes[recipe.name] = recipe

    def remove_recipe(self, name: str):
        if name in self.recipes:
            _ = self.recipes.pop(name)


class Day:
    """This class makes it possible to take multiple recipes and group them
    into meals as lists. Each meal is a key in a dictionary."""

    def __ini__(self, calendar_date: date):
        """Initialize the day with a date object."""
        self.date = date
        self.meals = {}  # stores keys: meal names and values: list of recipes

    def add_food(self, meal_name: str, recipes=[]):
        """For a list of recipes, add it(them) to the list in the meals
        dictionary. If the meal exists, add the recipe to the
        meal. Otherwise, create a new meal name."""
        if isinstance(recipes, list):
            if meal_name in self.meals:
                self.meals[meal_name] += recipes
            else:
                self.mealse[meal_name] = recipes

    def delete_meal(self, meal_name: str):
        """Remove a meal identified by name (str)."""
        if meal_name in self.meals:
            self.meals.pop[meal_name]
