# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from sklearn.naive_bayes import GaussianNB
import csv
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import MultinomialNB
import matplotlib.pyplot  as plt
# Load data
def load_csv_data(filename):
    file = pd.read_csv(filename)

    data = file[['Elevation', 'Aspect', 'Slope', 'Horizontal_Distance_To_Hydrology', 'Vertical_Distance_To_Hydrology',
                 'Horizontal_Distance_To_Roadways', 'Hillshade_9am', 'Hillshade_Noon', 'Hillshade_3pm', 'Horizontal_Distance_To_Fire_Points']]
    labels = file['Cover_Type']
    data = np.array(data)
    labels = np.array(labels)
    return data, labels
def load_csv_data1(filename):
    file = pd.read_csv(filename)

    data = file[[
                 'Wilderness_Area', 'Soil_Type']]
    labels = file['Cover_Type']
    data = np.array(data)
    labels = np.array(labels)
    return data, labels

# Load data
def load_csv_test(filename):
    file = pd.read_csv(filename)

    data = file[['Elevation', 'Aspect', 'Slope', 'Horizontal_Distance_To_Hydrology', 'Vertical_Distance_To_Hydrology',
                 'Horizontal_Distance_To_Roadways', 'Hillshade_9am', 'Hillshade_Noon', 'Hillshade_3pm', 'Horizontal_Distance_To_Fire_Points',
                 'Wilderness_Area1', 'Wilderness_Area2', 'Wilderness_Area3', 'Wilderness_Area4', 'Soil_Type']]
    labels = file['Cover_Type']
    data = np.array(data)
    labels = np.array(labels)
    return data
# Load data
def load_csv_test1(filename):
    file = pd.read_csv(filename)

    data = file[['Wilderness_Area1', 'Wilderness_Area2', 'Wilderness_Area3', 'Wilderness_Area4']]
    data = np.array(data)
    labels = file['Cover_Type']
    labels = np.array(labels)
    return data, labels

# LogisticRegression
def testLogisticRegression(features, labels, features_test):

    rf2 = GaussianNB()

    # train
    rf2.fit(features, labels)

    # predict
    predict = rf2.predict(features_test)

    # write csv
    with open("all/predict-nb.csv", "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            ["Id", "Cover_Type"])
        for i in range(0, len(predict)):
            writer.writerow([(15121 + i), predict[i]])
def test(features, labels):



    with open("all/predict-2222.csv", "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            ["Id", "Cover_Type"])
        for i in range(0, len(labels)):
            for j in range(0,4):
                if(features[i][j]!=0):
                    writer.writerow([(i),j])


def knn1(features, features1,labels,features_test,features_test1,labels_test,i):
    gnb = GaussianNB()
    mnnb=MultinomialNB(alpha=i/10)
    gnb.fit(features, labels)
    mnnb.fit(features1,labels)
    predict1 = gnb.predict_proba(features_test)
    predict2=mnnb.predict_proba(features_test1)
    predict=np.argmax(np.multiply(predict1,predict2), axis=1)+1
    return accuracy_score(labels_test, predict)

if __name__ == '__main__':
    features, labels = load_csv_data('all/train.csv')
    features1, labels = load_csv_data1('all/train.csv')
    features2, labels2=load_csv_test1('all/train.csv')
    #test(features2,labels2)



    kf = KFold(n_splits=5)
    average=0
    x=[]
    result=[]
    for i in range(100):
        average=0
        for train_index, test_index in kf.split(features):
            train_X, train_y = features[train_index], labels[train_index]
            train_X1= features1[train_index]
            test_X, test_y = features[test_index], labels[test_index]
            test_X1 = features1[test_index]
            average+=knn1(train_X,train_X1,train_y,test_X,test_X1,test_y,i)
        result.append((average/5))
        x.append(i)
    plt.plot(x,result)
    plt.xlabel('the alpha of laplace')
    plt.ylabel('accuracy of bayes')
    plt.show()
