# -*- coding: utf-8 -*-
"""
Created on Sat Jul  6 12:27:58 2024

@author: AldenYellowhorse

In this script, we assemble a range of test recipes to ensure that the code
imports recipes as required. This has proved to be a serious issue with other
recipe importers. They look capable but when it comes time to import, they have
many failures in correctly gathering recipe data.
"""


from recipe_scrapers import scrape_html
from src.harvester import Harvester
from unittest import TestCase


class TestRecipe(TestCase):
    """Test the full process of scraping a recipe from a website and converting
    it into a recipe object."""

    def setUp(self):
        """Initialize all the required test data."""
        url = r'https://www.allrecipes.com/recipe/24059/creamy-rice-pudding/'
        test_urls = {'all recipes rice pudding': url}

        url = r'https://foodnetwork.co.uk/recipes/bruschetta'
        test_urls['food network bruschetta'] = url

        url = (r'https://www.tasteofhome.com/recipes/'
               'slow-cooker-baby-back-ribs/')
        test_urls['taste of home ribs'] = url

        url = (r'https://www.delish.com/cooking/recipe-ideas/a61488085/'
               'blueberry-scones-recipe/')
        test_urls['delish scones'] = url

        url = r'https://www.bbcgoodfood.com/recipes/strawberry-pavlova'
        test_urls['bbc good food pavlova'] = url

        url = r'https://www.simplyrecipes.com/recipes/blondies/'
        test_urls['simply recipes blondies'] = url

        url = r'https://minimalistbaker.com/vegan-brownie-chocolate-ice-cream/'
        test_urls['minimalist baker'] = url
        self.test_urls = test_urls

    def test_recipe_construction(self):
        """Run the entire process of creating a recipe object. To conserve
        calls to the websites, later tests build off the information collected
        here."""
        urls = [self.test_urls['all recipes rice pudding']]
        h = Harvester()
        recipes = h.get_recipes(urls)
        self.assertEqual(recipes[0].title(), 'Creamy Rice Pudding')
