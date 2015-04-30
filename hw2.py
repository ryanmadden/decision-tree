from __future__ import division
import math
import operator
import time
import random
import copy
from collections import Counter


##################################################
# data class to import and hold csv data
##################################################
class data:
    def __init__(self, datafile, test=False):
        self.datafile = datafile
        self.read_data()

    def read_data(self):
        f = open('tennis.csv') #make general later
        original_file = f.read()
        rowsplit_data = original_file.split("\r")
        self.examples = [rows.split(',') for rows in rowsplit_data]

        #list attributes
        self.attributes = self.examples.pop(0)
        
        #create array that indicates whether each attribute is a numerical value or not
        attr_type = open('tennistypes.csv') #make general later
        orig_file = attr_type.read()
        self.attr_types = orig_file.split(',')

        #convert attributes that are numeric to floats
        for example in self.examples:
            for x in range(len(self.examples[0])):
                if self.attributes[x] == 'True':
                    example[x] = float(example[x])

        print str(self.examples)
        #print str(orig_file)
        #print str(self.attr_types)

##################################################
# tree node class that will make up the tree
##################################################
class treeNode():
    def __init__(self, is_leaf, classification, attr_split_index, attr_split_value, parent, upper_child, lower_child):
        self.is_leaf = True
        self.classification = None
        self.attr_split_index = None
        self.attr_split_value = None
        self.parent = None
        self.upper_child = None
        self.lower_child = None



##################################################
# compute tree recursively
##################################################
# initialize Tree
    # if dataset is pure (all one result) or there is other stopping criteria then stop
    # for all attributes a in dataset
        # compute information-theoretic criteria if we split on a
    # abest = best attribute according to above
    # tree = create a decision node that tests abest in the root
    # dv (v=1,2,3,...) = induced sub-datasets from D based on abest
    # for all dv
        # tree = compute_tree(dv)
        # attach tree to the corresponding branch of Tree
    # return tree
    
def compute_tree(dataset, parent_node):
    node = treeNode(True, None, None, None, parent_node, None, None)
    classifier = "Play" # TODO generalize target attribute
    ones = one_count(train_data.examples, train_data.attributes, classifier)
    if (len(dataset.examples) == ones):
        node.classification = 1
    elif (ones == 0):
        node.classification = 0
    attr_to_split = None # The index of the attribute we will split on
    max_gain = 0 # The gain given by the best attribute
    split_val = None 
    #TODO impose minimum gain limit
    min_gain = 0
    dataset_entropy = calc_dataset_entropy(dataset)
    for attribute in range(len(dataset.examples[0])):
        # TODO compute gain if we split on a at best value
        # split_val = best value we could find to split on
        # if gain > max_gain and gain > min_gain
            # attr_to_split = attribute


    #attr_to_split is now the best attribute according to our gain metric

    if (max_gain <= min_gain):
        print "Unable to find an effective split. Tree is complete."
    elif (split_val is None or attr_to_split is None):
        print "Something went wrong. Couldn't find an attribute to split on or a split value."

    node.attr_split_index = attr_to_split
    node.attr_split_value = split_val
    # currently doing one split per node so only two datasets are created
    upper_dataset = []
    lower_dataset = []
    for example in dataset.examples
        if (example[attr_to_split] >= split_val):
            upper_dataset.append(example)
        else
            lower_dataset.append(example)

    node.upper_child = compute_tree(upper_dataset, node)
    node.lower_child = compute_tree(lower_dataset, node)

    return node

##################################################
# Calculate the entropy of the current dataset
##################################################
def calc_dataset_entropy(dataset):
    # TODO generalize classifier
    classifier = "Play"
    ones = one_count(dataset.examples, dataset.attributes, classifier)
    total_examples = len(dataset.examples[0]);
    entropy = 0
    p = ones/total_examples
    entropy += p * math.log(p, 2)
    p = (total_examples - ones)/total_examples
    entropy += p * math.log(p, 2)

    return entropy


##################################################
# count number of examples with classification "1"
##################################################
def one_count(instances, attributes, classifier):
    count = 0

    #find index of classifier
    print attributes
    for a in range(len(attributes)):
        if attributes[a] == classifier:
            class_index = a
    
    for i in instances:
        if i[class_index] == "1":
            count += 1

    return count


##################################################
# main function, organize data and execute functions based on input
# need to account for missing data
##################################################
def main():
    train_file = "tennis.csv"
    train_data = data(train_file)

    classifier = "Play"

    ones = one_count(train_data.examples, train_data.attributes, classifier)
    print ones
    
    compute_tree(train_data)




if __name__ == "__main__":
	main()
