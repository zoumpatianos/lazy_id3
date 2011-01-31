"""
Author: Kostas Zoumpatianos
File: splitting/base.py
Description: The base class for splitting methods...
Date: March, 6 2010
"""

class Splitting(object):
    """ Must never be instantiated, only use subclasses! """
    
    def __init__(self, dataset, target_attribute):
        """
        Constructor for splitting methods, accepts a dataset and a target attribute
        """
        self.dataset = dataset
        self.target_attribute = target_attribute
   
    def make_choice(self, current_index, subset, do_not_expand):
        """
        Makes a splitting choice
        """
        pass