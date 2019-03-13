"""
Defines shared functions and classes

Edited and partially authored by Stan Slupecki
"""

import numpy as np
import collections

class State:
    """
    basic state class
    keeps track of a piece of data, it's parent, and depth
    """
    def __init__(self, payload, parent=None, depth=1):
        """
        basic state class
        keeps track of a piece of data, it's parent, and depth
        :param payload:
        the data to be stored
        :param parent:
        the state of the node used to generate this state
        :param depth:
        how many deep the solution to this is
        """
        self.payload = payload
        self.parent = parent
        self.depth = depth

    def compare(self, other):
        """
        check if the current node is equal to another
        :param other:
        the other node to compare to
        :return:
        True if the two states are equal
        False otherwise
        """
        return all((self.payload[i] == other.payload[i]) for i in range(3))

    def print_path(self):
        """
        print the path of the solution to the problem
        """
        # print the parent's data before this data
        if self.parent:
            self.parent.print_path()
        # print this node's data
        self.print_data()

    def print_data(self):
        """
        instructions on how to print this node's data
        """
        print("Depth: " + str(self.depth) + " Value: " + str(self.payload))

def is_in(item,things):
    return any((item.compare(athing)) for athing in things)

def breadth_first_search(start, goal, actions):
    """
    A breadth first search
    :param start:
    The starting state of the search
    :param goal:
    The goal state of the search
    :param actions:
    a callback that generates an iteratable containing possible solutions
    given a state
    actions
        :param state
        the state used to generate solutions to the problem
    :return:
    True if a solution is found
    False otherwise
    """
    # first init node to start
    node = start
    # create a queue to represent the frontier
    frontier = collections.deque([node])
    # create a list to hold already explored solutions
    explored = []

    # create a list for found solutions
    solutions = []
    # this value holds the depth of the last found solution
    # start at none
    max_solution_depth = None

    # check if the start state already is the goal state
    if node.compare(goal):
        # print the first solution
        print("Solution Depth: " + str(node.depth))
        node.print_path()
        return True
    while True:
        try:
            node = frontier.pop()
            # get the next node from the frontier
        except IndexError:
            # if there is a solution, print it and return True
            if len(solutions) > 0:
                # print the first solution
                print("Solution Depth: " + str(solutions[0].depth))
                solutions[0].print_path()
                return True
            return False
            # if there isn't another node, then there is no solution

        explored.append(node)
        # mark the current node as explored

        # generate possible actions based on the current node
        for newstate in actions(node):
            # don't explore states that have already been explored
            if not(is_in(newstate, explored) or is_in(newstate, frontier)):
                # check if at goal state
                if newstate.compare(goal):
                    # the first goal state is always accepted
                    if not solutions:
                        # if no solutions are yet found, add one
                        # and set the maximum depth
                        solutions.append(newstate)
                        max_solution_depth = newstate.depth

                    elif newstate.depth > max_solution_depth:
                        # if the newstate depth exceeds the max solution depth
                        # we've exhausted the most efficient solutions
                        # so end the search and display the results
                        # first sort the solutions by depth
                        solutions.sort(key=lambda x: x.depth)

                        # print the first solution
                        print("Solution Depth: " + str(solutions[0].depth))
                        solutions[0].print_path()

                        # if there is a second solution, print it
                        if(len(solutions) > 1):
                            print("Solution Depth: " + str(solutions[1].depth))
                            solutions[1].print_path()

                        return True
                else:
                    # only append new state to frontier if not a goal state
                    # a solution derived from a goal state would be redundant
                    # and even if followed, would be a deeper, less efficient solution
                    frontier.append(newstate)

def actions(state):
    """
    a test action function for the breadth first search
    also a template for making such functions
    :param state:
    the state being used to generate solutions
    :return:
    an interable that represents possible solutions for the problem
    """
    # generate a list of actions based on the current state
    # state is a 3 value array:

    possible = np.array([[0, 1, 1], [1, 0, 1], [1, 1, 1], [0, 2, 1], [2, 0, 1]])
    # generate an array of valid values
    sending = 1 - 2 * state.payload[2]
    # find the number being sent from the right bank
    for p in possible:
        ns_ws = State(np.add(np.multiply(sending, p), state.payload), state, state.depth+1)
        ns_rs = np.subtract(np.array([3, 3, 1]), ns_ws.payload)
        if ns_ws.payload[0] <0:
            continue
            # you can't have negative values
        if ns_rs[0] <0:
            continue
            # you can't have negative values
        if ns_ws.payload[0] > ns_ws.payload[1] and ns_ws.payload[1] > 0:
            continue
        if ns_rs[0] > ns_rs[1] and ns_rs[1] > 0:
            continue
        yield ns_ws
    pass