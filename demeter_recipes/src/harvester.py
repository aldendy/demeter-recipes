# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 23:02:22 2024

@author: AldenYellowhorse
"""

from recipe_scrapers import scrape_html
from urllib.request import urlopen
from src.datastructures import Recipe


class Harvester:
    """This class automates the process of assembling a list of recipes from a
    list of website URLs."""

    @staticmethod
    def get_recipes(URL_list: list) -> list[Recipe]:
        """Iterate over a list of URLs and generate associated recipes."""
        recipe_list = []
        for url in URL_list:
            html = urlopen(url).read().decode("utf-8")
            recipe = scrape_html(html, org_url=url)
            recipe_list.append(recipe)
        return recipe_list
