from agent import Agent
from agent import cmAgent1
from agent import cmAgent2
import time
import matplotlib.pyplot as plt

maze = '2'

if maze == '1':
    from maze_env1 import Maze
elif maze == '2':
    from maze_env2 import Maze


if __name__ == "__main__":
    if maze == '1':
        env = Maze() 

        agent = cmAgent1(list(range(env.n_actions)), epsilon=0.5, N=30, gamma=0.9, alpha=0.5)

        for episode in range(500):
            state = env.reset()
            state.append(False)

            episode_reward = 0

            while True:
                #env.render()
                #print(agent.q_dic, '\n')
                action = agent.epsilon_greedy(state)
                state_, reward, done = env.step(action)
                agent.update_q(action, state, state_, reward)
                agent.update_trans(state, action, state_, reward)

                episode_reward += reward

                state = state_

                agent.dynamic()

                if done:
                    #env.render()
                    break

            
            print('episode:', episode, 'episode_reward:', episode_reward)

        print('\ntraining over\n')


    elif maze == '2':
        env = Maze() 

        agent = cmAgent2(list(range(env.n_actions)), epsilon=0.5, N=20, gamma=0.9, alpha=0.5)

        for episode in range(500):
            state = env.reset()
            state.append(False)

            episode_reward = 0

            while True:
                #env.render()
                #print(agent.q_dic, '\n')
                action = agent.new_choose_action(state)
                
                state_, reward, done = env.step(action)
                agent.counter_based(action, state, state_, reward, k=30)
                agent.update_trans(state, action, state_, reward)

                episode_reward += reward

                state = state_

                agent.dynamic()

                if done:
                    #env.render()
                    break

            
            print('episode:', episode, 'episode_reward:', episode_reward)

        print('\ntraining over\n')
        