# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 23:02:22 2024

@author: AldenYellowhorse
"""

import re
from recipe_scrapers import scrape_me
from datastructures import Recipe


class Harvester:
    """This class automates the process of assembling a list of recipes from a
    list of website URLs."""

    @staticmethod
    def get_recipes(URL_list):
        """Iterate over a list of URLs and generate associated recipes."""
        recipe_list = []
        for url in URL_list:
            scraper = scrape_me(url)
            recipe = Harvester.get_recipe(scraper)
            recipe_list.append(recipe)

    @staticmethod
    def get_recipe(scraper: scrape_me):
        """From a scrape_me object, construct a recipe."""
        ingredients = [Harvester.process_step(txt) for txt in
                       scraper.ingredients()]
        new_recipe = Recipe(name=scraper.title(),
                            array=ingredients(),
                            instructions=scraper.instructions())
        return new_recipe

    @staticmethod
    def process_step(step: str):
        """For a given step (str), convert it to an ingredient or string
        instruction."""
        vulgar_step = Harvester.swap_vulgar_values(step)
        filtered_step = Harvester.parse_text(vulgar_step)
        return filtered_step

    @staticmethod
    def swap_vulgar_values(text):
        """Take the vulgar fraction and return the equivalent float."""
        mapping = {'\u00bc': 0.25,
                   '\u2153': 0.33,
                   '\u00bd': 0.5,
                   '\u2154': 0.66,
                   '\u00be': 0.75}
        target = list(text)
        for i, char in enumerate(target):
            if char in mapping:
                target[i] = str(mapping[char])

        return "".join(target)

    @staticmethod
    def str_to_number(text):
        """convert a number (str) to float assuming it consists only of digits,
        decimals and whitespace."""
        numbers = text.split()
        value = sum([float(i) for i in numbers])
        return value

    @staticmethod
    def parse_text(text):
        """Extract the numeric value and ingredient from the text."""
        number = '([0-9.\\s]*)'
        unit = '((cups)|(cup)|(teaspoons)|(teaspoon)|(egg))'
        unit = '(cups|cup|teaspoons|teaspoon|tablespoon|egg)'
        name = '([\\D\\s]*)'
        rule = re.compile(number + unit + name)
        m = rule.match(text)
        if m is not None:
            n, u, t = m.groups()
            n = Harvester.str_to_number(n)
            if u == 'cups':
                u = 'cup'
            if u == 'tablespoons':
                u = 'tablespoon'
            if u == 'teaspoons':
                u = 'teaspoon'
            return (n, u, t)
        else:
            return m


urls = ['https://www.allrecipes.com/recipe/24059/creamy-rice-pudding/']

# recipes = Harvester.get_recipes(urls)
scraper = scrape_me(urls[0])
