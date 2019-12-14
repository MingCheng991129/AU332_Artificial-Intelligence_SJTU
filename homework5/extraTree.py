## best: numberofTree 600

from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
import numpy as np
import pandas as pd
import csv
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt 
import os
from sklearn.model_selection import ShuffleSplit
import random




# Load data
def load_csv_data(filename):
    file = pd.read_csv(filename)

    data = file[['Elevation', 'Aspect', 'Slope', 'Horizontal_Distance_To_Hydrology', 'Vertical_Distance_To_Hydrology',
                 'Horizontal_Distance_To_Roadways', 'Hillshade_9am', 'Hillshade_Noon', 'Hillshade_3pm', 'Horizontal_Distance_To_Fire_Points',
                 'Wilderness_Area1', 'Wilderness_Area2', 'Wilderness_Area3', 'Wilderness_Area4', 'Soil_Type1',
                 'Soil_Type2', 'Soil_Type3', 'Soil_Type4', 'Soil_Type5', 'Soil_Type6',
                 'Soil_Type7', 'Soil_Type8', 'Soil_Type9', 'Soil_Type10', 'Soil_Type11',
                 'Soil_Type12', 'Soil_Type13', 'Soil_Type14', 'Soil_Type15', 'Soil_Type16',
                 'Soil_Type17', 'Soil_Type18', 'Soil_Type19', 'Soil_Type20', 'Soil_Type21',
                 'Soil_Type22', 'Soil_Type23', 'Soil_Type24', 'Soil_Type25', 'Soil_Type26',
                 'Soil_Type27', 'Soil_Type28', 'Soil_Type29', 'Soil_Type30', 'Soil_Type31',
                 'Soil_Type32', 'Soil_Type33', 'Soil_Type34', 'Soil_Type35', 'Soil_Type36',
                 'Soil_Type37', 'Soil_Type38', 'Soil_Type39', 'Soil_Type40']]
    labels = file['Cover_Type']
    data = np.array(data)
    labels = np.array(labels)
    return data, labels

# Load data
def load_csv_test(filename):
    file = pd.read_csv(filename)

    data = file[['Elevation', 'Aspect', 'Slope', 'Horizontal_Distance_To_Hydrology', 'Vertical_Distance_To_Hydrology',
                 'Horizontal_Distance_To_Roadways', 'Hillshade_9am', 'Hillshade_Noon', 'Hillshade_3pm', 'Horizontal_Distance_To_Fire_Points',
                 'Wilderness_Area1', 'Wilderness_Area2', 'Wilderness_Area3', 'Wilderness_Area4', 'Soil_Type1',
                 'Soil_Type2', 'Soil_Type3', 'Soil_Type4', 'Soil_Type5', 'Soil_Type6',
                 'Soil_Type7', 'Soil_Type8', 'Soil_Type9', 'Soil_Type10', 'Soil_Type11',
                 'Soil_Type12', 'Soil_Type13', 'Soil_Type14', 'Soil_Type15', 'Soil_Type16',
                 'Soil_Type17', 'Soil_Type18', 'Soil_Type19', 'Soil_Type20', 'Soil_Type21',
                 'Soil_Type22', 'Soil_Type23', 'Soil_Type24', 'Soil_Type25', 'Soil_Type26',
                 'Soil_Type27', 'Soil_Type28', 'Soil_Type29', 'Soil_Type30', 'Soil_Type31',
                 'Soil_Type32', 'Soil_Type33', 'Soil_Type34', 'Soil_Type35', 'Soil_Type36',
                 'Soil_Type37', 'Soil_Type38', 'Soil_Type39', 'Soil_Type40']]
    data = np.array(data)
    return data

def extra1(features, labels, features_test, numberOfTree):
    model = ExtraTreesClassifier(n_estimators=numberOfTree)

    model.fit(features, labels)

    predict = model.predict(features_test)

    if os.path.exists("all/predictef.csv") == False:

        with open("all/predictef.csv", "w", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(
                ["Id", "Cover_Type"])
            for i in range(0, len(predict)):
                writer.writerow([(15121 + i), predict[i]])

    return 0
def extraForest(features, labels, features_test, labels_test, numberOfTree):
    
    model = ExtraTreesClassifier(n_estimators=numberOfTree)

    model.fit(features, labels)

    predict = model.predict(features_test)

    score = accuracy_score(labels_test, predict)
    


    return score

def plot(numberOfTree, accuracy):
    
    plt.plot(numberOfTree, accuracy)
    plt.xlabel("number of trees")
    plt.ylabel("accuracy")
    plt.title("Accuracy - Number of Trees")
    plt.grid()
    plt.show()

if __name__ == '__main__':
    features, labels = load_csv_data('all/train.csv')

    features_test = load_csv_test('all/test.csv')

    print('extraForest\r')

    ss = ShuffleSplit(n_splits=5, random_state=random.randint(1, 100), test_size=0.2)

    score = []
    num = []
    extra1(features,labels,features_test,250)
    for numTree in range(50, 850, 50):
        num.append(numTree)

        score_per_lis = []

        for train_index, test_index in ss.split(features):
            train_X, train_y = features[train_index], labels[train_index]
            test_X, test_y = features[test_index], labels[test_index]

            score_per_lis.append(extraForest(train_X, train_y, test_X, test_y, numTree))

        score_per = np.mean(score_per_lis)

        score.append(score_per)

    plot(num, score)

        
