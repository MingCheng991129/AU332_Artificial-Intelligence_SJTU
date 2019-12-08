This folder contains the first part of homework 3: the maze game. 

In this part, I use the dyna-Q learning algorithm to enable the red block to find the optimal path in the maze board. 
- If the diamond is foound, the red block will get the reward of +2.
- If the red block finds the terminal, it will get the reward of +1.
- If the red block falls into the traps(black block), it will get the reward of -1.

The evaluation function I used is *f = u + k/n*.

*maze_env1.py* and *maze_env2.py* define the maze environment.

*agent.py* is my agent.

