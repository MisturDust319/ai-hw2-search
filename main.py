from shared import *
from missionaries_cannibals import *

# TEST SEARCH
start = State(np.array([3,3,1]))
# starting value
end = State(np.array([0,0,0]))
# ending value
print("Test Search")
print(breadth_first_search(start, end, actions))

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

print("Missionaries and Cannibals")
print(breadth_first_search(start_node, end_node, actions_missionaries_cannibals))
