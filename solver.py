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


class Node(LaserTankMap):

    def __init__(self, state):
        self.state = state
        self._start_point = (game_map.player_y, game_map.player_x)
        self.end_point = self.__get_end_point()
        self.pos = self.__get_player_pos()
        self.successors = self.get_successors
        self.player_heading = state.player_heading
        self.g_score = self.get_g_score()
        self.h_score = self.heuristic('manhattan')
        self.f_score = self.get_f_score()
        super().__init__(x_size=state.x_size, y_size=state.y_size, grid_data=state.grid_data,
                         player_heading=state.player_heading, player_x=state.player_x, player_y=state.player_y)



    def __get_end_point(self):
        """
        :return: the index [y][x] of the flag point
        """

        length = len(self.state.grid_data)
        width = len(self.state.grid_data[0])
        expanded = []
        index = 0
        while index < len(self.state.grid_data[0]):
            for i in self.state.grid_data:
                expanded.append(i[index])
            index += 1

        index = expanded.index('F')

        return index % length, index % width

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

    def get_g_score(self):
        """
        This is the distance from the starting position
        :param state: The current state the map is in
        :return: The distance from the start position
        """
        g_score = abs(self.pos[0] - game_map.player_y)
        g_score += abs(self.pos[1] - game_map.player_x)

        return g_score

    def get_f_score(self):

        return self.g_score + self.h_score

    def create_copy(self):
        """
        This function copy's the game board
        """
        new_state = copy.deepcopy(self.state)

        return new_state

    def get_successors(self):
        """
        This function gets all the elements that are surrounding
        the player in terms of U, D, L, R in the direction the tank is facing
        """
        successors = []

        for action in self.state.MOVES:
            new_state = self.create_copy()
            self.state = new_state
            n = new_state.apply_move(action)
            if n != self.state.COLLISION:
                successors.append((Node(new_state), action))

        return successors



# def astar(Node, start, end):
#     """
#     This is the implementation of the astar algorithm
#     :param map: The map being played
#     :param start: The player's start position
#     :param end: The end goal position
#     :return:
#     """
#     begin_clock = time.time()
#     log = dict()
#     log['no_vertex_explored'] = 0
#
#     queue = PriorityQueue()
#     f_score = heuristic(state, 'manhattan')
#     queue.put((f_score, state))
#     explored = {state: cost(state)} # a disctionary of vertex: g_score
#
#     path = {state: []}
#     log['no_vertex_explored'] += 1
#
#     while not queue.empty():
#         current = queue.get()
#         print(current[1])
#         current_pos = __get_player_pos(current[1])
#
#         if current_pos == end:
#             log['no_vertex_in_queue_at_termination'] = queue.qsize()
#             log['no_vertex_explored'] = len(explored)
#             log['elapsed_time_in_minutes'] = (time.time()) - begin_clock/60
#             return log
#
#         for neighbour, action, cost in get_successors(current[1]):
#             cost_so_far = explored[current[1]] + [cost]
#             if neighbour not in explored:
#                 explored[current[1]] = [cost]
#                 path[neighbour] = path[current[1]] + [action]
#                 log['no_vertex_explored'] += 1
#                 vfp = cost_so_far + heuristic(neighbour, 'manhattan')
#                 neighbour.value_for_property = vfp
#                 print(queue.put(vfp, neighbour))
#
#     raise RuntimeError('No Solution')






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


    a = Node(game_map)

    node_list = []
    for i in a.get_successors():
        h = i[0].get_successors()
        node_list.append(h)

    for j in node_list:
        for s in j:
            print(s[0].render())






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

