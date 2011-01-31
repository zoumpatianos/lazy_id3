"""
Author: Kostas Zoumpatianos
File: validation/base.py
Description: The base validation method for decision trees, returns accuracy between a training and a testing set.
Date: March, 6 2010
"""

from __future__ import division

class Validator(object):
    dataset = None
    training_set = None
    testing_set = None
    target_attribute = None

  
    def get_answer_for(self,tree,query,tabs=0):
        for record in tree:
            if query["columns"][record[0][0]] == record[0][1]:
                if record[0][2] == "leaf":
                    return record[1][0]
                else:
                    return self.get_answer_for(record[1], query, tabs+1)
        return -1
            
            
    def get_accuracy_of(self, tree):
        """
        acc = (1/len(testing_set)) * [for_all(x in testing_set): sum(is_same(prediction(x), real(x)))]
        
        """
        if(len(self.testing_set.records) == 0):
            return 1
            
        unclass = 0
        sigma = 0
        misclass = 0
        for index,record in enumerate(self.testing_set.records):
            target_value = self.get_answer_for(tree=tree,query=record)
            if(target_value == -1):
                unclass += 1
            elif(target_value == record["columns"][self.target_attribute]):
                sigma += 1
            elif(target_value != record["columns"][self.target_attribute]):
                misclass += 1
            
        #print "Misclassified: ", misclass/len(self.testing_set.records)
        #print "Unclassified:", unclass/len(self.testing_set.records)
        
        accuracy = (1/len(self.testing_set.records)) * sigma 
        return accuracy