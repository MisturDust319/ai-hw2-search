"""
A set of funtions used to solve the missionaries and cannibals problem
using breadth first search

Authored by Stan Slupecki
"""
from shared import *


class MissionariesCannibalsState(State):
    """"
    A node representing the state of a step in a solution to the Missionaries & Cannibals problem
    """
    def __init__(self, payload, direction="left", parent=None, depth=1):
        """
        A node representing the state of a step in a solution to the Missionaries & Cannibals problem
        :param payload:
        The data representing the missionaries and cannibals on both sides of the river
        :param direction:
        The direction the boat will be HEADING (not the current side)
        :param parent:
        The node used to generate this state
        :param depth:
        The number of nodes, including this one, that are on the current solution path
        """
        # init the State superclass with the proper info
        super().__init__(payload, parent, depth)
        # set the starting direction
        self.direction = direction

    def compare(self, other):
        # compare the missionaries and cannibals on both sides of the river for the current node and the other nodes
        left_missionary_comparison = self.payload["left_bank"]["missionaries"] == other.payload["left_bank"]["missionaries"]
        left_cannibal_comparison = self.payload["left_bank"]["cannibals"] == other.payload["left_bank"]["cannibals"]
        right_missionary_comparison = self.payload["right_bank"]["missionaries"] == other.payload["right_bank"]["missionaries"]
        right_cannibal_comparison = self.payload["right_bank"]["cannibals"] == other.payload["right_bank"]["cannibals"]
        # compare the direction this and the other node is heading
        direction_comparison = self.direction == other.direction
        if(other.direction is None):
            direction_comparison = True
            # when direction is None, this means it's an end goal, so
            # it doesn't matter what side the boat is on
            # default to true

        return left_missionary_comparison and left_cannibal_comparison\
               and right_missionary_comparison and right_cannibal_comparison\
               and direction_comparison


def actions_missionaries_cannibals_factory(boat_capacity=2):
    """
    Returns a callback that can calculate solutions for the
    Missionaries & Cannibals problem that uses a specific boat capacity
    :param boat_capacity:
    the boat capacity for the returned solution callback
    :return:
    a callback function that can calculate possible solutions for the problem
    when given a state
    """
    def actions_missionaries_cannibals(state):
        """
        A function that solves Missionaries & Cannibals problem
        :param state:
        The current state of the problem
        :return:
        an iterable that represnts possible solutions given the current problem state
        """
        # set the maximum boat capacity
        boatsize = boat_capacity
        # generate tuples representing the number of missionaries and cannibals in the boat
        #   (missionaries, cannibals)
        # the boat can hold from 1 to it's capacity number of people
        possible = [tuple((i, boatsize-i)) for i in range(boatsize+1) if i == 0 or i >= boatsize-i]
        # this generates a full capacity boat
        # note it avoids combinations where cannibals exceed missionaries
        possible += [tuple((i, 0)) for i in range(1, boatsize)]
        # for when the boat only carries missionaries but doesn't reach capacity
        possible += [tuple((0, i)) for i in range(1, boatsize)]
        # for when the boat only carries cannibals but doesn't reach capacity

        # an array to store results
        results = []
        for possibility in possible:
            # first value is missionaries in the boat, second is cannibals
            (missionaries, cannibals) = possibility
            if cannibals > missionaries and missionaries != 0:
                continue
                # there shouldn't be more cannibals in the boat
                # the list comprehension should handle this but jik
            if state.direction == "left":
                # if going left, remove from the right bank, add to the left
                # first missionaries
                left_missionaries = missionaries + state.payload["left_bank"]["missionaries"]
                right_missionaries = state.payload["right_bank"]["missionaries"] - missionaries
                # then cannibals
                left_cannibals = cannibals + state.payload["left_bank"]["cannibals"]
                right_cannibals = state.payload["right_bank"]["cannibals"] - cannibals

                # skip invalid solutions
                if left_cannibals < 0 or right_cannibals < 0 or left_missionaries < 0 or right_missionaries < 0:
                    continue
                    # negative values are invalid
                if left_cannibals > left_missionaries and left_missionaries != 0:
                    continue
                    # if cannibals and missionaries are both present, the cannibals can't outnumber the missionaries
                if right_cannibals > right_missionaries and right_missionaries != 0:
                    continue
                    # if cannibals and missionaries are both present, the cannibals can't outnumber the missionaries

                # if all is still well, create a new state node
                # create a dict to represent the state payload
                new_payload = {}
                new_payload["left_bank"] = {}
                new_payload["right_bank"] = {}
                new_payload["left_bank"]["missionaries"] = left_missionaries
                new_payload["right_bank"]["missionaries"] = right_missionaries
                new_payload["left_bank"]["cannibals"] = left_cannibals
                new_payload["right_bank"]["cannibals"] = right_cannibals
                # create the state
                new_state = MissionariesCannibalsState(new_payload, "right", state, state.depth+1)
                # add this to results
                results.append(new_state)
            else:
                # if going right, remove from the left bank, add to the right
                # first missionaries
                left_missionaries = state.payload["left_bank"]["missionaries"] - missionaries
                right_missionaries = state.payload["right_bank"]["missionaries"] + missionaries
                # then cannibals
                left_cannibals = state.payload["left_bank"]["cannibals"] - cannibals
                right_cannibals = state.payload["right_bank"]["cannibals"] + cannibals

                # skip invalid solutions
                if left_cannibals < 0 or right_cannibals < 0 or left_missionaries < 0 or right_missionaries < 0:
                    continue
                    # negative values are invalid
                if left_cannibals > left_missionaries and left_missionaries != 0:
                    continue
                    # if cannibals and missionaries are both present, the cannibals can't outnumber the missionaries
                if right_cannibals > right_missionaries and right_missionaries != 0:
                    continue
                    # if cannibals and missionaries are both present, the cannibals can't outnumber the missionaries

                # if all is still well, create a new state node
                # create a dict to represent the payload
                new_payload = {}
                new_payload["left_bank"] = {}
                new_payload["right_bank"] = {}
                new_payload["left_bank"]["missionaries"] = left_missionaries
                new_payload["right_bank"]["missionaries"] = right_missionaries
                new_payload["left_bank"]["cannibals"] = left_cannibals
                new_payload["right_bank"]["cannibals"] = right_cannibals
                # create the state
                new_state = MissionariesCannibalsState(new_payload, "left", state, state.depth+1)
                # add this to results
                results.append(new_state)
        return results

    # return the custom callback
    return actions_missionaries_cannibals

