import numpy as np
import collections

class State:
    """
    basic state clase
    keeps track of a piece of data and depth
    """
    def __init__(self, payload, parent=None, depth=0):
        self.payload = payload
        self.parent = parent
        self.depth = depth

    def compare(self, other):
        return all((self.payload[i] == other.payload[i]) for i in range(3))

    def print_path(self):
        # print the parent's data before this data
        if(self.parent):
            self.parent.print_path()
        # print this node's data
        self.print_data()

    def print_data(self):
        print("Depth: " + str(self.depth) + " Value: " + str(self.payload))

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

def breadth_first_search():
    node = State(np.array([3,3,1]))
    # starting value
    goal = State(np.array([0,0,0]))
    # ending value
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
        return True
    while True:
        try:
            node = frontier.pop()
            # get the next node from the frontier
        except IndexError:
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
                    # only append if not a goal state
                    # a solution derived from a goal state would be redundant
                    # and at best, would be a deeper, less efficient solution
                    frontier.append(newstate)


print(breadth_first_search())

