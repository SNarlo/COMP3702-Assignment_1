#!/usr/bin/python
import sys
from laser_tank import LaserTankMap
from queue import PriorityQueue
import copy
import time
import queue as queuelib
import math



"""
Template file for you to implement your solution to Assignment 1.

COMP3702 2020 Assignment 1 Support Code
"""

#
#
# Code for any classes or functions you need can go here.
#
#


class Node(LaserTankMap):
    def __init__(self, state):
        self.state = state
        self._start_point = (state.player_y, state.player_x)
        self.end_point = self.__get_end_point()
        self.pos = self.__get_player_pos()
        self.successors = self.get_successors
        self.player_heading = state.player_heading
        self.cost = 0
        self.h_score = self.heuristic('manhattan')
        self.g_score = 0
        self.grid = hash(self.get_hash_grid())
        self.id = hash((self.pos[0], self.pos[1], self.player_heading, self.grid)) # all the elements that change with moves
        super().__init__(x_size=state.x_size, y_size=state.y_size, grid_data=state.grid_data,
                         player_heading=state.player_heading, player_x=state.player_x, player_y=state.player_y)

    def get_hash_grid(self): # converts the grid data map into a tuple of tuples in order allow hashing
        i = 0
        tuplised = []
        while i < len(self.state.grid_data):
            tuplised.append(tuple(self.state.grid_data[i]))
            i += 1

        return tuple(tuplised)

    def __get_end_point(self):
        """
        :return: the index [y][x] of the flag point
        """

        length = len(self.state.grid_data)
        width = len(self.state.grid_data[0])
        expanded = []
        index = 0
        while index < width:
            for i in self.state.grid_data:
                expanded.append(i[index])
            index += 1

        index = expanded.index('F')
        width_index = (self.state.grid_data[index % length]).index('F')

        return index % length, width_index

    def __get_player_pos(self):
        """
        A function which returns the current position of the player
        :return: The players coordinates [y][x]
        """
        return self.state.player_y, self.state.player_x

    def heuristic(self, mode):
        """
        The heuristic function
        :param state: The game state
        :param mode: The type of heuristic implemented
        :return: The estimated distance between the tank and the goal
        """
        if mode == 'manhattan':
            h_score_estimate = abs(self.end_point[0] - self.pos[0])
            h_score_estimate += abs(self.end_point[1] - self.pos[1])
        else:
            raise NotImplementedError(mode)
        return h_score_estimate

    def create_copy(self):
        """
        This function copy's the game board
        """
        new_map = [row[:] for row in self.grid_data]

        new_state = LaserTankMap(x_size=self.x_size, y_size=self.y_size, grid_data=new_map, player_x=self.player_x,
                                 player_y=self.player_y, player_heading=self.player_heading)

        return new_state

    def get_successors(self):
        """
        This function gets all the nodes that are surrounding
        the player
        """
        successors = []

        for action in self.state.MOVES:
            new_state = self.create_copy()
            self.state = new_state
            n = new_state.apply_move(action)
            if n == self.SUCCESS:
                successors.append((Node(new_state), action))

        return successors

    # def __gt__(self, other):
    #     return self.cost > other.cost

    def __lt__(self, other):
        return self.cost < other.cost

    def __eq__(self, other):
        return self.id == other.id

class Goal(Node):
    def __init__(self, state):
        self.state = state
        super().__init__(state=state)
        self.pos = self.end_point


def astar(start, end):
    """
    This is the implementation of the astar algorithm
    :param node: The map being played
    :param start: The player's start position
    :param end: The end goal position
    :return:
    """
    begin_clock = time.time()
    log = dict()
    log['nodes_explored'] = 0

    frontier = PriorityQueue()
    frontier.put(start)
    explored = set()
    path = {start.id: []}

    while not frontier.empty():
        current = frontier.get()

        explored.add(current.id)
        log['nodes_explored'] += 1

        if current.pos == end.pos: # calculate these when the end is found
            log['action_path'] = path[current.id]
            log['path_length'] = len(path[current.id])
            log['nodes_in_fringe_at_termination'] = frontier.qsize()
            log['elapsed_time_in_seconds'] = ((time.time()) - begin_clock)
            return log

        for neighbour, action in current.get_successors():  # getting all the neighbours of the current node
            if neighbour.id not in explored: # if the neighbour is not in explored or if the total g score is less than the neighbors g_score
                neighbour.g_score = current.g_score + 1
                path[neighbour.id] = path[current.id] + [action] # update the path
                log['nodes_explored'] += 1 # add vertex to the total
                neighbour.cost = neighbour.h_score + neighbour.g_score
                frontier.put(neighbour)

    raise RuntimeError('No Solution')


def ucs(start, goal):

    begin_clock = time.time()
    log = dict()
    log['nodes_explored'] = 0
    path = {start.id: []}
    visited = set()
    fringe = PriorityQueue()
    fringe.put(start)

    while not fringe.empty():
        node = fringe.get()

        visited.add(node.id)
        log['nodes_explored'] += 1

        if node.pos == goal.pos:
            # log['action_path'] = path[node.id]
            log['path_length'] = len(path[node.id])
            log['nodes_in_fringe_at_termination'] = fringe.qsize()
            log['elapsed_time_in_seconds'] = ((time.time()) - begin_clock)
            return log

        for n, action in node.get_successors():
            if n.id not in visited:
                path[n.id] = path[node.id] + [action]
                n.cost = node.cost + 1
                fringe.put(n)

    raise RuntimeError('No solution!')


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
    # input_file = arglist[0]
    # output_file = arglist[1]
    input_file = "testcases/t3_labyrinth.txt"
    output_file = "testcases/output.txt"

    # Read the input testcase file
    game_map = LaserTankMap.process_input_file(input_file)

    actions = []


    start = Node(game_map)
    end = Goal(game_map)

    solution = (astar(start, end))
    print(solution)

    for i in solution:
        actions.append(i)


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