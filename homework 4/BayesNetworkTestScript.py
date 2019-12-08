#!/usr/bin/env python3

from BayesianNetworks import *
import numpy as np
import pandas as pd

#############################
## Example Tests from Bishop Pattern recognition textbook on page 377
#############################
BatteryState = readFactorTable(['battery'], [0.9, 0.1], [[1, 0]])
FuelState = readFactorTable(['fuel'], [0.9, 0.1], [[1, 0]])
GaugeBF = readFactorTable(['gauge', 'battery', 'fuel'], [0.8, 0.2, 0.2, 0.1, 0.2, 0.8, 0.8, 0.9], [[1, 0], [1, 0], [1, 0]])

carNet = [BatteryState, FuelState, GaugeBF] # carNet is a list of factors 
## Notice that different order of operations give the same answer
## (rows/columns may be permuted)
joinFactors(joinFactors(BatteryState, FuelState), GaugeBF)
joinFactors(joinFactors(GaugeBF, FuelState), BatteryState)

joinFactors(GaugeBF, BatteryState)
marginalizeFactor(joinFactors(GaugeBF, BatteryState), 'gauge')

marginalizeFactor(joinFactors(GaugeBF, BatteryState), 'gauge')
joinFactors(marginalizeFactor(GaugeBF, 'gauge'), BatteryState)

joinFactors(marginalizeFactor(joinFactors(GaugeBF, BatteryState), 'battery'), FuelState)
marginalizeFactor(joinFactors(joinFactors(GaugeBF, FuelState), BatteryState), 'battery')

marginalizeFactor(joinFactors(marginalizeFactor(joinFactors(GaugeBF, BatteryState), 'battery'), FuelState), 'gauge')
marginalizeFactor(joinFactors(marginalizeFactor(joinFactors(GaugeBF, BatteryState), 'battery'), FuelState), 'fuel')

evidenceUpdateNet(carNet, ['fuel'], [1])
evidenceUpdateNet(carNet, ['fuel', 'battery'], [1, 0])

## Marginalize must first combine all factors involving the variable to
## marginalize. Again, this operation may lead to factors that aren't
## probabilities.
marginalizeNetworkVariables(carNet, ['battery']) ## this returns back a list
marginalizeNetworkVariables(carNet, ['fuel']) ## this returns back a list
marginalizeNetworkVariables(carNet, ['battery', 'fuel'])

# inference
print("inference starts")
print(inference(carNet, ['battery', 'fuel'], [], []) )        ## chapter 8 equation (8.30)
print(inference(carNet, ['battery'], ['fuel'], [0]))           ## chapter 8 equation (8.31)
print(inference(carNet, ['battery'], ['gauge'], [0]))          ##chapter 8 equation  (8.32)
print(inference(carNet, [], ['gauge', 'battery'], [0, 0]))    ## chapter 8 equation (8.33)
print("inference ends")
###########################################################################
#RiskFactor Data Tests
###########################################################################
riskFactorNet = pd.read_csv('RiskFactorsData.csv')

# Create factors

income      = readFactorTablefromData(riskFactorNet, ['income'])
smoke       = readFactorTablefromData(riskFactorNet, ['smoke', 'income'])
exercise    = readFactorTablefromData(riskFactorNet, ['exercise', 'income'])
bmi         = readFactorTablefromData(riskFactorNet, ['bmi', 'income'])
diabetes    = readFactorTablefromData(riskFactorNet, ['diabetes', 'bmi'])
## you need to create more factor tables

risk_net = [income, smoke, exercise, bmi, diabetes]
print("income dataframe is ")
print(income)
factors = riskFactorNet.columns

# example test p(diabetes|smoke=1,exercise=2)

margVars = list(set(factors) - {'diabetes', 'smoke', 'exercise'})
obsVars  = ['smoke', 'exercise']
obsVals  = [1, 2]

p = inference(risk_net, margVars, obsVars, obsVals)
print(p)


### Please write your own test scrip similar to  the previous example 
###########################################################################
#HW4 test scrripts start from here
###########################################################################



def problem_one(BayesNet):
    res = 0
    for factor in BayesNet.BayesNet:
        res += factor.shape[0]

    print('The size of RiskFactorNet is :',res)

def problem_two(BayesNet):

    outcome_list = ['diabetes', 'stroke' , 'attack' , 'angina']


    obsVar_  = ['smoke', 'exercise']
    obsVal_  = [[1, 2], [2, 1]]
    str_ = ['bad habits', 'good habits']
    # for i in range(len(obsVal_)):
    #     print(str_[i], obsVar_, 'is', obsVal_[i])
    #     for j in range(len(healthVals)):

    #         margVars = list(set(factors) - set(healthVals[j] + obsVar_))
    #         p = inference(risk_net, margVar_, obsVar_, obsVal_[i])

    

    for outcome in outcome_list:
        print('The probability of ' , outcome , ' if I smoke and do not exercise is:')
        print(BayesNet.get_prob(outcome, ['smoke','exercise'], [1,2]))


    for outcome in outcome_list:
        print('The probability of ' , outcome , ' if I do not smoke and do exercise is:')
        print(BayesNet.get_prob(outcome, ['smoke','exercise'], [2,1]))
    


    for outcome in outcome_list:
        print('The probability of ' , outcome , ' if I have high blood pressure, high cholesterol, and overweight is:')
        print(BayesNet.get_prob(outcome, ['bp','cholesterol','bmi'], [1,1,3]))
   

    for outcome in outcome_list:
        print('The probability of ' , outcome , ' if I have low blood pressure, low cholesterol, and normal weight is:')
        print(BayesNet.get_prob(outcome,['bp','cholesterol','bmi'],[3,2,2]))

def problem_three(BayesNet):

    outcome_list = ['diabetes', 'stroke' , 'attack' , 'angina']
    probability_dic = {}

    for outcome in ['diabetes', 'stroke' , 'attack' , 'angina']:
        probability_dic[outcome] = []

        for i in range(1,9):

            factor = BayesNet.get_prob(outcome,['income'],[i])
            print(factor)
            probability_dic[outcome].append(factor.loc[0,'probs'])
    
    import matplotlib.pyplot as plt
    x = []
    for i in range(1, 9):
        x.append(i)

    
    for i in range(4):
        plt.plot(x, probability_dic[outcome_list[i]], label = outcome_list[i])

    plt.legend()
    plt.xlabel('income')
    plt.ylabel('probability')
    plt.title('probability-income figure')
    plt.grid()
    plt.show()


def problem_four(BayesNet):

    diabetes_new   = readFactorTablefromData(riskFactorNet, ['diabetes', 'bmi', 'smoke', 'exercise'])
    angina2_new     = readFactorTablefromData(riskFactorNet, ['angina', 'bmi', 'bp', 'cholesterol', 'smoke', 'exercise'])
    stroke2_new     = readFactorTablefromData(riskFactorNet, ['stroke', 'bmi', 'bp', 'cholesterol', 'smoke', 'exercise'])
    attack2_new     = readFactorTablefromData(riskFactorNet, ['attack', 'bmi', 'bp', 'cholesterol', 'smoke', 'exercise'])

    edge = {'diabetes':['smoke','exercise'], 'stroke':['smoke','exercise'] , \
        'attack':['smoke','exercise'] , 'angina':['smoke','exercise']}
    new_BayesNet = BayesNet.edge(edge)
    new_BayesNet.initialize()
    problem_two(new_BayesNet)
    return new_BayesNet

def problem_five(BayesNet):
    origin_BN = BayesNet

    stroke_new     = readFactorTablefromData(riskFactorNet, ['stroke', 'bmi', 'bp', 'cholesterol', 'smoke', 'exercise', 'diabetes'])

    print('The factor table for P(stroke | diabetes = 1) is as below : ')
    print(origin_BN.get_prob('stroke', ['diabetes'], [1]))
    factor = origin_BN.get_prob('stroke', ['diabetes'], [1])
    print('P(stroke = 1 | diabetes = 1) = ','%.3f'%factor.loc[0,'probs'])

    print('The factor table for P(stroke | diabetes = 3) is as below : ')
    print(origin_BN.get_prob('stroke',['diabetes'], [3]))
    factor = origin_BN.get_prob('stroke',['diabetes'], [3])
    print('P(stroke = 1 | diabetes = 3) = ','%.3f'%factor.loc[0,'probs'])

    edge = {'stroke':['diabetes']}
    new_BayesNet = BayesNet.edge(edge)
    new_BayesNet.initialize()
    print('After adding the edge to the BayesNetWork in problem four , we can get the probability as below : ')

    print('The factor table for P(stroke | diabetes = 1) is as below : ')
    print(new_BayesNet.get_prob('stroke',['diabetes'], [1]))
    factor = new_BayesNet.get_prob('stroke',['diabetes'], [1])
    print('P(stroke = 1 | diabetes = 1) = ','%.3f'%factor.loc[0,'probs'])

    print('The factor table for P(stroke| diabetes = 3) is as below : ')
    print(new_BayesNet.get_prob('stroke',['diabetes'], [3]))
    factor = new_BayesNet.get_prob('stroke',['diabetes'], [3])
    print('P(stroke = 1 | diabetes = 3) = ','%.3f'%factor.loc[0,'probs'])

    # for i in range(len(obsVals)):
    # margVars = list(set(factors) - set(['stroke'] + obsVars))
    # p = inference(risk_net3, margVars, obsVars, obsVals[i])

def wholeProblem():

    net = RiskNet()
    net.initialize()

    print('problem one')
    problem_one(net)
    print('problem two')
    problem_two(net)
    print('problem three')
    problem_three(net)

    print('problem four')
    new_net = problem_four(net)
    new_net.initialize()

    print('problem five')
    problem_five(new_net)

if __name__ == "__main__":
    wholeProblem()



