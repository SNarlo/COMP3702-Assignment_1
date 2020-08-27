#!/usr/bin/python
import sys
from laser_tank import LaserTankMap
from queue import PriorityQueue
import copy



"""
Template file for you to implement your solution to Assignment 1.

COMP3702 2020 Assignment 1 Support Code
"""


#
#
# Code for any classes or functions you need can go here.
#
#

"""
This function copy's the game board 
"""
def create_copy(current_state):
    new_state = copy.deepcopy(current_state)

    return new_state

"""
This function gets all the elements that are surrounding 
the player in terms of U, D, L, R in the direction the tank is facing
"""
def get_successors(state):

    successors = []

    for action in state.MOVES:
        new_state = create_copy(state)
        new_state.apply_move(action)
        successors.append(new_state)

    return successors

def UCS(map, start, end):

    queue = PriorityQueue()



def write_output_file(filename, actions):
    """
    Write a list of actions to an output file. You should use this method to write your output file.
    :param filename: name of output file
    :param actions: list of actions where is action is in LaserTankMap.MOVES
    """
    f = open(filename, 'w')
    for i in range(len(actions)):
        f.write(str(actions[i]))
        if i < len(actions) - 1:
            f.write(',')
    f.write('\n')
    f.close()


def main(arglist):
    input_file = "testcases/t1_bridgeport.txt" # TODO Change this back to arglist[0]
    output_file = "testcases/foo.txt"

    # Read the input testcase file
    game_map = LaserTankMap.process_input_file(input_file)

    actions = []


    #
    #
    # Code for your main method can go here.
    #
    # Your code should find a sequence of actions for the agent to follow to reach the goal, and store this sequence
    # in 'actions'.
    #
    #

    # Write the solution to the output file
    write_output_file(output_file, actions)


if __name__ == '__main__':
    main(sys.argv[1:])

