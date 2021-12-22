### Pichu-Pikachu
## Artificial Intelligence Game

## 1.1 Problem Formulation:
I formulate the problem of finding the best move given a Pichu board as a search problem in a depth first tree, where the goal is to find the move which maximizes a fitness score, within the allocated time. This is achieved by looking recursively K moves ahead (K is a variable set at the discretion of the user) and returns the board corresponding to the best move found so far, so that the later boards are always better than previous ones.

## 1.2 Program Description:
The game is represented using Pikachu class, which implements 2 main methods:
*  ###  Fitness: 
      Fitness returns a score ranging from +infinity if the current player wins to -infinity if the current player loses. Otherwise, the score is of board is the                       difference between the number of pieces of the current player and his opponent. Pikachu pieces count as 3 pichu pieces.
     
*  ###  Successors:
   Successors represents the bulk of the code, is a method that yields every single valid board configuration, which is one move away from the current board                         configuration.
              
A parse-board function is used to parse a string into a nested list that is a better representation of the board as it can be accessed more intuitively using indices. A maximum-score-ahead function returns the best score k moves ahead from the current board. This is a helper function used by find-best-move which initializes a Pikachu object using the input board, and loops through every single board one move away, we than compute the fitness of this board k moves ahead and update the best current board if said fitness is higher than the former one.

## 1.3 Issues faced during development:
One major issue consisted of making the changes to a successor board not affect its parent. This is due to how Python handles mutable object such as list of lists. This is circumvented using the deepcopy function, which makes sure to create a new memory slot for the new list instead of simply pointing to the original list.

