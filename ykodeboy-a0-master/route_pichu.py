#!/usr/local/bin/python3
#
# route_pichu.py : a maze solver
#
# Submitted by :  Name:- Yamini Priya, Username:- ykodeboy
#
# Based on skeleton code provided in CSCI B551, Spring 2021.


import sys
import json

# Parse the map from a given filename
def parse_map(filename):
    with open(filename, "r") as f:
        return [[char for char in line] for line in f.read().rstrip("\n").split("\n")]

# Return a string with the board rendered in a human/pichu-readable format
def printable_board(board):
    return "\n".join([ "".join(row) for row in board])

# Check if a row,col index pair is on the map
def valid_index(pos, n, m):
    return 0 <= pos[0] < n and 0 <= pos[1] < m

# Find the possible moves from position (row, col)
def moves(map, row, col):
    moves = ((row+1, col), (row-1, col), (row, col-1), (row, col+1))

    # Return only moves that are within the board and legal (i.e. go through open space ".")
    return [move for move in moves if valid_index(move, len(map), len(map[0])) and (map[move[0]][move[1]] in ".@")]

# Identifies to which direction pichu moved
def direction(curr_row, curr_col, row, col):
    if(curr_row != row):
        if curr_row > row:
            move_direction = "U"
        else:
            move_direction = "D"
    else:
        if curr_col > col:
            move_direction = "L"
        else:
            move_direction = "R"
    return move_direction


# Perform search on the map
#
# This function MUST take a single parameter as input -- the house map --
# and return a tuple of the form (move_count, move_string), where:
# - move_count is the number of moves required to navigate from start to finish, or -1
#    if no such route exists
# - move_string is a string indicating the path, consisting of U, L, R, and D characters
#    (for up, left, right, and down)
#
def search(house_map):
    # Find pichu start position
    pichu_loc=[(row_i,col_i) for col_i in range(len(house_map[0])) for row_i in range(len(house_map)) if house_map[row_i][col_i]=="p"][0]
    fringe=[(pichu_loc,"")]
    explored_loc = []
    while fringe:
        (curr_move, curr_dist)=fringe.pop()
        for move in moves(house_map, *curr_move):
            if move not in explored_loc:
                move_direction = direction(*curr_move, move[0], move[1])
                if house_map[move[0]][move[1]]=="@":
                    curr_dist = curr_dist + move_direction
                    return (len(curr_dist), curr_dist)
                else:
                    fringe = [(move, curr_dist + move_direction)] + fringe
                    explored_loc.append(move)
    return (-1, "")


# Main Function
if __name__ == "__main__":
    house_map = parse_map(sys.argv[1])
    print("Routing in this board:\n" + printable_board(house_map) + "\n")
    print("Shhhh... quiet while I navigate!")
    solution = search(house_map)
    print("Here's the solution I found:")
    print(str(solution[0]) + " " + str(solution[1]))
