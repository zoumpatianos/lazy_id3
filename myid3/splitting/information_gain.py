"""
Author: Kostas Zoumpatianos
File: ingormation_gain.py
Description: The entropy based information gain splitting point heuristic for the ID3 algorithm
Date: March, 6 2010
"""

from __future__ import division 
from math import log
import operator

from base import Splitting

class InformationGain(Splitting):
    dataset = None
    target_attribute = None
    
    def __init__(self, dataset, target_attribute):
        """
        Constructor for the entropy based splitting method, accepts a dataset and a target attribute
        """
        self.dataset = dataset
        self.target_attribute = target_attribute
        
        
    def calculate_entropy_for(self, subset):
        """
        Calculates the entropy of an examples set.
        """
        sigma = 0
        for value in self.dataset.fields[self.target_attribute]["values"]:
            number_of_examples_with_this_value = 0
            for example in subset:
                if example["columns"][self.target_attribute] == value:
                    number_of_examples_with_this_value += 1
            p = number_of_examples_with_this_value / len(subset)
            if p > 0:
                sigma += -1 * p * log(p,2)

        return sigma

    
    def calculate_gains_for(self, subset, entropy, do_not_expand):
        """
        Calculates the gains for an examples set using the entropy.
        """
        gains = {}#[0] * len(self.dataset.fields) # Array with gains for each field
        # For each field
        for field_number in range(0, subset[0]["column_size"]):
            
            # Skip fields that have already been chosen back in the path from root
            if(field_number in do_not_expand):
                continue
                
            sigma = 0
            for value in self.dataset.fields[field_number]["values"]:
                s_v = []
                
                for example in subset:
                    if example["columns"][field_number] == value:
                        s_v += [example]
                
                if len(s_v) > 0:
                    ratio = len(s_v) / len(subset)
                    sigma += ratio * self.calculate_entropy_for(s_v)
                
            gains[field_number] = entropy - sigma
        
       
        return gains
        
    
    def make_choice(self, current_index, subset, do_not_expand):
        """
        Makes a splitting choice, returns -1 if we have reached the end of a branch (a leaf)
        and we do not need to make any more splits.
        """    
        entropy = self.calculate_entropy_for(subset) # Calculate the entropy of the subset
        if entropy == 0: # If the set is ordered then there is only one value for the target function for this subset.
            return -1    # return -1 to tell that we have found a leaf node and we need no further choices.
            
        gains = self.calculate_gains_for(subset, entropy, do_not_expand)
        if(gains == {}): # If there are no more choices to be made then return -1 to tell that we have found a leaf
            return -2    # and that we cannot make anymore choices.
        else:
            return max(gains.iteritems(), key=operator.itemgetter(1))[0]
        
       