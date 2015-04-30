from __future__ import division
import math
import operator
import time
import random
import copy
import sys
import ast
from collections import Counter


##################################################
# data class to hold csv data
##################################################
class data():
    def __init__(self, classifier):
        self.examples = []
        self.attributes = []
        self.attr_types = []
        self.classifier = classifier
        self.class_index = None

##################################################
# function to read in data from the .csv files
##################################################
def read_data(dataset, datafile, datatypes):
    print "Reading data..."
    f = open(datafile)
    original_file = f.read()
    rowsplit_data = original_file.splitlines()
    dataset.examples = [rows.split(',') for rows in rowsplit_data]

    #list attributes
    dataset.attributes = dataset.examples.pop(0)

    
    #create array that indicates whether each attribute is a numerical value or not
    attr_type = open(datatypes) 
    orig_file = attr_type.read()
    dataset.attr_types = orig_file.split(',')

##################################################
# Preprocess dataset
##################################################
def preprocess(dataset):
    print "Preprocessing data..."
    averages = [0] * len(dataset.attributes)
    total = len(dataset.examples)
    for attr_index in range(len(dataset.attributes)):
        attr_sum = 0
        for example in dataset.examples:
            if (example[attr_index] == '?'):
                total -= 1
            else:
                attr_sum += float(example[attr_index])
        averages[attr_index] = attr_sum/total
    for example in dataset.examples:
        for attr_index in range(len(dataset.attributes)):
            if(example[attr_index] == '?'):
                example[attr_index] = averages[attr_index]



def preprocess2(dataset):
    print "Preprocessing data..."

    class_values = [example[dataset.class_index] for example in dataset.examples]
    class_mode = Counter(class_values)
    class_mode = class_mode.most_common(1)[0][0]
                         
    for attr_index in range(len(dataset.attributes)):
        #if (dataset.attr_types[attr_index] ==
        ex_0class = filter(lambda x: x[dataset.class_index] == '0', dataset.examples)
        values_0class = [example[attr_index] for example in ex_0class]  
                           
        ex_1class = filter(lambda x: x[dataset.class_index] == '1', dataset.examples)
        values_1class = [example[attr_index] for example in ex_1class]
                
        values = Counter(values_0class)
        value_counts = values.most_common()
        
        mode0 = values.most_common(1)[0][0]
        if mode0 == '?':
            mode0 = values.most_common(2)[1][0]
        # print str(mode0) 

        values = Counter(values_1class)
        mode1 = values.most_common(1)[0][0]
        
        if mode1 == '?':
            mode1 = values.most_common(2)[1][0]
        # print str(mode1)

        mode_01 = [mode0, mode1]
        # print str(mode_01)

        attr_modes = [0]*len(dataset.attributes)
        attr_modes[attr_index] = mode_01
        
        for example in dataset.examples:
            if (example[attr_index] == '?'):
                if (example[dataset.class_index] == '0'):
                    example[attr_index] = attr_modes[attr_index][0]
                elif (example[dataset.class_index] == '1'):
                    example[attr_index] = attr_modes[attr_index][1]
                else:
                    example[attr_index] = class_mode
                    
               
            


##################################################
# tree node class that will make up the tree
##################################################
class treeNode():
    def __init__(self, is_leaf, classification, attr_split_index, attr_split_value, parent, upper_child, lower_child, height):
        self.is_leaf = True
        self.classification = None
        self.attr_split = None
        self.attr_split_index = None
        self.attr_split_value = None
        self.parent = parent
        self.upper_child = None
        self.lower_child = None
        self.height = None



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
    
def compute_tree(dataset, parent_node, classifier):
    # print dataset.examples
    node = treeNode(True, None, None, None, parent_node, None, None, 0)
    if (parent_node == None):
        node.height = 0
    else:
        node.height = node.parent.height + 1
    # print node.height
    ones = one_count(dataset.examples, dataset.attributes, classifier)
    if (len(dataset.examples) == ones):
        node.classification = 1
        node.is_leaf = True
        return node
    elif (ones == 0):
        node.classification = 0
        node.is_leaf = True
        return node
    else:
        node.is_leaf = False
    attr_to_split = None # The index of the attribute we will split on
    max_gain = 0 # The gain given by the best attribute
    split_val = None 
    min_gain = 0.01
    dataset_entropy = calc_dataset_entropy(dataset, classifier)
    for attr_index in range(len(dataset.examples[0])):
        # split_val = best value we could find to split on
        # if gain > max_gain and gain > min_gain
            # attr_to_split = attribute
        if (dataset.attributes[attr_index] != classifier):
            local_max_gain = 0
            local_split_val = None
            attr_value_list = [example[attr_index] for example in dataset.examples] # these are the values we can split on, now we must find the best one
            attr_value_list = list(set(attr_value_list)) # remove duplicates from list of all attribute values
            if(len(attr_value_list) > 100):
                attr_value_list = sorted(attr_value_list)
                total = len(attr_value_list)
                ten_percentile = int(total/10)
                new_list = []
                for x in range(1, 10):
                    new_list.append(attr_value_list[x*ten_percentile])
                attr_value_list = new_list

            for val in attr_value_list:
                # calculate the gain if we split on this value
                # if gain is greater than local_max_gain, save this gain and this value
                local_gain = calc_gain(dataset, dataset_entropy, val, attr_index) # calculate the gain if we split on this value
                # print "LOCAL GAIN: " + str(local_gain)  
                if (local_gain > local_max_gain):
                    local_max_gain = local_gain
                    local_split_val = val

            if (local_max_gain > max_gain):
                max_gain = local_max_gain
                split_val = local_split_val
                attr_to_split = attr_index
            # print "LOCAL MAX GAIN: " + str(local_max_gain)

    #attr_to_split is now the best attribute according to our gain metric
    if (split_val is None or attr_to_split is None):
        print "Something went wrong. Couldn't find an attribute to split on or a split value."
    elif (max_gain <= min_gain or node.height > 20):
        # print "Unable to find an effective split. Branch is complete."
        node.is_leaf = True
        node.classification = classify_leaf(dataset, classifier)
        # print dataset_entropy
        return node

    # print "MAX GAIN: " + str(max_gain)
    node.attr_split_index = attr_to_split
    node.attr_split = dataset.attributes[attr_to_split]
    node.attr_split_value = split_val
    # currently doing one split per node so only two datasets are created
    upper_dataset = data(classifier)
    lower_dataset = data(classifier)
    upper_dataset.attributes = dataset.attributes
    lower_dataset.attributes = dataset.attributes
    upper_dataset.attr_types = dataset.attr_types
    lower_dataset.attr_types = dataset.attr_types
    for example in dataset.examples:
        if (attr_to_split is not None and example[attr_to_split] >= split_val):
            upper_dataset.examples.append(example)
        elif (attr_to_split is not None):
            lower_dataset.examples.append(example)

    node.upper_child = compute_tree(upper_dataset, node, classifier)
    node.lower_child = compute_tree(lower_dataset, node, classifier)

    return node

##################################################
# Classify dataset
##################################################
def classify_leaf(dataset, classifier):
    ones = one_count(dataset.examples, dataset.attributes, classifier)
    total = len(dataset.examples)
    zeroes = total - ones
    if (ones >= zeroes):
        return 1
    else:
        return 0

##################################################
# Calculate the entropy of the current dataset
##################################################
def calc_dataset_entropy(dataset, classifier):
    ones = one_count(dataset.examples, dataset.attributes, classifier)
    total_examples = len(dataset.examples);
    # if (ones == total_examples or ones == 0):
    #     return 0
    entropy = 0
    p = ones / total_examples
    if (p != 0):
        entropy += p * math.log(p, 2)
    p = (total_examples - ones)/total_examples
    if (p != 0):
        entropy += p * math.log(p, 2)
    # if (entropy == 0):
        # print "ONES: " + str(ones)
        # print "TOTAL: " + str(total_examples)
    entropy = -entropy
    return entropy

##################################################
# Calculate the gain of a particular attribute split
##################################################
def calc_gain(dataset, entropy, val, attr_index):
    classifier = dataset.attributes[attr_index]
    attr_entropy = 0
    total_examples = len(dataset.examples);
    gain_upper_dataset = data(classifier)
    gain_lower_dataset = data(classifier)
    gain_upper_dataset.attributes = dataset.attributes
    gain_lower_dataset.attributes = dataset.attributes
    gain_upper_dataset.attr_types = dataset.attr_types
    gain_lower_dataset.attr_types = dataset.attr_types
    for example in dataset.examples:
        if (example[attr_index] >= val):
            gain_upper_dataset.examples.append(example)
        elif (example[attr_index] < val):
            gain_lower_dataset.examples.append(example)

    if (len(gain_upper_dataset.examples) == 0 or len(gain_lower_dataset.examples) == 0): #Splitting didn't actually split (we tried to split on the max or min of the attribute's range)
        return -1

    attr_entropy += calc_dataset_entropy(gain_upper_dataset, classifier)*len(gain_upper_dataset.examples)/total_examples
    attr_entropy += calc_dataset_entropy(gain_lower_dataset, classifier)*len(gain_lower_dataset.examples)/total_examples
    # print "Attr entropy: " + str(attr_entropy)

    return entropy - attr_entropy

##################################################
# count number of examples with classification "1"
##################################################
def one_count(instances, attributes, classifier):
    count = 0
    class_index = None
    #find index of classifier
    for a in range(len(attributes)):
        if attributes[a] == classifier:
            class_index = a
        else:
            class_index = len(attributes) - 1
    for i in instances:
        if i[class_index] == "1":
            count += 1
    return count

##################################################
# Validate tree
##################################################
def validate_tree(node, dataset):
    total = len(dataset.examples)
    correct = 0
    for example in dataset.examples:
        # validate example
        correct += validate_example(node, example)
    print "Score: " + str(100*correct/total) +"%"

##################################################
# Validate example
##################################################
def validate_example(node, example):
    if (node.is_leaf == True):
        projected = node.classification
        actual = int(example[-1])
        # print "Projected: " + str(projected)
        # print "Actual:    " + str(actual)
        if (projected == actual):
            # print "TRUUUUUU" 
            return 1
        else:
            # print "NAHHHH"
            return 0
    value = example[node.attr_split_index]
    if (value >= node.attr_split_value):
        return validate_example(node.upper_child, example)
    else:
        return validate_example(node.lower_child, example)

##################################################
# Print tree
##################################################
def print_tree(node):
    if (node.is_leaf == True):
        for x in range(node.height):
            print "\t",
        print "Classification: " + str(node.classification)
        return
    for x in range(node.height):
            print "\t",
    print "Split index: " + str(node.attr_split)
    for x in range(node.height):
            print "\t",
    print "Split value: " + str(node.attr_split_value)
    print_tree(node.upper_child)
    print_tree(node.lower_child)

##################################################
# Print tree in disjunctive normal form
##################################################
def print_disjunctive(node, dataset, dnf_string):
    if (node.parent == None):
        dnf_string = "( "
    if (node.is_leaf == True):
        if (node.classification == 1):
            dnf_string = dnf_string[:-3]
            dnf_string += ") ^ "
            print dnf_string,
        else:
            return
    else:
        upper = dnf_string + str(dataset.attributes[node.attr_split_index]) + " >= " + str(node.attr_split_value) + " V "
        print_disjunctive(node.upper_child, dataset, upper)
        lower = dnf_string + str(dataset.attributes[node.attr_split_index]) + " < " + str(node.attr_split_value) + " V "
        print_disjunctive(node.lower_child, dataset, lower)
        return


##################################################
# main function, organize data and execute functions based on input
# need to account for missing data
##################################################
def main():
    # args format: 
        # script.py 
        # <training filename> 
        # <classifier name>
        # <datatypes flag> <datatypes filename>
        # <print flag>
        # <validate tag> <validate filename>
        # <test tag> <test filename>

    args = str(sys.argv)
    args = ast.literal_eval(args)
    if (len(args) < 2):
        print "You have input less than the minimum number of arguments. Go back and read README.txt and do it right next time!"
    elif (args[1][-4:] != ".csv"):
        print "Your training file (second argument) must be a .csv!"
    else:
        datafile = args[1]
        dataset = data("")
        if ("-d" in args):
            datatypes = args[args.index("-d") + 1]
        else:
            datatypes = 'datatypes.csv'
        read_data(dataset, datafile, datatypes)
        arg3 = args[2]
        if (arg3 in dataset.attributes):
            classifier = arg3
        else:
            classifier = dataset.attributes[-1]

        dataset.classifier = classifier

         #find index of classifier
        for a in range(len(dataset.attributes)):
            if dataset.attributes[a] == dataset.classifier:
                dataset.class_index = a
            else:
                dataset.class_index = range(len(dataset.attributes))[-1]

        preprocess2(dataset)

        #convert attributes that are numeric to floats
        for example in dataset.examples:
            for x in range(len(dataset.examples[0])):
                if dataset.attributes[x] == 'True':
                    example[x] = float(example[x])

        print "Computing tree..."
        root = compute_tree(dataset, None, classifier) 
        if ("-p" in args):
            print_disjunctive(root, dataset, "")
            print "\n"
        if ("-v" in args):
            datavalidate = args[args.index("-v") + 1]
            print "Validating tree..."

            validateset = data(classifier)
            read_data(validateset, datavalidate, datatypes)
            for a in range(len(dataset.attributes)):
                if validateset.attributes[a] == validateset.classifier:
                    validateset.class_index = a
                else:
                    validateset.class_index = range(len(validateset.attributes))[-1]
            preprocess2(validateset)

            validate_tree(root, validateset)
        if ("-t" in args):
            #TODO
            print "I FUCKIGN LOVE TESTING"




    # classifier = "winner" #is this enough or can main take inputs where we give the dataset?
    # datafile = 'btrain.csv'
    # datatypes = 'datatypes.csv'
    # datavalidate = 'bvalidate.csv'
    # dataset = data()
    # read_data(dataset, datafile, datatypes)
    # validateset = data()
    # read_data(validateset, datavalidate, datatypes)
    
    # print "Compute tree..."
    # root = compute_tree(dataset, None, classifier) 
    # print "Print tree..."
    # # print_tree(root)
    # print "Validate tree..."
    # validate_tree(root, validateset)

    # # print_disjunctive(root, dataset, "")




if __name__ == "__main__":
	main()