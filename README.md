# decision-tree
A C4.5 Decision Tree python implementation with pruning and continuous attribute multi-splitting
Contributors: Ryan Madden and Ally Cody

## Requirements
python 2.7.6 [Download](https://www.python.org/download/releases/2.7.6/)

## How to run
hw2.py accepts parameters passed via the command line. The possible paramters are:
* Filename for training (Required, must be the first argument after 'python hw2.py')
* Classifier name (Optional, by default the classifier is the last column of the dataset)
* Datatype flag (-d) followed by datatype filename (Optional, defaults to 'datatypes.csv')
* Print flag (-s) (Optional, causes the dataset)
* Validate flag (-v) followed by validate filename (Optional, specifies file to use for validation)
* Test flag (-t) followed by test filename (Optional, specifies file to use for testing)
* Pruning flag (-p) (Optional, you must include a validation file in order to prune)

### Example
'''
python hw2.py btrain.csv -v bvalidate.csv -p -t btest.csv
'''
The above command runs hw2.py with btrain.csv as the training set, bvalidate.csv as the validation set, btest.csv as the test set, and pruning enabled. The classifier is not specified so it defaults to the last column in the training set. Printing is not enabled.