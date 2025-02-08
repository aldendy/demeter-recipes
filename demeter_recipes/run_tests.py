# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 22:24:34 2025

@author: alden
"""

import os
from unittest import TestLoader, TextTestRunner

loader = TestLoader()

# use 'test*.py' to run all tests

suite = loader.discover(start_dir=os.getcwd(), pattern='test_imp*.py')

runner = TextTestRunner()
runner.run(suite)
