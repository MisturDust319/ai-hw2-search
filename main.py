import numpy as np
import collections

class State:
    """
    basic state clase
    keeps track of a piece of data, it's parent, and depth
    """
    def __init__(self, payload, parent=None, depth=0):
        self.payload = payload
        self.parent = parent
        self.depth = depth

    def compare(self, other):
        return all((self.payload[i] == other.payload[i]) for i in range(3))

    def print_path(self):
        # print the parent's data before this data
        if self.parent:
            self.parent.print_path()
        # print this node's data
        self.print_data()

    def print_data(self):
        print("Depth: " + str(self.depth) + " Value: " + str(self.payload))


class MissionariesCannibalsState(State):
    def __init__(self, payload, direction="left", parent=None, depth=0):
        # call the super function
        super().__init__(payload, parent, depth)
        self.direction = direction

    def compare(self, other):
        left_missionary_comparison = self.payload["left_bank"]["missionaries"] == other.payload["left_bank"]["missionaries"]
        left_cannibal_comparison = self.payload["left_bank"]["cannibals"] == other.payload["left_bank"]["cannibals"]
        right_missionary_comparison = self.payload["right_bank"]["missionaries"] == other.payload["right_bank"]["missionaries"]
        right_cannibal_comparison = self.payload["right_bank"]["cannibals"] == other.payload["right_bank"]["cannibals"]
        direction_comparison = self.direction == other.direction
        if(other.direction is None):
            direction_comparison = True
            # when direction is None, this means it's an end goal, so
            # it doesn't matter what side the boat is on
            # default to true

        return left_missionary_comparison and left_cannibal_comparison\
               and right_missionary_comparison and right_cannibal_comparison\
               and direction_comparison

def actions_missionaries_cannibals(state):
    boatsize = 2
    # generate tuples representing the number of missionaries and cannibals in the boat
    possible = [tuple((i, boatsize-i)) for i in range(boatsize+1) if i == 0 or i >= boatsize-i]
    possible += [tuple((i, 0)) for i in range(1, boatsize)]
    possible += [tuple((0, i)) for i in range(1, boatsize)]
    # (missionaries, cannibals)
    # this comprehension makes sure that the first outnumbers the second

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
            new_payload = {}
            new_payload["left_bank"] = {}
            new_payload["right_bank"] = {}
            new_payload["left_bank"]["missionaries"] = left_missionaries
            new_payload["right_bank"]["missionaries"] = right_missionaries
            new_payload["left_bank"]["cannibals"] = left_cannibals
            new_payload["right_bank"]["cannibals"] = right_cannibals
            new_state = MissionariesCannibalsState(new_payload, "right", state, state.depth+1)
            # yield the state
            # yield new_state
            results.append(new_state)
        else:
            # if going right, remove from the left bank, add to the right
            left_missionaries = state.payload["left_bank"]["missionaries"] - missionaries
            right_missionaries = state.payload["right_bank"]["missionaries"] + missionaries
            # then cannibals
            left_cannibals = state.payload["left_bank"]["cannibals"] - cannibals
            right_cannibals = state.payload["right_bank"]["cannibals"] + cannibals
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
            new_payload = {}
            new_payload["left_bank"] = {}
            new_payload["right_bank"] = {}
            new_payload["left_bank"]["missionaries"] = left_missionaries
            new_payload["right_bank"]["missionaries"] = right_missionaries
            new_payload["left_bank"]["cannibals"] = left_cannibals
            new_payload["right_bank"]["cannibals"] = right_cannibals
            new_state = MissionariesCannibalsState(new_payload, "left", state, state.depth+1)
            # yield the state
            # yield new_state
            results.append(new_state)
    return results

def actions(state):
    # generate a list of actions based on the current state
    # state is a 3 value array:

    possible = np.array([[0, 1, 1], [1, 0, 1], [1, 1, 1], [0, 2, 1], [2, 0, 1]])
    # generate an array of valid values
    sending = 1 - 2 * state.payload[2]
    # find the number being sent from the right bank
    for p in possible:
        ns_ws = State(np.add(np.multiply(sending, p), state.payload), state, state.depth+1)
        # find the number of people on the left (west) side
        ns_rs = np.subtract(np.array([3, 3, 1]), ns_ws.payload)
        # find the number of people on the right side
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

def is_in(item,things):
    return any((item.compare(athing)) for athing in things)

def breadth_first_search(start, goal, actions):
    # first init node to start
    node = start
    frontier = collections.deque([node])
    # next left to explore
    explored = []
    # previously visited

    # this version can return many solutions
    # this holds solutions
    solutions = []
    # this value holds the depth of the last found solution
    # start at none
    max_solution_depth = None

    print(frontier)
    if (node.compare(goal)):
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
            if(len(solutions) > 0):
                # print the first solution
                print("Solution Depth: " + str(solutions[0].depth))
                solutions[0].print_path()
                return True
            return False
            # if there isn't another node, then there is no solution

        explored.append(node)
        # mark the current node as explored
        # print(explored)

        # generate possible actions based on the current node
        for newstate in actions(node):

            if not(is_in(newstate, explored) or is_in(newstate, frontier)):
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

"""
start = State(np.array([3,3,1]))
# starting value
end = State(np.array([0,0,0]))
# ending value
print(breadth_first_search(start, end, actions))
"""
"""
assume that:
    1. missionaries must outnumber the cannibals, lest they be eaten
    2. we are done when the missionaries are on the left bank and
        cannibals are on the right
    3. we start with 3 missionaries and 3 cannibals on the
        right bank
"""
start_payload = {}
start_payload["left_bank"] = {}
start_payload["right_bank"] = {}
start_payload["left_bank"]["missionaries"] = 0
start_payload["left_bank"]["cannibals"] = 0
start_payload["right_bank"]["missionaries"] = 3
start_payload["right_bank"]["cannibals"] = 3

end_payload = {}
end_payload["left_bank"] = {}
end_payload["right_bank"] = {}
end_payload["left_bank"]["missionaries"] = 3
end_payload["left_bank"]["cannibals"] = 0
end_payload["right_bank"]["missionaries"] = 0
end_payload["right_bank"]["cannibals"] = 3

start_node = MissionariesCannibalsState(start_payload, "left")
end_node = MissionariesCannibalsState(end_payload, None)

print(breadth_first_search(start_node, end_node, actions_missionaries_cannibals))
