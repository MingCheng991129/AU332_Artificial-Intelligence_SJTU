import numpy as np
import pandas as pd
from functools import reduce

## Function to create a conditional probability table
## Conditional probability is of the form p(x1 | x2, ..., xk)
## varnames: vector of variable names (strings) first variable listed 
##           will be x_i, remainder will be parents of x_i, p1, ..., pk
## probs: vector of probabilities for the flattened probability table
## outcomesList: a list containing a vector of outcomes for each variable
## factorTable is in the type of pandas dataframe
## See the test file for examples of how this function works
def readFactorTable(varnames, probs, outcomesList):
    factorTable = pd.DataFrame({'probs': probs})

    totalfactorTableLength = len(probs)
    numVars = len(varnames)

    k = 1
    for i in range(numVars - 1, -1, -1):
        levs = outcomesList[i]
        numLevs = len(levs)
        col = []
        for j in range(0, numLevs):
            col = col + [levs[j]] * k
        factorTable[varnames[i]] = col * int(totalfactorTableLength / (k * numLevs))
        k = k * numLevs

    return factorTable

## Build a factorTable from a data frame using frequencies
## from a data frame of data to generate the probabilities.
## data: data frame read using pandas read_csv
## varnames: specify what variables you want to read from the table
## factorTable is in the type of pandas dataframe
def readFactorTablefromData(data, varnames):
    numVars = len(varnames)
    outcomesList = []

    for i in range(0, numVars):
        name = varnames[i]
        outcomesList = outcomesList + [list(set(data[name]))]

    lengths = list(map(lambda x: len(x), outcomesList))
    m = reduce(lambda x, y: x * y, lengths)
   
    factorTable = pd.DataFrame({'probs': np.zeros(m)})

    k = 1
    for i in range(numVars - 1, -1, -1):
        levs = outcomesList[i]
        numLevs = len(levs)
        col = []
        for j in range(0, numLevs):
            col = col + [levs[j]] * k
        factorTable[varnames[i]] = col * int(m / (k * numLevs))
        k = k * numLevs

    numLevels = len(outcomesList[0])

    # creates the vector called fact to index probabilities 
    # using matrix multiplication with the data frame
    fact = np.zeros(data.shape[1])
    lastfact = 1
    for i in range(len(varnames) - 1, -1, -1):
        fact = np.where(np.isin(list(data), varnames[i]), lastfact, fact)
        lastfact = lastfact * len(outcomesList[i])

    # Compute unnormalized counts of subjects that satisfy all conditions
    a = (data - 1).dot(fact) + 1
    for i in range(0, m):
        factorTable.at[i,'probs'] = sum(a == (i+1))

    # normalize the conditional probabilities
    skip = int(m / numLevels)
    for i in range(0, skip):
        normalizeZ = 0
        for j in range(i, m, skip):
            normalizeZ = normalizeZ + factorTable['probs'][j]
        for j in range(i, m, skip):
            if normalizeZ != 0:
                factorTable.at[j,'probs'] = factorTable['probs'][j] / normalizeZ

    return factorTable


## Join of two factors
## factor1, factor2: two factor tables
##
## Should return a factor table that is the join of factor 1 and 2.
## You can assume that the join of two factors is a valid operation.
## Hint: You can look up pd.merge for mergin two factors
def joinFactors(factor1, factor2):
    # your code

    #     factor1['tmp'] = 0
    #     factor2['tmp'] = 0

    factor1_ = pd.DataFrame.copy(factor1)
    factor2_ = pd.DataFrame.copy(factor2)
   
    #      new_factor = pd.merge(factor1, factor2, on='tmp')

    #      eql = np.intersect1d(factor1,factor2).tolist()
    #      if eql == True:
    #           new_factor = pd.merge(factor1,factor2,on=eql)
    equal_col = []
    for col in factor1_.columns:
        if col in factor2_.columns:
            equal_col.append(col)

    equal_col.remove('probs')
    # del new_factor['probs_x']
    # del new_factor['probs_y']

    if (len(equal_col) == 0) == False:

        new_factor = pd.merge(factor1_, factor2_, how = 'outer', on = equal_col)
        
        new_factor['probs_x'] *= new_factor['probs_y']

        new_factor = new_factor.drop(['probs_y'], axis = 1)
        # del new_factor['probs_y']
        
        new_factor = new_factor.rename(columns = {'probs_x':'probs'})
    else:
        factor1_['augxiliary'] = 0
        factor2_['augxiliary'] = 0

        #     factor1['tmp'] = 0
        #     factor2['tmp'] = 0

        new_factor = pd.merge(factor1_, factor2_, how='outer', on=['augxiliary'])

        new_factor['probs_x'] *= new_factor['probs_y']

        new_factor = new_factor.drop(['probs_y','augxiliary'], axis=1)
        new_factor = new_factor.rename(columns = {'probs_x':'probs'}) 
    #   del new_factor['probs_x']
    #   del new_factor['probs_y']
    
    return new_factor

## Marginalize a variable from a factor
## table: a factor table in dataframe
## hiddenVar: a string of the hidden variable name to be marginalized
##
## Should return a factor table that marginalizes margVar out of it.
## Assume that hiddenVar is on the left side of the conditional.
## Hint: you can look can pd.groupby
def marginalizeFactor(factorTable, hiddenVar):
    # your code 

    # new_table = pd.DataFrame(columns = factorTable.columns)

    factor = pd.DataFrame.copy(factorTable) 
    # col = list(factor.columns)
    col = factor.columns.tolist()

    col.remove('probs')
    col.remove(hiddenVar)

    new_factor = factor.drop(hiddenVar, axis=1)

    # for name, group in factorTable.groupby(np.setdiff1d(vars, [hiddenVar]).tolist()):
    #     # sum probs
    #     group_sum = group.head(1)
    #     group_sum['probs'] = group['probs'].sum()

    #     new_table = pd.concat([new_table, group_sum], ignore_index=True)


    new_factor = new_factor[new_factor.columns].groupby(col, as_index=False).sum()
    probs = new_factor['probs']

    new_factor = new_factor.drop('probs', axis=1)
    # del new_table[hiddenVar]

    new_factor.insert(0, 'probs', probs, True)

    return new_factor

## Marginalize a list of variables 
## bayesnet: a list of factor tables and each table iin dataframe type
## hiddenVar: a string of the variable name to be marginalized
##
## Should return a Bayesian network containing a list of factor tables that results
## when the list of variables in hiddenVar is marginalized out of bayesnet.
def marginalizeNetworkVariables(bayesNet, hiddenVar):
    # your code 
    new_BN = bayesNet.copy()
    col = []
    for factor in new_BN:
        # col.extend(list(factor.columns))
        col.extend(factor.columns.tolist())

    col = set(col)
    for i in hiddenVar:
        if i in col:
            new_new_BN = new_BN.copy()
            new_factor = pd.DataFrame(columns=['probs'])
            
            # for factor in new_BN:
            for factor in new_new_BN:
                if i in factor.columns:

                    for j in range(len(new_BN)):

                        if list(new_BN[j].columns) == list(factor.columns):
                        # if (new_BN[j].columns.tolist() == factor.columns) == True:

                            del new_BN[j]
                            ## del new_BN[j].columns
                            break

                    if new_factor.empty == False:
                        new_factor = joinFactors(new_factor,factor)
                        # new_factor = marginalizeFactor(new_factor, var)

                    else:
                        new_factor = factor

            new_factor = marginalizeFactor(new_factor, i)
            new_BN.append(new_factor)
    
    return new_BN

## Update BayesNet for a set of evidence variables
## bayesNet: a list of factor and factor tables in dataframe format
## evidenceVars: a vector of variable names in the evidence list
## evidenceVals: a vector of values for corresponding variables (in the same order)
##
## Set the values of the evidence variables. Other values for the variables
## should be removed from the tables. You do not need to normalize the factors
def evidenceUpdateNet(bayesNet, evidenceVars, evidenceVals):
    # your code 
    new_net = []

    for factor_table in bayesNet:
        new_net.append(factor_table.copy())


    new_NB = bayesNet.copy()
    len_var = len(evidenceVars)

    for i in range(len_var):
        new_new_NB = new_NB.copy()

        for factor in new_new_NB:

            if evidenceVars[i] in factor.columns:

                #     var = evidenceVars[i]
                #     val = evidenceVals[i]
        
                #     df.drop(df[df[var] != val].index, inplace=True)

                for j in range(len(new_NB)):
                    if list(new_NB[j].columns) == list(factor.columns):
                    # if (new_NB[j].columns.tolist() == factor.columns) == True:
                        del new_NB[j]
                        break

                new_factor = factor[factor[evidenceVars[i]] == evidenceVals[i]]
                new_NB.append(new_factor)

    return new_NB


## Run inference on a Bayesian network
## bayesNet: a list of factor tables and each table iin dataframe type
## hiddenVar: a string of the variable name to be marginalized
## evidenceVars: a vector of variable names in the evidence list
## evidenceVals: a vector of values for corresponding variables (in the same order)
##
## This function should run variable elimination algorithm by using 
## join and marginalization of the sets of variables. 
## The order of the elimiation can follow hiddenVar ordering
## It should return a single joint probability table. The
## variables that are hidden should not appear in the table. The variables
## that are evidence variable should appear in the table, but only with the single
## evidence value. The variables that are not marginalized or evidence should
## appear in the table with all of their possible values. The probabilities
## should be normalized to sum to one.
def inference(bayesNet, hiddenVar, evidenceVars, evidenceVals):
    # your code 

    new_NB = bayesNet.copy()
    new_NB = evidenceUpdateNet(new_NB,evidenceVars,evidenceVals)
    new_NB = marginalizeNetworkVariables(new_NB,hiddenVar)

    ## debug
    
    while (len(new_NB) == 1) == False:
        factor1 , factor2 = np.random.choice(new_NB,2)

        # if len(new_NB) > 1:
        if len(set(factor1.columns).intersection(set(factor2.columns))) > 1 \
            and (list(factor1.columns) == list(factor2.columns)) == False:

            for j in range(len(new_NB)):
                if (list(new_NB[j].columns) == list(factor1.columns)) == True:
                    del new_NB[j]
                    break

            for j in range(len(new_NB)):
                if (list(new_NB[j].columns) == list(factor2.columns)) == True:
                    del new_NB[j]
                    break

            new_factor = joinFactors(factor1,factor2)
            new_NB.append(new_factor)

    res = new_NB[0]

    res['probs'] /= sum(res['probs'].tolist()) ## normalize
    
    return res


initial_con = {'income':[],'bmi':['income','exercise'],'exercise':['income'],\
            'smoke':['income'],'bp':['income','exercise','smoke'],\
                'cholesterol':['income','exercise','smoke'],\
            'diabetes':['bmi'],'stroke':['bmi','bp','cholesterol'],\
                'attack':['bmi','bp','cholesterol'],\
                    'angina':['bmi','bp','cholesterol']}

class RiskNet(object):
    def __init__(self, con = initial_con):
        self.BayesNet = []
        self.riskFactorData = pd.read_csv('RiskFactorsData.csv')
        self.con = con
        # self.connection = {}
        # self.node = node 
        # self.edge = edge
        # self.netBN = []

    def initialize(self):
        for i in self.con.keys():
            node = self.con[i].copy()
            node.insert(0,i)

            factor = readFactorTablefromData(self.riskFactorData,node)
            self.BayesNet.append(factor)
    
    def edge(self,edge):
            new_con = self.con.copy()
            for key in edge.keys():
                new_con[key].extend(edge[key])
            new_net = RiskNet(new_con)

            return new_net

    def netSize(self, bayesNet):
        size_list = []
        prod = 1
        for factorTable in bayesNet:
            prod *= factorTable.shape[0]
            size_list.append(factorTable.shape[0])

    def get_prob(self,q, evidenceVars, evidenceVals):

        Vars = []
        for i in self.con.keys():
            Vars.append(i)

        hiddenVar = Vars

        for var in evidenceVars:
            hiddenVar.remove(var)

        if q in hiddenVar:
            hiddenVar.remove(q)

        return inference(self.BayesNet,hiddenVar,evidenceVars,evidenceVals)

        
    def VarProcess(self, factorTable):
        return np.setdiff1d(factorTable.columns.values,['probs']).tolist()


