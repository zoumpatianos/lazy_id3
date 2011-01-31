"""
Author: Kostas Zoumpatianos
File: id3.py
Description: An ID3 algorithm implementation for discrete valued datasets.
Date: March, 6 2010
"""

import sys
from copy import copy

from utils.dataset import DataSet
from splitting.information_gain import InformationGain
from splitting.lazy_information_gain import LazyInformationGain

class ID3(object):
    tree = None # The tree created by the ID3 algorithm
    dataset = None # The training dataset
    target_attribute = None # The target attribute
    pivoting_function = None # The splitting function to be used (by default this is set to the entropy heuristic)
    lazy = False

    def __init__(self, dataset, target_attribute, lazy=False):
        
        """
        This is the constructor of the ID3 class, it sets the dataset, target attribute and pivoting function.
        """
        
        self.dataset = dataset 
        self.target_attribute = target_attribute
        self.lazy = lazy
        self.pivoting_function = InformationGain(dataset, target_attribute).make_choice
                    
        
    def train(self, instance=None):
        
        """
        This function creates the tree.
        """
        if self.lazy and instance:
            # Prune dataset to the part of the data that really matter for the tree that is built!
            (new_dataset, unvisitable_pivots) = self._prune_data_for(instance)
            
            first_pivot = self.pivoting_function(-1, new_dataset.records, unvisitable_pivots)
            self.tree = self.expand_tree(new_dataset.records, first_pivot, unvisitable_pivots, "root")
        else:
            first_pivot = self.pivoting_function(-1, self.dataset.records, [self.target_attribute])
            self.tree = self.expand_tree(self.dataset.records, first_pivot, [self.target_attribute], "root")
                       
            
            

    def _prune_data_for(self, instance):
        """
        """
        valid_pivots = {}
        unvisitable_pivots = []
        new_records = []

        new_dataset = copy(self.dataset)

        for record in new_dataset.records:
            has_at_least_one_same = False

            for findex, field in enumerate(record["columns"]):
                if field == instance[findex]:
                    has_at_least_one_same = True
                    valid_pivots[findex] = 1

            if has_at_least_one_same:
                new_records += [record]

        new_dataset.records = new_records
        for findex, field in enumerate(new_dataset.fields):
            if not findex in valid_pivots:
                unvisitable_pivots += [findex]

        return (new_dataset, unvisitable_pivots)
            
    

        
    def expand_tree(self, examples, index, do_not_expand, prev_value):
        
        """
        This function gets a list of examples as input and expands it on the field that is specified with the
        index parameter. i.e. expand_tree(examples, 1,[]) would branch the tree on the value of the second 
        field, it calls its self recursively. The do_not_expand parameter should contain a set of field ids
        that we do not want to expand on (i.e. the fields on which we have already expanded), in order to avoid
        chosing the same pivot over and over.
        """
        children = []
        
        # Find all values of the example set for the selected field
        

        #values = dict(zip(map(lambda x:x["columns"][index],examples),[""]*examples[0]["column_size"])).keys()
        values = []
        for example in examples:
            if example["columns"][index] not in values:
                values += [example["columns"][index]]
        
        # Add the index of the field that we expand in the "black list", so that it won't be expanded again in this branch.
        
        
        # For all values of this field (index), that appear in the examples
        for value in values:
            # Find all the examples that have this value in the selected field
            children_with_value = filter(lambda x: x, 
                                         map(lambda x: x["columns"][index]==value and x, 
                                             examples)
                                        )
                                        
            # For the set of examples that have this value, find all the values for the target field
            target_attribute_values = dict(zip(
                                                 map(lambda x: x["columns"][self.target_attribute], children_with_value), 
                                                 children_with_value)
                                           ).keys()      
            
            # For the examples that have this value, choose a new splitting point and branch on it                                
            next_attribute = self.pivoting_function(index,children_with_value, do_not_expand+[index])
            #print ("for", value, "that comes from", prev_value, "I will split to", next_attribute,
            #       "and I have already split at", do_not_expand)
            
            # If this splitting point is greater than -1 and there are more than one target values
            
            if next_attribute > -1 and len(target_attribute_values)>1:
                # Branch on this splitting point
                children += [((index,value,"node"),self.expand_tree(children_with_value,next_attribute, do_not_expand+[index], value))]
            else:
                # We have only one target value for the subset, attach it and end recurssion
                #children += [((index,value,"leaf"),children_with_value,target_attribute_values)]
                children += [((index,value,"leaf"),target_attribute_values)]
                
        return children             

 
    def print_tree(self,tree=None,tabs=0, parents=[]):
        """
        This function prints the tree in the console.
        """
        if not tree:
            tree = self.tree

        for record in tree:
            print "|\t"*tabs+"|"+"--"*tabs + "> %s = %s" % (self.dataset.fields[record[0][0]]["name"], record[0][1] )
            if(record[0][2]=="leaf"):
                print "|\t"*(tabs+1)+"|"+"--"*(tabs+1) + "> [ %s =  %s ]" % (self.dataset.fields[self.target_attribute]["name"],
                                                                             str(record[1][0])) 
            else:
                self.print_tree(record[1],tabs+1, parents + [record[0]])
