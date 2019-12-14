from sklearn import neighbors
import random
import numpy as np
import pandas as pd
import csv
from sklearn.model_selection import ShuffleSplit
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot  as plt
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

# LogisticRegression
def knn(features, labels, features_test):
    knn = neighbors.KNeighborsClassifier(n_neighbors=1)

    # train
    knn.fit(features, labels)

    # predict
    predict = knn.predict(features_test)

    # write csv
    with open("all/predict-knn.csv", "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            ["Id", "Cover_Type"])
        for i in range(0, len(predict)):
            writer.writerow([(15121 + i), predict[i]])

def knn1(features, labels,features_test,labels_test,i):
    knn = neighbors.KNeighborsClassifier(n_neighbors=i, metric = 'minkowski', p = 2)

    # train
    knn.fit(features, labels)
    predict = knn.predict(features_test)
    return accuracy_score(labels_test, predict)



if __name__ == '__main__':
    features, labels = load_csv_data('all/train.csv')

    features_test = load_csv_test('all/test.csv')
    knn(features,labels,features_test)
    print('knn\r')
    result=[]
    x=[]
    #knn(features, labels, features_test)
    kf = ShuffleSplit(n_splits=5, random_state=random.randint(1, 100), test_size=0.2)
    for i in range(1,10):
        average = 0
        for train_index, test_index in kf.split(features):
            train_X, train_y = features[train_index], labels[train_index]
            test_X, test_y = features[test_index], labels[test_index]
            average+=knn1(train_X,train_y,test_X,test_y,i)
        print(average / 5)
        result.append((average/5))
        x.append(i)
    plt.plot(x,result)
    plt.xlabel('the k of knn')
    plt.ylabel('accuracy of knn')
    plt.show()
