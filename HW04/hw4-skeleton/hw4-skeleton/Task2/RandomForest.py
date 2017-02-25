import csv
import numpy as np  # http://www.numpy.org
import ast
from collections import Counter
import math

"""
Here, X is assumed to be a matrix with n rows and d columns
where n is the number of total records
and d is the number of features of each record
Also, y is assumed to be a vector of d labels

XX is similar to X, except that XX also contains the data label for
each record.
"""

"""
This skeleton is provided to help you implement the assignment. It requires
implementing more that just the empty methods listed below.

So, feel free to add functionalities when needed, but you must keep
the skeleton as it is.
"""

class RandomForest(object):
    class __DecisionTree(object):
        def __init__(self):
            self.tree = {}
            self.maxdepth = 17

        def learn(self, X, y, attributes):
            # TODO: train decision tree and store it in self.tree
            self.tree = self.buildTree(X, y, 0, attributes)

        def classify(self, record):
            # TODO: return predicted label for a single record using self.tree
            return self.traverse(record, self.tree)

        def buildTree(self, X, y, depth, attributes):
            if y.tolist().count(y[0]) == len(y):
                return y[0]
            if len(set(y)) == 1:
                return set(y).pop()
            if self.maxdepth == depth or len(X[0]) == 1 or len(attributes) == 0:
                return np.bincount(y).argmax()
            index = self.findIndex(X, y, attributes)
            if index == -1:
                return y
            t = {index : {}}
            attributes.remove(index)
            vals = [row[index] for row in X]
            for val in np.unique(vals):
                t[index][val] = self.buildTree(self.split2(X, index, val), self.split1(X, y, index, val), depth + 1, attributes)
            return t

        def split1(self, x, y, i, val):
            splitted = []
            newx = x.tolist()
            newy = y.tolist()
            xy = zip(newx,newy)
            for row in xy:
                if row[0][i] == val:
                    splitted.append(row[1])
            return np.array(splitted)

        def split2(self, x, i, val):
            splitted = []
            newx = x.tolist()
            for row in newx:
                if row[i] == val:
                    splitted.append(row)
            return np.array(splitted)

        def entropy(self, y):
            temp = y.tolist()
            frequency = [float(temp.count(i)) / len(temp) for i in [0,1]]
            ret = 0.0
            for datum in frequency:
                if datum != 0.0:
                    ret -= datum * np.log2(datum)
            return ret

        def findIndex(self, x, y, attributes):
            rValue = self.entropy(y)
            maxgain = 0.0
            targetAttribute = -1
            for i in attributes:
                col = [row[i] for row in x]
                uniqueValues = np.unique(col)
                temp = 0.0
                for j in uniqueValues:
                    splitted = self.split1(x, y, i, j)
                    temp += len(splitted)/float(len(y)) * self.entropy(splitted)
                gain = rValue - temp
                if gain > maxgain:
                    maxgain = gain
                    targetAttribute = i
            return targetAttribute

        def traverse(self, record, tree):
            attribute = tree.keys()[np.random.randint(len(tree))]
            t = tree[attribute]
            label = 0
            for key in t.keys():
                try:
                    if float(record[attribute]) == key:
                        if type(t[key]) == type({}):
                            label = self.classify(t[key], record)
                        else:
                            label = t[key]
                except:
                    return 0
            return label

    num_trees = 0
    decision_trees = []
    bootstraps_datasets = [] # the bootstrapping dataset for trees
    bootstraps_labels = []   # the true class labels,

    def __init__(self, num_trees):
        # TODO: do initialization here.
        self.num_trees = num_trees
        self.decision_trees = [self.__DecisionTree() for i in range(num_trees)]

    def _bootstrapping(self, XX, n):
        # TODO: create a sample dataset with replacement of size n
        #
        # Note that you will also need to record the corresponding
        #           class labels for the sampled records for training purpose.
        #
        # Reference: https://en.wikipedia.org/wiki/Bootstrapping_(statistics)
        bootstrapped = np.random.choice(range(len(XX)), n)
        data = np.array(XX, dtype=float)
        data = data[bootstrapped]
        samples = []
        labels = []
        for sample in data:
            samples.append(sample[:-1])
            labels.append(int(sample[-1]))
        return (np.array(samples), np.array(labels))

    def bootstrapping(self, XX):
        # TODO: initialize the bootstrap datasets for each tree.
        for i in range(self.num_trees):
            data_sample, data_label = self._bootstrapping(XX, len(XX))
            self.bootstraps_datasets.append(data_sample)
            self.bootstraps_labels.append(data_label)

    def fitting(self):
        # TODO: train `num_trees` decision trees using the bootstraps datasets and labels
        for i in range(len(self.decision_trees)):
            tree = self.decision_trees[i]
            data = self.bootstraps_datasets[i]
            label = self.bootstraps_labels[i]
            m = len(data[0])
            attributes = np.random.choice(len(data[0]), m, replace=False).tolist()
            tree.learn(data, label, attributes)


    def voting(self, X):
        y = np.array([], dtype = int)
        for record in X:
            # TODO: find the sets of proper trees that consider the record
            #       as an out-of-bag sample, and predict the label(class) for the record.
            #       The majority vote serves as the final label for this record.
            votes = []
            for i in range(len(self.bootstraps_datasets)):
                dataset = self.bootstraps_datasets[i]
                if record.tolist() in dataset.tolist():
                    OOB_tree = self.decision_trees[i]
                    effective_vote = OOB_tree.classify(record)
                    votes.append(effective_vote)
            counts = np.bincount(votes)
            if len(counts) == 0:
                # TODO: special handling may be needed.
                y = np.append(y, np.random.randint(2))
            else:
                y = np.append(y, np.argmax(counts))
        return y

def main():
    X = list()
    y = list()
    XX = list() # Contains data features and data labels

    # Note: you must NOT change the general steps taken in this main() function.

    # Load data set
    with open("hw4-data.csv") as f:
        next(f, None)

        for line in csv.reader(f, delimiter = ","):
            X.append(line[:-1])
            y.append(line[-1])
            xline = [ast.literal_eval(i) for i in line]
            XX.append(xline[:])

    # Initialize according to your implementation
    forest_size = 10

    # Initialize a random forest
    randomForest = RandomForest(forest_size)

    # Create the bootstrapping datasets
    randomForest.bootstrapping(XX)

    # Build trees in the forest
    randomForest.fitting()

    # Provide an unbiased error estimation of the random forest
    # based on out-of-bag (OOB) error estimate.
    # Note that you may need to handle the special case in
    #       which every single record in X has used for training by some
    #       of the trees in the forest.
    y_truth = np.array(y, dtype = int)
    X = np.array(X, dtype = float)
    y_predicted = randomForest.voting(X)

    #results = [prediction == truth for prediction, truth in zip(y_predicted, y_test)]
    results = [prediction == truth for prediction, truth in zip(y_predicted, y_truth)]

    # Accuracy
    accuracy = float(results.count(True)) / float(len(results))
    print "accuracy: %.4f" % accuracy

main()
