# -*- coding: utf-8 -*-
"""
Created on Sat Jul  6 12:27:58 2024

@author: AldenYellowhorse

In this script, we assemble a range of test recipes to ensure that the code
imports recipes as required. This has proved to be a serious issue with other
recipe importers. They look capable but when it comes time to import, they have
many failures in correctly gathering recipe data.
"""

url = r'https://www.allrecipes.com/recipe/24059/creamy-rice-pudding/'
test_urls = {'all recipes rice pudding': url}

url = r'https://foodnetwork.co.uk/recipes/bruschetta'
test_urls['food network bruschetta'] = url

url = r'https://www.tasteofhome.com/recipes/slow-cooker-baby-back-ribs/'
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
