# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 15:08:35 2024

@author: AldenYellowhorse

This script provides conversions between important cooking units and base
units. This information comes from the article
https://en.wikipedia.org/wiki/Cooking_weights_and_measures
"""


class Unitless:
    def __init__(self, mass, volume):
        """Initialize the properties of unitless objects such as eggs. The
        inputs are
        mass (g)
        volume (mL)
        """
        self._mass = mass
        self._volume = volume

    def mass(self, _=None):
        """Getter for the mass (g)."""
        return self._mass

    def volume(self, _=None):
        """Getter for the volume (mL)."""
        return self._volume


class Garlic(Unitless):
    """Modifies a 'unitless' to adjust for different volume types."""

    def volume(self, style='chopped'):
        """Can switch between 'chopped' or 'minced' where style (str) is one
        or the other."""
        if style == 'chopped':
            return self._volume
        elif style == 'minced':
            # it becomes smaller when minced
            return self._volume / 2


unitless_mL = {'egg': Unitless(48, 44.3604),
               'garlic clove': Garlic(5.101, 5)
               }


# These dictionaries maps measures of volume to their equivalent in mL.
us_volumes = {'drop': 0.0513429,
              'pinch': 0.115522,
              'dash': 0.46208,
              'dram': 3.69669,
              'teaspoon': 4.92892,
              'tablespoon': 14.7868,
              'fluid ounce': 29.5735,
              'cup': 236.588,
              'pint': 473.176,
              'quart': 946.353,
              'gallon': 3785.41,
              }

imperial_volumes = {'fluid ounce': 28.4130625,
                    'gallon': 4546.09,
                    'gill': 142.0653125,
                    'pint': 568.26125,
                    'quart': 1136.5225,
                    }

metric = {'g': 1,
          'kg': 1000,
          'liter': 1000,
          'mL': 1,
          }

us_volumes.update(metric)
imperial_volumes.update(metric)

unit_to_base = {'us': us_volumes,
                'imperial': imperial_volumes,
                }
