"""
Author: Kostas Zoumpatianos
File: holdout.py
Description: The holdout validation method for decision trees.
Date: March, 6 2010
"""

from __future__ import division
from copy import copy
from base import Validator

class Holdout(Validator):
    dataset = None
    training_set = None
    testing_set = None
    target_attribute = None
    
    
    def __init__(self, dataset, target_attribute, holdout_ratio = 0.3):
        self.dataset = copy(dataset)
        self.training_set = copy(dataset)
        self.testing_set = copy(dataset)
        
        split_at = round(len(dataset.records) * holdout_ratio)
        print "Splitting at %d" % (split_at)
        self.testing_set.records = copy(dataset.records[0:int(split_at)])
        print "First %s records are used as testing." % len(self.testing_set.records)
        self.training_set.records = copy(dataset.records[int(split_at):])
        print "Last %s records are used as training." % len(self.training_set.records)
        
        self.target_attribute = target_attribute
        