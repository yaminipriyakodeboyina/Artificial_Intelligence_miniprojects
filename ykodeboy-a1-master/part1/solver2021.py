#!/usr/local/bin/python3
# solver2021.py : 2021 Sliding tile puzzle solver
#
# Code by: name IU ID
#
# Based on skeleton code by D. Crandall, January 2021
#

import sys

ROWS=4
COLS=5

def printable_board(board):
    return [ ('%3d ')*COLS  % board[j:(j+COLS)] for j in range(0, ROWS*COLS, COLS) ]



def rotate_right(state,n):
    d= state[0:n]+[state[n][-1:]+state[n][:-1]]+state[n+1:]
    return d

def rotate_left(state,n):
    return state[0:n]+[state[n][1:]+state[n][:1]]+state[n+1:]

def rotate_down(state,n):
    l=rotate_right(list(map(list, zip(*state))),n)
    return list(map(list, zip(*l)))

def rotate_up(state, n):
    l= rotate_left(list(map(list, zip(*state))),n)
    return list(map(list, zip(*l)))
    

# return a list of possible successor states
def successors(state):
     return [(rotate_left(state,0),'L1'),(rotate_left(state,2),'L3'),(rotate_right(state,1),'R2'),(rotate_right(state,3),'R4'),(rotate_up(state,0),'U1'),(rotate_up(state,2),'U3'),(rotate_up(state,4),'U5'),(rotate_down(state,1),'D2'),(rotate_down(state,3),'D4')]
    

# check if we've reached the goal
def is_goal(state):
    l=list(list(i for i in range(n+1,n+6)) for n in range(0,20,5))
    if(state == l):
        return True
    return False

def h(state):
   
    cost=0
    for i in range(0,4):
        c=0
        for j in range(0,5):
            value= state[i][j]
            original_row= (value-1)//5
            
            original_column= (value-1)%5
            if(j!=original_column):
                # if(i==1 or i==3):
                if(original_row==1 or original_row==3):
                    if(original_column>j):
                        c=c+abs(original_column-j)
                    elif(original_column<j):
                        c=c+5-abs(original_column-j)
                # elif(i==0 or i==2):
                elif(original_row==0 or original_row==2):
                    if(original_column<j):
                        c=c+abs(original_column-j)
                    elif(original_column>j):
                        c=c+5-abs(original_column-j)
        # cost=cost+(c//5)+(c%5)
        cost=cost+(c/5)

    for j in range(0,5):
        c=0
        for i in range(0,4):
            value= state[i][j]
            original_row= (value-1)//5
            original_column= (value-1)%5
            if i!= original_row:
                # if(j==0 or j==2 or j==4):
                if(original_column==0 or original_column==2 or original_column==4):
                        if(original_row<i):
                            c=c+abs(original_row-i)
                        elif(original_row>i):
                            c=c+4-abs(original_row-i)
                # elif(j==1 or j==3):
                elif(original_column==1 or original_column==3):
                    if(original_row>i):
                        c=c+abs(original_row-i)
                    elif(original_row<i):
                        c=c+4-abs(original_row-j)
        # cost=cost+(c//4)+(c%4)
        cost=cost+(c/4)
    return cost
                
# def h(state):
#     return 0

def solve(initial_board):
    """
    1. This function should return the solution as instructed in assignment, consisting of a list of moves like ["R2","D2","U1"].
    2. Do not add any extra parameters to the solve() function, or it will break our grading and testing code.
       For testing we will call this function with single argument(initial_board) and it should return 
       the solution.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """
    fringe=[]
    visited=[]
    c=list(list(initial_board[n:n+5]) for n in range(0,len(initial_board),5))
    fringe += [(0,c, []),]
    while len(fringe) > 0:
        (value,state,path)=min(fringe)
        index=fringe.index((value,state,path))
        (value1,state1,path1)=fringe.pop(index)
        if is_goal(state):
            return path

        for s in successors(state):
            # visited=0
            if(s[0] not in visited):
                visited.append(s[0])
                f=value+1+h(s[0])
                # for l in visited:
                #     if s[0]==l[0]:
                #         visited=1
                #         visited_value=l[1]
                #     break
                # if visited==0 or f<visited_value:
                #     if visited ==1:
                #         l[1]=f
                fringe.append((f,s[0],path+[s[1],]))
    return []


# Please don't modify anything below this line
#
if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected a board filename"))

    start_state = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            start_state += [ int(i) for i in line.split() ]

    if len(start_state) != ROWS*COLS:
        raise(Exception("Error: couldn't parse start state file"))

    print("Start state: \n" +"\n".join(printable_board(tuple(start_state))))

    print("Solving...")
    route = solve(tuple(start_state))
    
    print("Solution found in " + str(len(route)) + " moves:" + "\n" + " ".join(route))
