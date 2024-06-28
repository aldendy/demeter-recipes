# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 21:35:30 2024

@author: AldenYellowhorse

This file implements various classes and datastructures used by the recipe code
"""

from conversions import unit_to_base
from fractions import Fraction


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
        for v in values:
            self.value += Fraction(v)

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

    def __init__(self, amount, unit, item):
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

    def __mul__(self, scalar):
        """Get a multiple of 'Ingredient' based on a scalar (float)."""
        return Ingredient(self.amount * scalar, self.unit, self.item)

    def __rmul__(self, scalar):
        """Implement right multiplication with a scalar (float)."""
        return Ingredient(self.amount * scalar, self.unit, self.item)

    def __truediv__(self, divisor):
        """Get the ingredient divided by a divisor (float)."""
        return Ingredient(self.amount / divisor, self.unit, self.item)

    def __repr__(self):
        """Define how to represent this class."""
        measure = self.unit if self.amount != 1 else self.unit + 's'
        return f'Ingredient({self.amount} {measure} {self.item})'

    def to(self, unit, system='us'):
        """Given a unit (str) and the unit 'system' (metric, imperial, etc.)
        convert the class to the new unit."""
        ratio = unit_to_base[system][self.unit] / unit_to_base[system][unit]
        return Ingredient(self.amount * ratio, unit, self.item)
