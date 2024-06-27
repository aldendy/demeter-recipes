# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 23:02:22 2024

@author: AldenYellowhorse
"""

import re
from recipe_scrapers import scrape_me


url = 'https://www.allrecipes.com/recipe/24059/creamy-rice-pudding/'
scraper = scrape_me(url)


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


def str_to_number(text):
    """convert a string number to a float assuming it consists only of digits,
    decimals and whitespace."""
    numbers = text.split()
    value = sum([float(i) for i in numbers])
    return value


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
        n = str_to_number(n)
        if u == 'cups':
            u = 'cup'
        if u == 'tablespoons':
            u = 'tablespoon'
        if u == 'teaspoons':
            u = 'teaspoon'
        return (n, u, t)
    else:
        return m


res = []
for text in scraper.ingredients():
    res.append(swap_vulgar_values(text))

for i in res:
    m = parse_text(i)
    print(m)
