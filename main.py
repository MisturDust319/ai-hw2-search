"""
A serious of tests of various search functions and AI problems

All either edited or authored by Stan Slupecki
"""

from shared import *
from missionaries_cannibals import *
from fox_goose_beans import *

# TEST SEARCH
start = State(np.array([3,3,1]))
# starting value
end = State(np.array([0,0,0]))
# ending value
print("###############################################################################################################")
print("Test Search")
print("###############################################################################################################")
print(breadth_first_search(start, end, test_actions))

# MISSIONARIES & CANNIBALS
"""
assume that:
    1. missionaries must outnumber the cannibals, lest they be eaten
    2. we are done when the missionaries are on the left bank and
        cannibals are on the right
    3. we start with 3 missionaries and 3 cannibals on the
        right bank
"""
# create dictionaries to represent the payload
start_payload = {}
start_payload["left_bank"] = {}
start_payload["right_bank"] = {}
start_payload["left_bank"]["missionaries"] = 0
start_payload["left_bank"]["cannibals"] = 0
start_payload["right_bank"]["missionaries"] = 3
start_payload["right_bank"]["cannibals"] = 3
# use the dictionary to create the starting state
start_node = MissionariesCannibalsState(start_payload, "left")

end_payload = {}
end_payload["left_bank"] = {}
end_payload["right_bank"] = {}
end_payload["left_bank"]["missionaries"] = 3
end_payload["left_bank"]["cannibals"] = 0
end_payload["right_bank"]["missionaries"] = 0
end_payload["right_bank"]["cannibals"] = 3
# use the dictionary to create the ending state
end_node = MissionariesCannibalsState(end_payload, None)

print("###############################################################################################################")
print("Missionaries and Cannibals")
print("###############################################################################################################")
print("Capacity 2:")
print("###############################################################################################################")
# generate a callback for a two person boat
solution_capacity_two = actions_missionaries_cannibals_factory()
print(breadth_first_search(start_node, end_node, solution_capacity_two))

print("###############################################################################################################")
print("Capacity 3:")
solution_capacity_three = actions_missionaries_cannibals_factory(3)
print(breadth_first_search(start_node, end_node, solution_capacity_three))
print("###############################################################################################################")

# FOX, GOOSE, AND BEANS PROBLEM
print("###############################################################################################################")
print("The Farmer, His Fox, His Goose, and His Beans")
print("###############################################################################################################")
start_node = FoxGooseBeanState()
end_node = FoxGooseBeanState("right", (True, True, True), (False, False, False), None)
print(breadth_first_search(start_node, end_node, actions_fox_goose_beans))
print("###############################################################################################################")
