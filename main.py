"""

"""
from __future__ import division
import sys, getopt

from myid3.utils.dataset import DataSet
from myid3.utils.ordinal import ordinal
from myid3.id3 import ID3
from myid3.validation.holdout import Holdout
from myid3.validation.kfold import KFold

def usage():
    print "Usage: \t python %s" % (sys.argv[0])
    
    
def run_for(dataset, target_attribute, tenfold_validate, holdout_validate, holdout_sample, lazy_find=[]):
    if len(lazy_find) == 0:
        lazy = False
    else:
        lazy = True
    
    if(holdout_validate and tenfold_validate):
        print "Only one validation method is allowed, it will be either 10-fold or Holdout, Not both!"
        sys.exit()
    else:
        # Traing with all data    
        if not lazy:
            id3_instance = ID3(dataset, target_attribute)
            id3_instance.train()
        else:
            id3_instance = ID3(dataset, target_attribute, lazy=True)
            id3_instance.train(lazy_find)

        print "\nTree:"
        id3_instance.print_tree()
    
    if(holdout_validate):
        print "Running ID3 with holdout (%f) validation..." % holdout_sample
        holdout = Holdout(dataset, target_attribute, holdout_sample)
        id3_instance = ID3(holdout.training_set, target_attribute)
        id3_instance.train()
        
        #print "\nTree:"
        #id3_instance.print_tree()
        print "Tree accuracy (by holdout): %f\n" % holdout.get_accuracy_of(id3_instance.tree) 
         
    elif(tenfold_validate):
        print "Running ID3 with 10-Fold validation..."
        
        kfold = KFold(dataset, target_attribute)
        accuracies = []
        while True:
            has_next_subset = kfold.next_subset()
            if not has_next_subset:
                break
            else:
                id3_instance = ID3(kfold.training_set, target_attribute)
                id3_instance.train()
                #print "\nNext Tree"
                #id3_instance.print_tree()
                accuracies += [kfold.get_accuracy_of(id3_instance.tree) ]
        
        accuracy = sum(accuracies)/len(accuracies)
        print "Mean tree accuracy (by 10-fold): %f\n" % accuracy
                
            #accuracy = kfold.get_accuracy_of(id3_instance.tree)
            
        
        sys.exit()
    
    
        


if __name__ == "__main__":
    data = None
    names = None
    target_attribute = None
    holdout_sample = 0
    tenfold_validate = False
    holdout_validate = False
    lazy_find = []
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], "?t:d:n:h:fl:", ["help", "target=", "data=", "names=", "holdout=", "tenfold", "lazy_find="])
    except getopt.GetoptError, err:
        print str(err) 
        usage()
        sys.exit(2)
        
    for o, a in opts:
        if o in ("-?", "--help"):
            usage()
            sys.exit()
        elif o in ("-d", "--data"):
            data = a
        elif o in ("-n", "--names"):
            names = a
        elif o in ("-t", "--target"):
            if(int(a)<0):
                print "Target attribute must be greater or equal to zero!"
                sys.exit()
            target_attribute = int(a)
        elif o in ("-f", "--tenfold"):
            tenfold_validate = True
        elif o in ("-h", "--holdout"):
            holdout_validate = True
            holdout_sample = float(a)
        elif o in("-l", "--lazy_find"):
            lazy_find = a.split(",")
        else:
            assert False, "unhandled option"
    
    
    if(data == None):
        print "No dataset specified!"
        usage()
        sys.exit()
    else:    
        dataset = DataSet(names, data)

    if target_attribute >= len(dataset.fields):
        print "Error: Target attribute cannot be greater than the total number of fields!"
        sys.exit()
    elif target_attribute == None:
        target_attribute = len(dataset.fields) - 1
        print "=" * 100 
        print "!!! Choosing last field as target attribute"
        
    print "=" * 100 
    print "[-] Data file: %s" % data
    print "[-] Names file: %s" % names
    print "[-] Target attribute: '%s' (%s field out of %d)" % (dataset.fields[target_attribute]["name"], ordinal(target_attribute+1), len(dataset.fields))
    print "=" * 100
    
    
    
    
    run_for(dataset, target_attribute, tenfold_validate, holdout_validate, holdout_sample, lazy_find)
    
