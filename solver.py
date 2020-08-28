#!/usr/bin/python
import sys
from laser_tank import LaserTankMap
from queue import PriorityQueue
import copy
import time



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


def create_copy(current_state):
    """
    This function copy's the game board
    """
    new_state = copy.deepcopy(current_state)

    return new_state


def get_successors(state):
    """
    This function gets all the elements that are surrounding
    the player in terms of U, D, L, R in the direction the tank is facing
    """
    successors = []

    for action in state.MOVES[1:4]:
        new_state = create_copy(state)
        new_state.apply_move(action)
        n = new_state.apply_move('f')
        if new_state.cell_is_laser_movable(new_state.player_y, new_state.player_x, new_state.player_heading):
            new_state.apply_move('s')
        if n != 1:
            successors.append((new_state, action))

    return successors


def __get_end_point(state):
    """
    :return: the index [y][x] of the flag point
    """

    length = len(state.grid_data)
    width = len(state.grid_data[0])
    expanded = []
    index = 0
    while index < len(state.grid_data[0]):
        for i in state.grid_data:
            expanded.append(i[index])
        index += 1

    index = expanded.index('F')

    return index % length, index % width


def __get_player_pos(state):
    """
    A function which returns the current position of the player
    :param state: The current state (map)
    :return: The players coordinates [y][x]
    """
    return state.player_y, state.player_x


def heuristic(state, mode):
    """
    The heuristic function
    :param state: The game state
    :param mode: The type of heuristic implemented
    :return: The estimated distance between the tank and the goal
    """
    if mode == 'manhattan':
        h_score_estimate = abs(__get_end_point(state)[0] - __get_player_pos(state)[0])
        h_score_estimate += abs(__get_end_point(state)[1] - __get_player_pos(state)[1])
    else:
        raise NotImplementedError(mode)
    return h_score_estimate


def cost(state):
    """
    This is the distance from the starting position
    :param state: The current state the map is in
    :return: The distance from the start position
    """
    g_score = abs(__get_player_pos(state)[0] - game_map.player_y)
    g_score += abs(__get_player_pos(state)[1] - game_map.player_x)

    return g_score


def __lt__(state, other_state):
    return state < other_state


def astar(state, start, end):
    """
    This is the implementation of the astar algorithm
    :param map: The map being played
    :param start: The player's start position
    :param end: The end goal position
    :return:
    """
    begin_clock = time.time()
    log = dict()
    log['no_vertex_explored'] = 0

    queue = PriorityQueue()
    queue.put(state)
    explored = {state: cost(state)} # a disctionary of vertex: g_score

    path = {state: []}
    log['no_vertex_explored'] += 1

    while not queue.empty():
        current = queue.get()
        if current == end:
            log['no_vertex_in_queue_at_termination'] = queue.qsize()
            log['no_vertex_explored'] = len(explored)
            log['elapsed_time_in_minutes'] = (time.time()) - begin_clock/60
            return log

        for neighbour, action in get_successors(current):
            cost_so_far = explored[current] + cost(neighbour)
            if neighbour not in explored:
                explored[current] = cost_so_far
                path[neighbour] = path[current] + [action]
                log['no_vertex_explored'] += 1
                vfp = cost_so_far + heuristic(neighbour, 'manhattan')
                neighbour.value_for_property = vfp
                print(path)


    # raise RuntimeError('No Solution')






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


    print(astar(game_map, __get_player_pos(game_map), __get_end_point(game_map)))











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

