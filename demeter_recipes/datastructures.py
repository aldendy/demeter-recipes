# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 21:35:30 2024

@author: AldenYellowhorse

This file implements various classes and datastructures used by the recipe code
"""

from fractions import Fraction
from datetime import date
from conversions import unit_to_base


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


class Ingredient:
    """This class inherits from 'Conversion' to access methods for converting
    easily to other units."""

    def __init__(self, amount: Number, unit: str, item: str):
        """Initialize the object based on an amount (float), unit (str) and
        item (str) which holds the actual ingredient name."""
        self.amount = Number(amount)
        self.unit = unit
        self.item = item

    def __add__(self, other):
        """Define the result when ingredients are added. The result takes the
        unit of this object (not other)."""
        if self.item == other.item:
            item_name = self.item
        else:
            item_name = self.item + '+' + other.item
        return Ingredient(self.amount + other.to(self.unit).amount, self.unit,
                          item_name)

    def __sub__(self, other):
        """Define subtraction between two ingredients. The item name is assumed
        to be the same as this object since it does not make sense to subtract
        different foods."""
        return Ingredient(self.amount - other.to(self.unit).amount, self.unit,
                          self.item)

    def __mul__(self, scalar: float):
        """Get a multiple of 'Ingredient' based on a scalar (float)."""
        return Ingredient(self.amount * scalar, self.unit, self.item)

    def __rmul__(self, scalar: float):
        """Implement right multiplication with a scalar (float)."""
        return Ingredient(self.amount * scalar, self.unit, self.item)

    def __truediv__(self, divisor: float):
        """Get the ingredient divided by a divisor (float)."""
        return Ingredient(self.amount / divisor, self.unit, self.item)

    def __repr__(self):
        """Define how to represent this class."""
        measure = self.unit if self.amount != 1 else self.unit + 's'
        return f'Ingredient({self.amount} {measure} {self.item})'

    def to_unit(self, unit: str, system: str = 'us'):
        """Given a unit (str) and the unit 'system' (metric, imperial, etc.)
        convert the class to the new unit."""
        ratio = unit_to_base[system][self.unit] / unit_to_base[system][unit]
        return Ingredient(self.amount * ratio, unit, self.item)


class Recipe:
    """This class stores an ordered list of ingredients and instructions that
    must be followed to execute the meal."""

    def __init__(self, name: str, array: list, instructions: str = None):
        """The array is assumed to be 1D and filled with objects of type str
        and Ingredient. 'instructions' is a string of overall info. 'name'
        stores the name of the recipe (str)."""
        self.name = name
        self.steps = array
        self.instructions = instructions

    def __repr__(self):
        """Display the steps of the recipe."""
        output = "" if self.instructions is None else self.instructions + '\n'
        for i, step in enumerate(self.steps):
            output += str(i+1) + ') ' + str(step) + '\n'
        return output

    def insert_after(self, step_num: int, step):
        """Insert step into the recipe where step is either a string or an
        Ingredient object."""
        self.steps.insert(step_num, step)
        return True

    def insert_before(self, step_num: int, step):
        """Insert a step before the given step number (starting at 1). The step
        is either a string or an Ingredient object."""
        self.steps.insert(step_num-1, step)
        return True

    def remove_step(self, step_num: int):
        """Delete a step."""
        del self.steps[step_num - 1]


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

    def populate_meal(self, meal_name: str, recipes):
        """For a single recipe or list of recipes, add them to the list stored
        in the meals dictionary. This assumes that the meal exists."""
        if isinstance(recipes, list):
            self.meals[meal_name] += recipes
        else:
            self.meals[meal_name].append(recipes)

    def add_meal(self, meal_name: str, recipes=[]):
        """Add a meal name (str). Optionally, add a single recipe or list of
        recipes."""
        self.meals[meal_name] = []
        self.populate_meal(recipes)

    def delete_meal(self, meal_name: str):
        """Remove a meal identified by name (str)."""
        if meal_name in self.meals:
            self.meals.pop[meal_name]

    def add_recipes(self, meal_name: str, recipes):
        """Add a recipe or receipes to the meal."""
        if meal_name in self.meals:
            self.populate_meal(meal_name, recipes)
        else:
            self.add_meal(meal_name, recipes)
