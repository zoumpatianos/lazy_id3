"""
Author: Kostas Zoumpatianos
File: kfold.py
Description: The kfold validation method for decision trees.
Date: March, 6 2010
"""
from __future__ import division
from copy import copy
from base import Validator

class KFold(Validator):
    dataset = None
    subsets = []
    current_testing_fold = 0
    training_set = None
    testing_set = None
    target_attribute = None
    
    def __init__(self, dataset, target_attribute, k=10):
        self.dataset = dataset
        self.target_attribute = target_attribute
        subsets_size = round(len(self.dataset.records)/k)
        
        for i in range(0,k):
            # Copy the dataset K times, and each time keep subsets_size elements for testing
            training_dataset = copy(self.dataset)
            testing_dataset = copy(self.dataset)
            
            testing_dataset.records = self.dataset.records[int(subsets_size*i):int(subsets_size*(i+1))]
            training_dataset.records = dataset.records[:int(subsets_size*i)] 
            training_dataset.records += self.dataset.records[int(subsets_size*(i+1)):]
            
            self.subsets += [(training_dataset, testing_dataset)]
            
            
    def next_subset(self):
        if self.current_testing_fold < len(self.subsets):
            (self.training_set, self.testing_set) = self.subsets[self.current_testing_fold]
            self.current_testing_fold += 1
            return True
        else:
            return False
        
        
    
    