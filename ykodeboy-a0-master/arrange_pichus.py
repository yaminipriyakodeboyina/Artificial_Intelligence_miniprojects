#!/usr/local/bin/python3
#
# arrange_pichus.py : arrange agents on a grid, avoiding conflicts
#
# Submitted by : Name: Yamini Priya Kodeboyina Username: ykodeboy 
#
# Based on skeleton code in CSCI B551, Spring 2021
#


import sys

# Parse the map from a given filename
def parse_map(filename):
	with open(filename, "r") as f:
		return [[char for char in line] for line in f.read().rstrip("\n").split("\n")]

# Count total # of pichus on board
def count_pichus(board):
    return sum([ row.count('p') for row in board ] )

# Return a string with the board rendered in a human-pichuly format
def printable_board(board):
    return "\n".join([ "".join(row) for row in board])

# Add a pichu to the board at the given position, and return a new board (doesn't change original)
def add_pichu(board, row, col):
    return board[0:row] + [board[row][0:col] + ['p',] + board[row][col+1:]] + board[row+1:]
    
# Checks whether the location is safe to place pichu, it make sure that no two agents can see one another rows and column wise
def isSafe(board,row,col):
    for r in range(row+1, len(board)):
        if board[r][col] == "X" or board[r][col] == "@":
            break
        elif board[r][col] == "p":
            return False
    
    for r in range(row-1, -1,-1):
        if board[r][col] == "X" or board[r][col] == "@":
            break
        elif board[r][col] == "p":
            return False

    for r in range(col+1, len(board[0])):
        if board[row][r] == "X" or board[row][r] == "@":
            break
        elif board[row][r] == "p":
            return False
    
    for r in range(col-1, -1,-1):
        if board[row][r] == "X" or board[row][r] == "@":
            break
        elif board[row][r] == "p":
            return False
    return True


# Checks whether the location is safe to place pichu, it make sure that no two agents can see one another rows and column and diagonal wise
def isSafe_max_pichu(board,row,col):

    result=isSafe(board,row,col) 
    if result == False:
        return False
      
    r= row+1
    c=col+1
    while r<len(board) and c<len(board[0]): 
        if board[r][c] == "X" or board[r][col] == "@":
            break
        elif board[r][c] == "p":
                return False
        else:
            r=r+1
            c=c+1

    r= row-1
    c= col+1
    while r > -1 and c<len(board[0]): 
        if board[r][c] == "X" or board[r][col] == "@":
            break
        elif board[r][c] == "p":
                return False
        else:
            r=r-1
            c=c+1

    r= row-1
    c= col-1
    while r > -1 and c > -1: 
        if board[r][c] == "X" or board[r][col] == "@":
            break
        elif board[r][c] == "p":
                return False
        else:
            r=r-1
            c=c-1

    r= row+1
    c= col-1
    while r < len(board) and c > -1: 
        if board[r][c] == "X" or board[r][col] == "@":
            break
        elif board[r][c] == "p":
                return False
        else:
            r=r+1
            c=c-1

    return True



# Get list of successors of given board state, where pichu is placed so that no two pichus see one another in row and column wise
def successors(board):
    return [ add_pichu(board, r, c) for r in range(0, len(board)) for c in range(0,len(board[0])) if board[r][c] == '.' and isSafe(board,r,c) ]

# Get list of successors of given board state, where pichu is placed so that no two pichus see one another in row and column diagonal wise
def successors_max_pichu(board):
    return [ add_pichu(board, r, c) for r in range(0, len(board)) for c in range(0,len(board[0])) if board[r][c] == '.' and isSafe_max_pichu(board,r,c) ]


# check if board is a goal state
def is_goal(board, k):
    return count_pichus(board) == k 

# Function to add k pichus to reach the goal state. Using Depth first strategy
def recursive_add_k_pichu_optimized(board, limit,k,explored):
    if is_goal(board, k):
        return(board, True)
    elif limit == 0:
        return (board, False)
    else:
        for s in successors(board):
            if s not in explored:
                result = recursive_add_k_pichu_optimized(s, limit-1,k,explored)
                explored.append(s)
                if(result[1] == True):
                    return result
        return(board,False)

# def recursive_add_k_pichu(board, limit,k):
#     if is_goal(board, k):
#         return(board, True)
#     elif limit == 0:
#         return (board, False)
#     else:
#         for s in successors(board):
#             result = recursive_add_k_pichu(s, limit-1,k)
#             if(result[1] == True):
#                 return result
#         return(board,False)



# Function to find maximum number of pichus that can be added with no agent seeing each other row, column and diagonaly. Using Depth first strategy
def recursive_add_max_pichu_optimized(board, limit,k,explored):
    if is_goal(board, k):
        return(board, True)
    elif limit == 0:
        return (board, False)
    else:
        for s in successors_max_pichu(board):
            if s not in explored:
                result = recursive_add_max_pichu_optimized(s, limit-1,k,explored)
                explored.append(s)
                if(result[1] == True):
                    return result
        return(board,False)


# This Function is only for reference
# def recursive_add_max_pichu(board, limit,k):
#     if is_goal(board, k):
#         return(board, True)
#     elif limit == 0:
#         return (board, False)
#     else:
#         for s in successors_max_pichu(board):
#             result = recursive_add_max_pichu(s, limit-1,k)
#             if(result[1] == True):
#                  return result
#         return(board,False)


    
# Arrange agents on the map
#
# This function MUST take two parameters as input -- the house map and the value k --
# and return a tuple of the form (new_map, success), where:
# - new_map is a new version of the map with k agents,
# - success is True if a solution was found, and False otherwise.
#
def solve(initial_board, k):
    if k==0:
        preResult =(initial_board,True)
        k=2
        while True:
            explored =[]
            result = recursive_add_max_pichu_optimized(initial_board, k-1,k,explored)
            #result =  recursive_add_max_pichu(initial_board, k-1, k)
            if result[1] == True:
                preResult=result
                k=k+1
            else:
                return preResult
    else:
        explored=[]
        result = recursive_add_k_pichu_optimized(initial_board, k-1,k,explored)
        #result= recursive_add_k_pichu(initial_board, k-1,k)
        if(result[1] == True):
            return result
        return ([],False)

# Main Function
if __name__ == "__main__":
    house_map=parse_map(sys.argv[1])

    # This is K, the number of agents
    k = int(sys.argv[2])
    print ("Starting from initial board:\n" + printable_board(house_map) + "\n\nLooking for solution...\n")
    (newboard, success) = solve(house_map, k)
    print ("Here's what we found:")
    print (printable_board(newboard) if success else "None")


