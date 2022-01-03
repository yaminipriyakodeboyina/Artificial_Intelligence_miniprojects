#
# pikachu.py : Play the game of Pikachu
#
# PLEASE PUT YOUR NAMES AND USER IDS HERE!
#
# Based on skeleton code by D. Crandall, March 2021
#
import sys
import time

def board_to_string(board, N):
    return "\n".join(board[i:i+N] for i in range(0, len(board), N))

def get_anti_side(side):
    if(side == 'b'):
        anti_side='w'
    else:
        anti_side='b'
    return anti_side

def pichu_moves(board,row,col,side):
    succ=[]
    anti_side=get_anti_side(side)

    #  col+1 step right
    if col+1<len(board[0])  and board[row][col+1]=='.':
        succ.append(board[0:row]+ [board[row][0:col] + ['.',]+ [side,]+board[row][col+2:] ]+board[row+1:])
    elif col+2<len(board[0]) and board[row][col+1].lower() == anti_side and board[row][col+2]=='.':
        succ.append(board[0:row]+[board[row][0:col]+['.','.',side]+board[row][col+3:]]+board[row+1:])

    # col-1
    if col-1>-1 and board[row][col-1]=='.':
        succ.append(board[0:row]+ [board[row][0:col-1] + [side,]+['.',]+board[row][col+1:] ]+board[row+1:])
    elif col-2>-1 and board[row][col-1].lower() == anti_side and board[row][col-2]=='.':
        succ.append(board[0:row]+[board[row][0:col-2]+[side,'.','.']+board[row][col+1:]]+board[row+1:])
    
    # row+1
    if side=='w' and row+1<len(board) and board[row+1][col]=='.':
        if row+1 == len(board)-1:
            succ.append(board[0:row]+ [board[row][0:col] +['.',]+board[row][col+1:] ]+[board[row+1][0:col] +[side.upper(),]+board[row+1][col+1:]]+board[row+2:])
        else:
            succ.append(board[0:row]+ [board[row][0:col] +['.',]+board[row][col+1:] ]+[board[row+1][0:col] +[side,]+board[row+1][col+1:] ]+board[row+2:])
    elif side=='w' and row+2<len(board) and board[row+1][col].lower() == anti_side and board[row+2][col]=='.':
        if row+2 == len(board)-1:
            succ.append(board[0:row]+[board[row][0:col] +['.',]+board[row][col+1:] ]+[board[row+1][0:col] +['.',]+board[row+1][col+1:]]+[board[row+2][0:col] +[side.upper(),]+board[row+2][col+1:]]+board[row+3:])
        else:
            succ.append(board[0:row]+[board[row][0:col] +['.',]+board[row][col+1:] ]+[board[row+1][0:col] +['.',]+board[row+1][col+1:]]+[board[row+2][0:col] +[side,]+board[row+2][col+1:]]+board[row+3:])

    #row-1
    if side=='b' and row-1>-1 and board[row-1][col]=='.':
        if(row-1==0):
            succ.append(board[0:row-1]+ [board[row-1][0:col] +[side.upper(),]+board[row-1][col+1:] ]+[board[row][0:col] +['.',]+board[row][col+1:] ]+board[row+1:])
        else:
            succ.append(board[0:row-1]+ [board[row-1][0:col] +[side,]+board[row-1][col+1:] ]+[board[row][0:col] +['.',]+board[row][col+1:] ]+board[row+1:])

    elif side=='b' and row-2>-1 and board[row-1][col].lower() == anti_side and board[row-2][col]=='.':
        if(row-2 ==0):
            succ.append(board[0:row-2]+[board[row-2][0:col] +[side.upper(),]+board[row-2][col+1:] ]+[board[row-1][0:col] +['.',]+board[row-1][col+1:]]+[board[row][0:col] +['.',]+board[row][col+1:]]+board[row+1:])
        else:
            succ.append(board[0:row-2]+[board[row-2][0:col] +[side,]+board[row-2][col+1:] ]+[board[row-1][0:col] +['.',]+board[row-1][col+1:]]+[board[row][0:col] +['.',]+board[row][col+1:]]+board[row+1:])
    
    return succ

def get_the_right_succ(board,row,col,side):
    succ=[]
    anti_side=get_anti_side(side)

    #  right direction
    j=col+1
    while(j<len(board[0])):
        if board[row][j] !='.':
            break
        j=j+1
    # jump to empty boxes
    for i in range(col+1,j):
        succ.append(board[0:row]+ [board[row][0:col] + ['.',]+board[row][col+1:i]+ [side.upper(),]+board[row][i+1:] ]+board[row+1:])
    # jump over opp team to empty boxes
    if j<len(board[0]) and board[row][j].lower() == anti_side:
        jump=j+1
        while(jump<len(board[0])):
            if board[row][jump] !='.':
                break
            jump=jump+1
            # jump to empty boxes
        for i in range(j+1,jump):
            succ.append(board[0:row]+ [board[row][0:col] + ['.',]+board[row][col+1:j]+['.',]+board[row][j+1:i]+ [side.upper(),]+board[row][i+1:] ]+board[row+1:])
    return succ



def get_the_left_succ(board,row,col,side):
    succ=[]
    anti_side=get_anti_side(side)
    # left direction
    j=col-1
    while(j>-1):
        if board[row][j] !='.':
            break
        j=j-1
    # jump to empty boxes
    for i in range(col-1,j,-1):
        succ.append(board[0:row]+ [board[row][0:i] + [side.upper(),]+board[row][i+1:col]+ ['.',]+board[row][col+1:] ]+board[row+1:])
    # jump over opp team to empty boxes
    if j>-1 and board[row][j].lower() == anti_side:
        jump=j-1
        while(jump>-1):
            if board[row][jump] !='.':
                break
            jump=jump-1
        # jump to empty boxes
        for i in range(j-1,jump,-1):
            succ.append(board[0:row]+ [board[row][0:i] + [side.upper(),]+board[row][i+1:j]+['.',]+board[row][j+1:col]+ ['.',]+board[row][col+1:] ]+board[row+1:])
    return succ
    # down di

def get_the_down_succ(board,row,col,side):
    board_transpose = list(map(list, zip(*board)))
    temp=row
    row=col
    col=temp
    succ=[]
    board_succ=[]
    anti_side=get_anti_side(side)

    
    #  right direction
    
    j=col+1
    while(j<len(board_transpose[0])):
        if board_transpose[row][j] !='.':
            break
        j=j+1
    # jump to empty boxes
    for i in range(col+1,j):
        board_succ=board_transpose[0:row]+ [board_transpose[row][0:col] + ['.',]+board_transpose[row][col+1:i]+ [side.upper(),]+board_transpose[row][i+1:] ]+board_transpose[row+1:]
        succ.append(list(map(list, zip(*board_succ))))
    # jump over opp team to empty boxes
    if j<len(board_transpose[0]) and board_transpose[row][j].lower() == anti_side:
        jump=j+1
        while(jump<len(board_transpose[0])):
            if board_transpose[row][jump] !='.':
                break
            jump=jump+1
            # jump to empty boxes
        for i in range(j+1,jump):
            board_succ=board_transpose[0:row]+ [board_transpose[row][0:col] + ['.',]+board_transpose[row][col+1:j]+['.',]+board_transpose[row][j+1:i]+ [side.upper(),]+board_transpose[row][i+1:] ]+board_transpose[row+1:]
            succ.append(list(map(list, zip(*board_succ))))
    return succ

def get_the_up_succ(board,row,col,side):
    board_transpose = list(map(list, zip(*board)))
    temp=row
    row=col
    col=temp
    succ=[]
    board_succ=[]
    anti_side=get_anti_side(side)
    # left direction
    j=col-1
    while(j>-1):
        if board_transpose[row][j] !='.':
            break
        j=j-1
    # jump to empty boxes
    for i in range(col-1,j,-1):
        board_succ=board_transpose[0:row]+ [board_transpose[row][0:i] + [side.upper(),]+board_transpose[row][i+1:col]+ ['.',]+board_transpose[row][col+1:] ]+board_transpose[row+1:]
        succ.append(list(map(list, zip(*board_succ))))
    # jump over opp team to empty boxes
    if j>-1 and board_transpose[row][j].lower() == anti_side:
        jump=j-1
        while(jump>-1):
            if board_transpose[row][jump] !='.':
                break
            jump=jump-1
        # jump to empty boxes
        for i in range(j-1,jump,-1):
            board_succ=board_transpose[0:row]+ [board_transpose[row][0:i] + [side.upper(),]+board_transpose[row][i+1:j]+['.',]+board_transpose[row][j+1:col]+ ['.',]+board_transpose[row][col+1:] ]+board_transpose[row+1:]
            succ.append(list(map(list, zip(*board_succ))))
    return succ



def pikachu_moves(board,i,j,side):
    s=[]
    s.extend(get_the_down_succ(board,i,j,side))
    s.extend(get_the_up_succ(board,i,j,side))
    s.extend(get_the_right_succ(board,i,j,side))
    s.extend(get_the_left_succ(board,i,j,side))
    return s

        
def evaluation_function(board,side):
    anti_side=get_anti_side(side)
    l=len(board)
    count_side_pichu =sum([row.count(side) for row in board])
    count_side_pikachu =sum([row.count(side.upper()) for row in board])
    count_anti_side_pichu =sum([row.count(anti_side) for row in board])
    count_anti_side_pikachu =sum([row.count(anti_side.upper()) for row in board])
    max=(1*count_side_pichu)+(l*count_side_pikachu)
    min=(1*count_anti_side_pichu)+(l*count_anti_side_pikachu)
    return max-min

def isTerminal(board,side):
    count_side =sum([row.count(side)+row.count(side.upper()) for row in board])
    if(count_side==0):
        return True
    return False
    
    # count_anti_side =sum([row.count(anti_side)+row.count(anti_side.upper()) for row in board])
    # if count_side == 0 and count_anti_side ==0 :
    #     return 0
    # elif count_anti_side == 0:
    #     return 1
    # else:
    #     return -1
    

    # -------------alpha,beta pruning----------------

def max_value_alphabeta(board,side,h,alpha,beta):
    anti_side=get_anti_side(side)
    if isTerminal(board,side):
        # return -100
        return evaluation_function(board,side)
    elif h==0:
        return evaluation_function(board,side)
    else:
        # return(max([min_value(succ,side,h-1) for succ in successor(board,side)]))
        for succ in successor(board,side):
            alpha=max(alpha,min_value_alphabeta(succ,side,h-1,alpha,beta))
            if(alpha>=beta):
                return alpha
        return alpha


    

def min_value_alphabeta(board,side,h,alpha,beta):
    anti_side=get_anti_side(side)
    if isTerminal(board,anti_side):
        # return 100
        return evaluation_function(board,side)
    elif h==0:
        return evaluation_function(board,side)
    else:
        # return(min([max_value(succ,anti_side,h-1) for succ in successor(board,side)]))
        for succ in successor(board,anti_side):
            beta=min(beta,max_value_alphabeta(succ,side,h-1,alpha,beta))
            if(alpha>=beta):
                return beta
        return beta


    # -----------------------------------------------------





def max_value(board,side,h):
    anti_side=get_anti_side(side)
    if isTerminal(board,side):
        # re turn -100
        return evaluation_function(board,side)
    elif h==0:
        return evaluation_function(board,side)
    else:
        k=successor(board,side)
        if(len(k)==0):
            return evaluation_function(board,side)
        return(max([min_value(succ,side,h-1) for succ in k]))

def min_value(board,side,h):
    anti_side=get_anti_side(side)
    if isTerminal(board,anti_side):
        # return 100
        return evaluation_function(board,side)
    elif h==0:
        return evaluation_function(board,side)
    else:
        k=successor(board,side)
        if(len(k)==0):
            return evaluation_function(board,side)
        return(min([max_value(succ,anti_side,h-1) for succ in k]))


def display(board):
    return ''.join(str(item) for row in board for item in row)

def min_max(board,side,h):
    max_value= -sys.maxsize
    max_state=[]
    anti_side=get_anti_side(side)
    # k=[[min_value(succ,side,h),succ] for succ in successor(board,side)]
    # (value,state)=max(k)
    # return state
    for succ in successor(board,side):
        value=min_value(succ,side,h)
        if(max_value<value):
            # yield display(succ)
            max_value=value
            max_state=succ
    state = display(max_state)
    return max_state





def successor(board,side):
    succ=[]
    # keep pikachu moves first
    for i in range(0,len(board)):
        for j in range(0,len(board[0])): 
            if board[i][j] == side:
                succ.extend(pichu_moves(board,i,j, side))
            elif board[i][j].isupper() and board[i][j].lower() == side:
                succ.extend(pikachu_moves(board,i,j,side))
    return succ


def find_best_move(board, N, player, timelimit):
    # This sample code just returns the same board over and over again (which
    # isn't a valid move anyway.) Replace this with your code!
    #
    k=0
    board1=[]
    for i in range(0,len(board),N):
        board1.append([board[j] for j in range(i,i+N)])
    # for r in successor(board1,player):
    #      print(r)
    # print(min_max(board1,player,7))
    # ------------------------------------------------------------------------------------
    # max_value= -sys.maxsize
    # max_state=[]
    # anti_side=get_anti_side(player)
    # # k=[[min_value(succ,side,h),succ] for succ in successor(board,side)]
    # # (value,state)=max(k)
    # # return state
    # h=2
    # while(True):
    #     # print(h)
    #     max_value= -sys.maxsize
    #     anti_side=get_anti_side(player)
    #     for succ in successor(board1,player):
    #         value=min_value(succ,player,h)
    #         print(display(succ)+str(value))
    #         if(max_value<value):
    #             max_value=value
    #             # print(succ)
    #             # yield display(succ)+str(max_value)
    #             # max_value=value
    #             max_state=succ
    #     h=h+1
    #     yield display(max_state)
    # -------------------------------------alpha-beta---------------------------------------------------

    # max_value= -sys.maxsize
    # anti_side=get_anti_side(player)
    # k=[[min_value(succ,side,h),succ] for succ in successor(board,side)]
    # (value,state)=max(k)
    # return state
    h=2
    while(True):
        # print(h)
        max_value= -sys.maxsize
        anti_side=get_anti_side(player)
        for succ in successor(board1,player):
            value=min_value_alphabeta(succ,player,h,-sys.maxsize,sys.maxsize)
            # print(display(succ)+str(value))
            # value=min_value_alphabeta(succ,player,-sys.maxsize,sys.maxsize)
            if(max_value<value):
                max_value=value
                # print(succ)
                # yield display(succ)
                # max_value=value
                max_state=succ
        # print(h)
        h=h+1
        yield display(max_state)



    # ---------------------------------------------------------------------------------------------
    # while True:
    #     time.sleep(1)
    #     yield board


if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise Exception("Usage: pikachu.py N player board timelimit")
        
    (_, N, player, board, timelimit) = sys.argv
    N=int(N)
    timelimit=int(timelimit)
    if player not in "wb":
        raise Exception("Invalid player.")

    if len(board) != N*N or 0 in [c in "wb.WB" for c in board]:
        raise Exception("Bad board string.")

    print("Searching for best move for " + player + " from board state: \n" + board_to_string(board, N))
    print("Here's what I decided:")
    for new_board in find_best_move(board, N, player, timelimit):
    # for new_board in find_best_move(".........wwwwwwwwwwwww.ww.....w.......b.........................", 8, 'b', 10):
        print(new_board)
