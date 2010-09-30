# Rolling Die Mazes

## Running
To run this program:

    python rblock.py <puzzle-file>

## Output

See output folder for examples of output.

## Problem Description

For this project, you will write an A* search in python for solving rolling-die mazes. The objective is to "roll" a die along its edges through a grid until a goal location is reached. The initial state of the search is given by the die location and orientation. For this project, the die will always start with the 1 facing up ('visible'), 2 facing up/north, and 3 to the right/east: note that the sum of two opposite faces on a die is always 7. Rolling dies mazes contain obstacles, as well as restrictions on which numbers may face 'up.'

For this project, the number 6 should never be face up on the die, and the number 1 must be on top of the die when the goal location is reached. Once a goal has been reached, your function should return the set of actions and states reached when moving from the initial state to the goal state. This output will also be helpful for debugging your system from intermediate states.

You will need to implement exactly 3 admissible heuristics for use with your A* search function.

_Note: Your implementation will be smaller and more flexible if you think carefully about the problem representation that you will use before you start coding; in particular, recall the components of a problem definition as discussed in the text and in class, and think about how this could be used directly within your implementation._

Your program must define a program rblock, which takes the name of a puzzle file (text file) from the command line, and then returns the result for each of your three heuristics, along with performance metrics for each, described below.

### Sample Puzzles

Here are some sample puzzles (you will need to copy these out to text files for use in your program). In these diagrams, '.' represents an empty location, '*' represents an obstacle, and 'S' and 'G' represent the starting and goal locations.

Puzzle 1

    S...G
    .....
                   
Puzzle 2
    
    S....
    ..***
    .*..G
    .....
    *....

Puzzle 3       

    S.....
    .****.
    .*....
    .*....
    .....G

Puzzle 4

    .G*.S.
    ...*..
    .*...*
    ......
    ...*..

Puzzle 5

    ...........S
    ............
    ............
    ............
    ....*.......
    ...*........
    ..*.........
    ............
    ....*.......
    ...*........
    ..*.........
    G...........              
    
## Analysis

In addition to your code, you will submit a .pdf file (roughly 3-4 pages in length) discussion.pdf containing the following:

A description of your state space and problem representation.
A (brief!) explanation of how to interpret your output. Please make your output easy to interpret for someone who knows the problem, but not your specific program.
A description of your heuristic functions: what they measure, and why they are admissible.
Performance metrics: for each of the five puzzles above, report the number of states generated (i.e. put on the frontier queue), and the number of states visited using each heuristic.
Briefly discuss the results in terms of the three different heuristics that you employed.