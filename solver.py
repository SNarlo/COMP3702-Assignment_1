#!/usr/bin/python
import sys
from laser_tank import LaserTankMap
from queue import PriorityQueue




"""
Template file for you to implement your solution to Assignment 1.

COMP3702 2020 Assignment 1 Support Code
"""


#
#
# Code for any classes or functions you need can go here.
#
#
input_file = "testcases/t1_bridgeport.txt" # TODO Change this back to arglist[0]
output_file = "testcases/foo.txt"

# Read the input testcase file
game_map = LaserTankMap.process_input_file(input_file)

"""
This function gets all the elements that are surrounding 
the player in terms of U, D, L, R in the direction the tank is facing
"""
def get_successors():

    y = [row[:] for row in game_map.grid_data]

    successors = []

    successors.append(y.grid_data[map.player_y - 1][map.player_x])
    successors.append(map.grid_data[map.player_y + 1][map.player_x])
    successors.append(map.grid_data[map.player_y][map.player_x + 1])
    successors.append(map.grid_data[map.player_y][map.player_x - 1])

    return y


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


    print(get_successors())



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

