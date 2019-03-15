"""
A set of funtions used to solve the Fox, Goose, and Bean problem
using breadth first search

Authored by Stan Slupecki
"""

__author__ = "Stan Slupecki"

from shared import *

class FoxGooseBeanState(State):
    def __init__(self, direction="left", left_bank=(False, False, False), right_bank=(True, True, True), parent=None, depth=1):
        """
        A node representing the state of the Fox, Goose, and Beans problem
        :param direction:
        The direction the boat will be heading
        :param left_bank:
        The occupants of the left bank, represented as a 3-Tuple binary flag
        with 1 representing that object/animal is present on the shore
            (Fox, Goose, Beans)
        :param right_bank:
        The occupants of the right bank, represented as a 3-Tuple binary flag
        with 1 representing that object/animal is present on the shore
            (Fox, Goose, Beans)
        :param parent:
        Parent node used to generate this node
        :param depth:
        Length of the path of this current solution
        """
        super().__init__(None, parent, depth)
        # init the superclass

        self.direction = direction
        self.left_bank = left_bank
        self.right_bank = right_bank

    def compare(self, other):
        # simple cross compare each corresponding element
        left_bank_compare = self.left_bank == other.left_bank
        right_bank_compare = self.right_bank == other.right_bank
        direction_compare = self.direction == other.direction

        return left_bank_compare and right_bank_compare and direction_compare

    def print_data(self):
        bank = "left" if self.direction == "right" else "right"
        
        left_bank_occupants = " "
        if self.left_bank[0]:
            left_bank_occupants += "fox "
        if self.left_bank[1]:
            left_bank_occupants += "goose "
        if self.left_bank[2]:
            left_bank_occupants += "beans "

        right_bank_occupants = " "
        if self.right_bank[0]:
            right_bank_occupants += "fox "
        if self.right_bank[1]:
            right_bank_occupants += "goose "
        if self.right_bank[2]:
            right_bank_occupants += "beans "
            
        print("Boat on " + bank + " bank * Left Bank Occupants:" + left_bank_occupants + "* Right Bank Occupants:" + right_bank_occupants)

def actions_fox_goose_beans(state):
    # helper functions that are used to move the objects between the shores
    def swap_fox(left_bank, right_bank):
        """
        move the fox to opposite shore
        """
        (left_fox, left_goose, left_beans) = left_bank
        (right_fox, right_goose, right_beans) = right_bank
        # the behavior depends on where the boat is heading
        if state.direction == "left":
            # if on the right bank preparing to transport to left
            if right_fox:
                # only create a new set of values if there is a fox to move
                # move fox from left bank to right
                new_left_bank = (True, left_goose, left_beans)
                new_right_bank = (False, right_goose, right_beans)

                return (new_left_bank, new_right_bank)
            else:
                # otherwise return the original values
                return (left_bank, right_bank)
        else:
            # if on the left bank preparing to transport to right
            if left_fox:
                # only create a new set of values if there is a fox to move
                # move fox from left bank to right
                new_left_bank = (False, left_goose, left_beans)
                new_right_bank = (True, right_goose, right_beans)

                return (new_left_bank, new_right_bank)
            else:
                # otherwise return the original values
                return (left_bank, right_bank)

    def swap_goose(left_bank, right_bank):
        """
        move the goose to opposite shore
        """
        (left_fox, left_goose, left_beans) = left_bank
        (right_fox, right_goose, right_beans) = right_bank
        # the behavior depends on where the boat is heading
        if state.direction == "left":
            # if on the right bank preparing to transport to left
            if right_goose:
                # only create a new set of values if there is a goose to move
                # move goose from left bank to right
                new_left_bank = (left_fox, True, left_beans)
                new_right_bank = (right_fox, False, right_beans)

                return (new_left_bank, new_right_bank)
            else:
                # otherwise return the original values
                return (left_bank, right_bank)
        else:
            # if on the left bank preparing to transport to right
            if left_goose:
                # only create a new set of values if there is a goose to move
                # move goose from left bank to right
                new_left_bank = (left_fox, False, left_beans)
                new_right_bank = (right_fox, True, right_beans)

                return (new_left_bank, new_right_bank)
            else:
                # otherwise return the original values
                return (left_bank, right_bank)

    def swap_beans(left_bank, right_bank):
        """
        move the beans to opposite shore
        """
        (left_fox, left_goose, left_beans) = left_bank
        (right_fox, right_goose, right_beans) = right_bank
        # the behavior depends on where the boat is heading
        if state.direction == "left":
            # if on the right bank preparing to transport to left
            if right_beans:
                # only create a new set of values if there is a beans to move
                # move beans from left bank to right
                new_left_bank = (left_fox, left_goose, True)
                new_right_bank = (right_fox, right_goose, False)

                return (new_left_bank, new_right_bank)
            else:
                # otherwise return the original values
                return (left_bank, right_bank)
        else:
            # if on the left bank preparing to transport to right
            if left_beans:
                # only create a new set of values if there is a beans to move
                # move beans from left bank to right
                new_left_bank = (left_fox, left_goose, False)
                new_right_bank = (right_fox, right_goose, True)

                return (new_left_bank, new_right_bank)
            else:
                # otherwise return the original values
                return (left_bank, right_bank)

    #INVALID SOLUTIONS
    fox_and_goose = (True, True, False)
    goose_and_beans = (False, True, True)

    # create a list of the helper functions
    possibilities = [swap_fox, swap_goose, swap_beans]

    # iterate through the helper functions to generate an iterable of
    # possible new solutions
    for action in possibilities:
        # generate new possible values for left and right bank
        (new_left_bank, new_right_bank) = action(state.left_bank, state.right_bank)

        # REMOVE INVALID SOLUTIONS
        # if the farmer is on the right bank, he can't tend to the left bank
        # direction left means farmer is on right bank, making a trip to left bank
        if state.direction == "left":
            # check if the bank leaves the fox with the goose
            if new_right_bank == fox_and_goose:
                continue
            # check if bank leaves goose with beans
            if new_right_bank == goose_and_beans:
                continue

            # otherwise, create a new state wit this data
            new_state = FoxGooseBeanState("right", new_left_bank, new_right_bank, state, state.depth + 1)
            yield new_state
        # if the farmer is on the left bank, he can't tend to the right bank
        else:
            # check if the bank leaves the fox with the goose
            if new_left_bank == fox_and_goose:
                continue
            # check if bank leaves goose with beans
            if new_left_bank == goose_and_beans:
                continue

            # otherwise, create a new state wit this data
            new_state = FoxGooseBeanState("left", new_left_bank, new_right_bank, state, state.depth + 1)
            yield new_state
