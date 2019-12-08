import numpy as np
import pandas as pd
import random


class Agent:
    ### START CODE HERE ###

    def __init__(self, actions):
        self.actions = actions
        self.epsilon = 1

    def choose_action(self, observation):
        action = np.random.choice(self.actions)
        return action



class cmAgent1:
    def __init__(self, actions, epsilon = 0.2, N = 50, gamma = 0.9, alpha = 0.2):
        self.epsilon = epsilon
        self.N = N
        self.gamma = gamma
        self.alpha = alpha
        self.action_dic = {}
        self.model_lis = [[], [], [], []]
        self.q_dic = {}
        #self.available_action = []
        self.actions = actions
        self.state = []
        self.trans = {}
        self.steps = 0
        self.counter = {}
        self.k = 1
        #self.dyn_reward = {}

    
    '''''
    def get_available_action(self, s):
        self.available_action = [0, 1, 2, 3]

        if s[0] >= (40 + 5) and s[0] <= (40 * 4 + 5) \
            and s[1] >= (40 + 5) and s[1] <= (40 * 4 + 5):
            self.available_action = [0, 1, 2, 3] # in the square
        elif s[0] == 5 and s[1] >= 45 and s[1] <= 40 * 4 + 5:
            self.available_action.remove(0) # up the square
        elif s[0] == 40 * 5 + 5 and s[1] >= 45 and s[1] <= 40 * 4 + 5:
            self.available_action.remove(1) # below the square
        elif s[1] == 5 and s[0] >= 45 and s[0] <= 40 * 4 + 5:
            self.available_action.remove(3) # left of the square
        elif s[1] == 40 * 5 + 5 and s[0] >= 45 and s[0] <= 40 * 4 + 5:
            self.available_action.remove(2) # right of the square
        elif s[0] == 5 and s[1] == 5: # left upper corner
            self.available_action.remove(0)
            self.available_action.remove(3)
        elif s[0] == 40 * 5 + 5 and s[1] == 5: # left lower corner
            self.available_action.remove(1)
            self.available_action.remove(3)
        elif s[0] == 5 and s[1] == 40 * 5 + 5: # right upper corner
            self.available_action.remove(0)
            self.available_action.remove(2)
        elif s[0] == 40 * 5 + 5 and s[1] == 40 * 5 + 5: # right lower corner
            self.available_action.remove(1)
            self.available_action.remove(2)

        return self.available_action

   
    def initial_q_dic(self):
        for x in range(5, 5 + 40 * 6, 6):
            for y in range(5, 5 + 40 * 6, 6):
                for act in self.get_available_action((x, y)):
                    self.q_dic[((x, y), act)] = 0
    '''''

    def max_q(self, state):

        val = []
        ## traverse actions
        for action in self.actions:
            q = (tuple(state), action)
            val.append(self.q_dic[q])
        ## find max one
        maxValue = max(val)

        ## get list of action
        actions = [action for action, value in enumerate(val) \
            if maxValue == value]

        return actions

    def epsilon_greedy(self, state):
        ## initialize q_dict
        self.steps += 1
        for action in self.actions:
            q_key = (tuple(state), action)
            if q_key not in self.q_dic:
                self.q_dic[q_key] = 0
        
        if self.steps % 1600 == 0:
            self.epsilon /= 2
        
        ## epsilon greedy
        ran = random.random()
        if ran < self.epsilon:
            action = np.random.choice(self.actions)
        else:
            # get the action corresponding to max q
            max_action = self.max_q(state)

            action = np.random.choice(max_action)

        return action


    def update_q(self, act, state, state_, reward):

        ## find max_q (consider that s_ is not in q_dic)
        max_q = -float('inf')
        for action in self.actions:
            q_key_ = (tuple(state_), action)
            if q_key_ not in self.q_dic:
                self.q_dic[q_key_] = 0
            if max_q < self.q_dic[q_key_]:
                max_q = self.q_dic[q_key_]

        q_key = (tuple(state), act)

        sample = reward + self.gamma * max_q

        self.q_dic[q_key] = (1 - self.alpha) * self.q_dic[q_key] + self.alpha * sample


        '''''

        ## update model_lis
        #self.model_lis.append((state_, self.epsilon_greedy(state)))
        self.model_lis[0].append(state) ## state
        self.model_lis[1].append(self.epsilon_greedy(state_)) ## action
        self.model_lis[2].append(state_)
        self.model_lis[3].append(reward)

        #self.model_lis[(state_, self.epsilon_greedy(state))]

        #self.q[:, s[0], s[1]] = (1 - self.alpha) * self.q[:, s[0], s[1]] + self.alpha * sample
        for item in self.q_dic.keys():
            self.q_dic[item] = (1 - self.alpha) * self.q_dic[item] + self.alpha * sample

        #return self.q_dic ## return a dic
        '''''

    def dynamic(self):
        for i in range(self.N):
            
            length1 = len(self.state)
            state = self.state[np.random.randint(length1)]
            tuple_state = tuple(state)
            length2 = len(self.action_dic[tuple_state])
            action = self.action_dic[tuple_state][np.random.randint(length2)]

            state_action = (tuple_state, action)

            state_, reward = self.trans[state_action]

            self.update_q(action, state, state_, reward)

            #return state, action, state_, reward

    def update_trans(self, sta, action, state_, reward):
        if sta not in self.state:
            self.state.append(sta)

        tuple_state = tuple(sta)

        if tuple_state not in self.action_dic:
            self.action_dic[tuple_state] = [action]
        else:
            if action not in self.action_dic[tuple_state]:
                self.action_dic[tuple_state].append(action)

        state_action = (tuple_state, action)

        if state_action not in self.trans:
            self.trans[state_action] = (state_, reward)
        else:
            self.trans[state_action] = (state_, reward)


    def counter_based(self, act, state, state_, reward, k):

        max_f = -float('inf')

        for action in self.actions:
            q_key_ = (tuple(state_), action)
           
            if q_key_ not in self.q_dic:
                self.q_dic[q_key_] = 0

            if q_key_ not in self.counter:
                self.counter[q_key_] = 1

            if max_f < self.q_dic[q_key_] + k / self.counter[q_key_]:
                max_f = self.q_dic[q_key_] + k / self.counter[q_key_]
            #_, max_f = self.max_f(state)

        q_key = (tuple(state_), act)
        sample = reward + self.gamma * self.q_dic[q_key_]

        self.q_dic[q_key] = (1 - self.alpha) * self.q_dic[q_key] + self.alpha * sample



    def max_f(self, state):

        val = []
        for action in self.actions:
            q = (tuple(state), action)

            if q not in self.q_dic:
                self.q_dic[q] = 0

            if q not in self.counter:
                self.counter[q] = 1
            # else:
            #     self.counter[q] += 1

            val.append(self.q_dic[q] + self.k / self.counter[q])
        maxValue = max(val)
        actions = [action for action, value in enumerate(val) if maxValue == value]

        return actions



    def new_choose_action(self, state):
        self.steps += 1
        for action in self.actions:
            q_key = (tuple(state), action)
            if q_key not in self.q_dic:
                self.q_dic[q_key] = 0


        max_action = self.max_f(state)

        actions = np.random.choice(max_action)

        self.counter[(tuple(state),self.actions[0])] += 1
        self.counter[(tuple(state),self.actions[1])] += 1
        self.counter[(tuple(state),self.actions[2])] += 1
        self.counter[(tuple(state),self.actions[3])] += 1


        return actions








class cmAgent2:
    def __init__(self, actions, epsilon = 0.2, N = 50, gamma = 0.9, alpha = 0.2):
        self.epsilon = epsilon
        self.N = N
        self.gamma = gamma
        self.alpha = alpha
        self.action_dic = {}
        self.model_lis = [[], [], [], []]
        self.q_dic = {}
        #self.available_action = []
        self.actions = actions
        self.state = []
        self.trans = {}
        self.steps = 0
        self.counter = {}
        self.k = 1
        #self.dyn_reward = {}

    

    def max_q(self, state):

        val = []
        for action in self.actions:
            q = (tuple(state), action)
            val.append(self.q_dic[q])
        maxValue = max(val)
        actions = [action for action, value in enumerate(val) if maxValue == value]

        return actions

    def epsilon_greedy(self, state):
        ## initialize q_dict
        self.steps += 1
        for action in self.actions:
            q_key = (tuple(state), action)
            if q_key not in self.q_dic:
                self.q_dic[q_key] = 0
        
        if self.steps % 800 == 0:
            self.epsilon /= 2
        
        ## epsilon greedy
        ran = random.random()
        if ran < self.epsilon:
            action = np.random.choice(self.actions)
        else:
            # get the action corresponding to max q
            max_action = self.max_q(state)

            action = np.random.choice(max_action)

        return action


    def update_q(self, act, state, state_, reward):

        ## find max_q (consider that s_ is not in q_dic)
        max_q = -float('inf')
        for action in self.actions:
            q_key_ = (tuple(state_), action)
            if q_key_ not in self.q_dic:
                self.q_dic[q_key_] = 0
            if max_q < self.q_dic[q_key_]:
                max_q = self.q_dic[q_key_]

        q_key = (tuple(state), act)

        sample = reward + self.gamma * max_q

        self.q_dic[q_key] = (1 - self.alpha) * self.q_dic[q_key] + self.alpha * sample


        

    def dynamic(self):
        for i in range(self.N):
           
            length1 = len(self.state)
            state = self.state[np.random.randint(length1)]
            tuple_state = tuple(state)
            length2 = len(self.action_dic[tuple_state])
            action = self.action_dic[tuple_state][np.random.randint(length2)]

            state_action = (tuple_state, action)

            state_, reward = self.trans[state_action]

            self.update_q(action, state, state_, reward)

            #return state, action, state_, reward

    def update_trans(self, sta, action, state_, reward):
        if sta not in self.state:
            self.state.append(sta)

        tuple_state = tuple(sta)

        if tuple_state not in self.action_dic:
            self.action_dic[tuple_state] = [action]
        else:
            if action not in self.action_dic[tuple_state]:
                self.action_dic[tuple_state].append(action)

        state_action = (tuple_state, action)

        if state_action not in self.trans:
            self.trans[state_action] = (state_, reward)
        else:
            self.trans[state_action] = (state_, reward)


    def counter_based(self, act, state, state_, reward, k):

        max_f = -float('inf')

        for action in self.actions:
            q_key_ = (tuple(state_), action)
           
            if q_key_ not in self.q_dic:
                self.q_dic[q_key_] = 0

            if q_key_ not in self.counter:
                self.counter[q_key_] = 1

            if max_f < self.q_dic[q_key_] + k / self.counter[q_key_]:
                max_f = self.q_dic[q_key_] + k / self.counter[q_key_]
            #_, max_f = self.max_f(state)

        q_key = (tuple(state_), act)
        sample = reward + self.gamma * self.q_dic[q_key_]

        self.q_dic[q_key] = (1 - self.alpha) * self.q_dic[q_key] + self.alpha * sample



    def max_f(self, state):

        val = []
        for action in self.actions:
            q = (tuple(state), action)

            if q not in self.q_dic:
                self.q_dic[q] = 0

            if q not in self.counter:
                self.counter[q] = 1
            # else:
            #     self.counter[q] += 1

            val.append(self.q_dic[q] + self.k / self.counter[q])
        maxValue = max(val)
        actions = [action for action, value in enumerate(val) if maxValue == value]

        return actions



    def new_choose_action(self, state):
        self.steps += 1
        
        for action in self.actions:
            q_key = (tuple(state), action)
            if q_key not in self.q_dic:
                self.q_dic[q_key] = 0

        if random.random()<0.95:
            max_action = self.max_f(state)

            actions = np.random.choice(max_action)
        else:
            max_action = self.max_f(state)
            actions = np.random.choice(self.actions)

        self.counter[(tuple(state),self.actions[0])] += 1
        self.counter[(tuple(state),self.actions[1])] += 1
        self.counter[(tuple(state),self.actions[2])] += 1
        self.counter[(tuple(state),self.actions[3])] += 1


        return actions


        


    




    
    

        





    




        

        

        

        

        






    ### END CODE HERE ###