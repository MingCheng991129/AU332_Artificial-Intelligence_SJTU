import random, re, datetime
import sys
import sys
import math
from queue import PriorityQueue
import copy
import board as Board
class Agent(object):
    def __init__(self, game):
        self.game = game

    def getAction(self, state):
        raise Exception("Not implemented yet")


class RandomAgent(Agent):
    def getAction(self, state):
        legal_actions = self.game.actions(state)
        self.action = random.choice(legal_actions)


class SimpleGreedyAgent(Agent):
    # a one-step-lookahead greedy agent that returns action with max vertical advance
    def getAction(self, state):
        legal_actions = self.game.actions(state)

        self.action = random.choice(legal_actions)

        player = self.game.player(state)
        if player == 1:
            max_vertical_advance_one_step = max([action[0][0] - action[1][0] for action in legal_actions])
            max_actions = [action for action in legal_actions if
                           action[0][0] - action[1][0] == max_vertical_advance_one_step]
        else:
            max_vertical_advance_one_step = max([action[1][0] - action[0][0] for action in legal_actions])
            max_actions = [action for action in legal_actions if
                           action[1][0] - action[0][0] == max_vertical_advance_one_step]
        self.action = random.choice(max_actions)


class CMWCHMinimaxAgent(Agent):

    def getFirstLastElement(self, agentPos, player):
        if player == 1:
            first = agentPos[0][0]
            last = agentPos[0][0]
            for position in agentPos:
                if position[0] < first:
                    first = position[0]
                if position[0] > last:
                    last = position[0]
        else:
            first = agentPos[0][0]
            last = agentPos[0][0]
            for position in agentPos:
                if position[0] > first:
                    first = position[0]
                if position[0] < last:
                    last = position[0]

        return first, last

    def duringGame(self, MyFirst, HerFirst, player):
        if player == 2:
            return (MyFirst - HerFirst >= 2)
        else:
            return (HerFirst - MyFirst >= 2)

    def isEnd(self, MyLast, HerLast, player, k=0):
        if player == 1:
            return (MyLast + k <= HerLast)
        else:
            return (HerLast + k <= MyLast)

    def verDist(self, agentPos, player):
        dist = 0

        if player == 1:
            for position in agentPos:
                dist += 20 - position[0]
        else:
            for position in agentPos:
                dist += position[0]

        return dist

    def midDist(self, agentPos, board):
        dist = 0

        for position in agentPos:
            dist += abs(position[1] - board.getColNum(position[0]) / 2)

        return dist

    def ourLoss(self, agentPos):
        dist = 0
        avg = 0

        for position in agentPos:
            avg += position[0] / 10
        for position in agentPos:
            dist += abs(position[0] - avg)

        return dist

    def player_win(self, agentPos):
        terminal_state = [(1, 1), (2, 1), (2, 2), (3, 1), (3, 2), (3, 3), (4, 1), (4, 2), (4, 3), (4, 4)]
        for p in agentPos:
            if p not in terminal_state:
                return False
        return True

    def feaPurne(self, state1, state2):
        eval = 0
        board1 = state1[1]
        board2 = state2[1]
        pos1 = board1.getPlayerPiecePositions(state2[0])
        pos2 = board2.getPlayerPiecePositions(state2[0])

        for position1 in pos1:
            eval += position1[0]
        for position2 in pos2:
            eval -= position2[0]

        return eval * 40.65

    def simpleeval(self, state):
        player = state[0]
        board = state[1]
        agentPos = board.getPlayerPiecePositions(state[0])

        ourWin = 0
        for position in agentPos:
            if player == 1:
                ourWin += 20 - position[0]
            else:
                ourWin += position[0]

        return ourWin

    def feature_eval2(self, state):
        eval = 0
        player = state[0]
        board = state[1]
        agentPos = board.getPlayerPiecePositions(state[0])
        oppoPos = board.getPlayerPiecePositions(3 - state[0])

        ourWin = 0
        oppoWin = 0
        ourCenter = 0
        avg_row = 0
        ourLoss = 0
        rightsideness = 0

        for position in agentPos:
            ourWin += position[0]
            ourCenter += abs(position[1] - board.getColNum(position[0]) / 2)
            avg_row += position[0] / 10.0

        for position in oppoPos:
            oppoWin += 20 - position[0]

        for position in agentPos:
            ourLoss += abs(position[0] - avg_row)

        actions = self.game.actions(state)
        last = actions[0][0]
        f = {}
        stepping = 0

        for action in actions:
            if action[0] in f.keys():
                if (action[0][0] - action[1][0]) < f[action[0]]:
                    f[action[0]] = (action[0][0] - action[1][0])
            else:
                f[action[0]] = (action[0][0] - action[1][0])

        for i in f.keys():
            stepping += f[i]
        stepping = -stepping
    
       

        eval = 2.1 * (ourWin - oppoWin) + 0.34 * (-ourCenter) + 0.7 * stepping - 0.35 * ourLoss
        return eval

    def feature_eval1(self, state):
        eval = 0
        player = state[0]
        board = state[1]
        agentPos = board.getPlayerPiecePositions(state[0])
        oppoPos = board.getPlayerPiecePositions(3 - state[0])

        ourWin = 0
        oppoWin = 0
        ourCenter = 0
        avg = 0
        ourLoss = 0

        for position in agentPos:
            ourWin += 20 - position[0]
            ourCenter += abs(position[1] - board.getColNum(position[0]) / 2)
            avg += position[0] / 10.0

        for position in oppoPos:
            oppoWin += position[0]

        for position in agentPos:
            ourLoss += abs(position[0] - avg)

        actions = self.game.actions(state)
        last = actions[0][0]
        f = {}
        stepping = 0

        for action in actions:
            if action[0] in f.keys():
                if (action[0][0] - action[1][0]) > f[action[0]]:
                    f[action[0]] = action[0][0] - action[1][0]
            else:
                f[action[0]] = action[0][0] - action[1][0]

        for i in f.keys():
            stepping += f[i]

        eval = 2.1 * (ourWin - oppoWin) + 0.34 * (-ourCenter) + 0.7 * stepping - 0.35 * ourLoss
        return eval

    def takeDepth(self, action):
        return action[1][0] - action[0][0]

    def max_value(self, state, n, alpha, beta):

        if n == 0:
            if state[0] == 1:
                return self.feature_eval1(state)
            else:
                return self.feature_eval2(state)

        value = sys.maxsize * -1
        bestAct = None

        actions = self.game.actions(state)
        if state[0] == 1:
            actions.sort(key=self.takeDepth)
        else:
            actions.sort(key=self.takeDepth)
            actions = actions[::-1]
        for action in actions:
            if state[0] == 1:
                if action[0][0] - action[1][0] < -1:
                    continue
                if action[0][0] <= 4:
                    continue
            else:
                if action[0][0] - action[1][0] > 1:
                    continue
                if action[0][0] >= 16:
                    continue
            if state[0] == 1:
                if value > 0:
                    value = max(value, self.min_value(self.game.succ(state, action), n-1, alpha, beta) / (0.06 * (21 - action[0][0])))
                else:
                    value = max(value, self.min_value(self.game.succ(state, action), n-1, alpha, beta) * (0.06 * (21 - action[0][0])))
            else:
                if value < 0:
                    value = max(value, self.min_value(self.game.succ(state, action), n-1, alpha, beta) * ((0.06 * action[0][0])))
                else:
                    value = max(value, self.min_value(self.game.succ(state, action), n-1, alpha, beta) / ((0.06 * action[0][0])))
            if value >= beta:
                if n == 2:
                    return value, action
                else:
                    return value
            if value > alpha:
                alpha = value
                if n == 2:
                    self.action = action
                bestAct = action
        if n == 2:
            return value, bestAct
        else:
            return value


    def min_value(self, state, n, alpha, beta):

        value = sys.maxsize
        actions = self.game.actions(state)
        if state[0] == 2:
            actions.sort(key=self.takeDepth)
            actions = actions[::-1]
        else:
            actions.sort(key=self.takeDepth)
        for action in actions:
            if state[0] == 2:
                if action[0][0] - action[1][0] > 1:
                    continue
                if action[0][0] >= 16:
                    continue
            else:
                if action[0][0] - action[1][0] < -1:
                    continue
                if action[0][0] <= 4:
                    continue
            successor = self.game.succ(state, action)
            if state[0] == 2:
                if self.feaPurne(successor, state) <= 65:
                    continue

            value = min(value, self.max_value(successor, n-1, alpha, beta))

            if value <= alpha:
                return value
            beta = min(value, beta)
        return value

    def minimax(self, state, n, alpha = sys.maxsize * -1, beta = sys.maxsize):
        value, action = self.max_value(state, n, alpha, beta)
        return action

    def maximax_value(self, state, n):
        if n == 0:
            if state[0] == 1:
                return self.feature_eval1(state)
            else:
                return self.feature_eval2(state)

        value = sys.maxsize * -1
        bestAct = None

        actions = self.game.actions(state)
        if state[0] == 1:
            actions.sort(key=self.takeDepth)
        else:
            actions.sort(key=self.takeDepth)
            actions = actions[::-1]
        for action in actions:
            next_value = self.maximax_value((state[0], self.game.succ(state, action)[1]), n-1)
            if value < next_value:
                value = next_value
                bestAct = action

        if n == 1:
            return value, bestAct
        else:
            return value

    def maximax(self, state, n):
        value, action = self.maximax_value(state, n)
        return action

    def getAction(self, state):
        legal_actions = self.game.actions(state)
        self.action = random.choice(legal_actions)
        # print (self.action)

        player = self.game.player(state)
        n = 2
        ### START CODE HERE ###
        bestAct = None
        agentPos = state[1].getPlayerPiecePositions(player)
        oppoPos = state[1].getPlayerPiecePositions(3 - player)
        myFirst, myLast = self.getFirstLastElement(agentPos, player)
        herFirst, herLast  =  self.getFirstLastElement(oppoPos, 3-player)

        if self.duringGame(myFirst, herFirst, player) and not self.isEnd(myLast, herLast, player):
            
            bestAct = self.minimax(state, n)
        elif self.isEnd(myLast, herLast, player):
            
            end_of_end = self.endProcess(state, player)
            if end_of_end == -1:
                if player == 1:
                    max_vertical_advance_one_step = max([action[0][0] - action[1][0] for action in legal_actions])
                    max_actions = [action for action in legal_actions if
                                   action[0][0] - action[1][0] == max_vertical_advance_one_step]
                else:
                    max_vertical_advance_one_step = max([action[1][0] - action[0][0] for action in legal_actions])
                    max_actions = [action for action in legal_actions if
                                   action[1][0] - action[0][0] == max_vertical_advance_one_step]
                self.action = random.choice(max_actions)
        else:
            
            bestAct = self.maximax(state, 1)

        if bestAct == None:
           
            pass
        else:
            self.action = bestAct
      

    def endProcess(self ,state, player):
        
        condPlay1 = [[(1, 1), (2, 1), (2, 2), (3, 1), (3, 2), (3, 3), (4, 1), (4, 2), (4, 3), (5, 1)],
                               [(1, 1), (2, 1), (2, 2), (3, 1), (3, 2), (3, 3), (4, 1), (4, 2), (4, 4), (5, 1)],
                               [(1, 1), (2, 1), (2, 2), (3, 1), (3, 2), (3, 3), (4, 1), (4, 3), (4, 4), (5, 1)],
                               [(1, 1), (2, 1), (2, 2), (3, 1), (3, 2), (3, 3), (4, 2), (4, 3), (4, 4), (5, 5)],
                               [(1, 1), (2, 1), (2, 2), (3, 1), (3, 2), (3, 3), (4, 1), (4, 3), (4, 4), (5, 5)],
                               [(1, 1), (2, 1), (2, 2), (3, 1), (3, 2), (3, 3), (4, 1), (4, 2), (4, 4), (5, 5)],
                               [(1, 1), (2, 1), (2, 2), (3, 1), (3, 2), (3, 3), (4, 1), (4, 2), (4, 3), (5, 2)],
                               [(1, 1), (2, 1), (2, 2), (3, 1), (3, 2), (3, 3), (4, 1), (4, 2), (4, 4), (5, 2)],
                               [(1, 1), (2, 1), (2, 2), (3, 1), (3, 2), (3, 3), (4, 2), (4, 3), (4, 4), (5, 4)],
                               [(1, 1), (2, 1), (2, 2), (3, 1), (3, 2), (3, 3), (4, 1), (4, 3), (4, 4), (5, 4)],
                               [(1, 1), (2, 1), (2, 2), (3, 1), (3, 2), (3, 3), (4, 2), (4, 3), (4, 4), (5, 3)],
                               [(1, 1), (2, 1), (2, 2), (3, 1), (3, 2), (3, 3), (4, 1), (4, 2), (4, 3), (5, 3)]]

        condPlay2 = [[(19, 1), (18, 1), (18, 2), (17, 1), (17, 2), (17, 3), (16, 1), (16, 2), (16, 3), (15, 1)], # 0
                               [(19, 1), (18, 1), (18, 2), (17, 1), (17, 2), (17, 3), (16, 1), (16, 3), (16, 4), (15, 1)], # 1
                               [(19, 1), (18, 1), (18, 2), (17, 1), (17, 2), (17, 3), (16, 1), (16, 2), (16, 4), (15, 1)], # 2
                               [(19, 1), (18, 1), (18, 2), (17, 1), (17, 2), (17, 3), (16, 2), (16, 3), (16, 4), (15, 5)], # 3
                               [(19, 1), (18, 1), (18, 2), (17, 1), (17, 2), (17, 3), (16, 1), (16, 3), (16, 4), (15, 5)], # 4
                               [(19, 1), (18, 1), (18, 2), (17, 1), (17, 2), (17, 3), (16, 1), (16, 2), (16, 4), (15, 5)], # 5
                               [(19, 1), (18, 1), (18, 2), (17, 1), (17, 2), (17, 3), (16, 1), (16, 2), (16, 3), (15, 2)], # 6
                               [(19, 1), (18, 1), (18, 2), (17, 1), (17, 2), (17, 3), (16, 1), (16, 2), (16, 4), (15, 2)], # 7
                               [(19, 1), (18, 1), (18, 2), (17, 1), (17, 2), (17, 3), (16, 2), (16, 3), (16, 4), (15, 4)], # 8
                               [(19, 1), (18, 1), (18, 2), (17, 1), (17, 2), (17, 3), (16, 1), (16, 3), (16, 4), (15, 4)], # 9
                               [(19, 1), (18, 1), (18, 2), (17, 1), (17, 2), (17, 3), (16, 2), (16, 3), (16, 4), (15, 3)], # 10
                               [(19, 1), (18, 1), (18, 2), (17, 1), (17, 2), (17, 3), (16, 1), (16, 2), (16, 3), (15, 3)]] # 11
        board = state[1]
        agentPos = board.getPlayerPiecePositions(player)
        idx = -1
        if player == 1:
            for i in range(len(condPlay1)):
                if condPlay1[i] == agentPos:
                    idx = i
                    break
            if idx == 0:
                self.action = ((4, 2), (4, 4))
            elif idx == 1:
                self.action = ((4, 1), (4, 3))
            elif idx == 2:
                self.action = ((4, 1), (4, 2))
            elif idx == 3:
                self.action = ((4, 3), (4, 1))
            elif idx == 4:
                self.action = ((4, 4), (4, 2))
            elif idx == 5:
                self.action = ((4, 4), (4, 3))
            elif idx == 6:
                self.action = ((4, 2), (4, 4))
            elif idx == 7:
                self.action = ((4, 2), (4, 3))
            elif idx == 8:
                self.action = ((4, 3), (4, 1))
            elif idx == 9:
                self.action = ((4, 3), (4, 2))
            elif idx == 10:
                self.action = ((4, 2), (4, 1))
            elif idx == 11:
                self.action = ((4, 3), (4, 4))
        else:
            for i in range(len(condPlay2)):
                if condPlay2[i] == agentPos:
                    idx = i
                    break
            if idx == 0:
                self.action = ((16, 2), (16, 4))
            elif idx == 1:
                self.action = ((16, 1), (16, 2))
            elif idx == 2:
                self.action = ((16, 1), (16, 3))
            elif idx == 3:
                self.action = ((16, 3), (16, 1))
            elif idx == 4:
                self.action = ((16, 4), (16, 2))
            elif idx == 5:
                self.action = ((16, 4), (16, 3))
            elif idx == 6:
                self.action = ((16, 2), (16, 4))
            elif idx == 7:
                self.action = ((16, 2), (16, 3))
            elif idx == 8:
                self.action = ((16, 3), (16, 1))
            elif idx == 9:
                self.action = ((16, 3), (16, 2))
            elif idx == 10:
                self.action = ((16, 2), (16, 1))
            elif idx == 11:
                self.action = ((16, 3), (16, 4))
        return idx

        ### END CODE HERE ###
