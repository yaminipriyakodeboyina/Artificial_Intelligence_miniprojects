# Assignment-0

## Navigation

### Search Abstraction

1. **Initial State**:- one Pichu in its starting location, one @ and walls on the board
2. **Goal State**:- The Pichu and @ are in the same location
3. **Valid States**:- Pichu in any of the '.' location in which Pichu possibly can move to that location without walls between the path.
4. **Successor function**:- Successor function gives the next possible Pichu location either up or down or left or right if there are no walls in these locations.
5. **Cost function**:- cost function is the same for each move of Pichu and we can ignore for this problem.


### Why does the initial program failed to find a solution?

1. The initial code is using the stack to solve the problem which implies the code is using a depth-first strategy to solve the problem. This procedure takes a lot more time than Breadth-first Search to find the solution and it is not sure whatever solution we got with dfs is the optimal solution, Because the DFS algorithm is not optimal.

2. In the fringe each tuple contains Pichu location and length traveled, the fringe is not storing the path Pichu traveled.  

3. The code doesn't know which direction the Pichu is moving


### Implementation to make code work better or Explanation for the latest code.

1. Implemented Breadth-first strategy by using queue (First in First Out), So that the solution which we find is the optimal solution. In other words it will find the shallowest solution
2. In this algorithm we can neglect explored locations because that path will not bring any good to the solution, "because that path must be at least as deep as the one already found" (the line in the quote is taken from "Artificial Intelligence A Modern Approach
Third Edition book")
3. Each tuple in fringe has the model:- (Current location of Pichu, path Pichu traveled till that moment) 
4. Methods added :-
    * _direction(curr\_row, curr\_col, row, col)_ which gives the direction to which Pichu traveled.
            * if it moves right return 'R'
            * if it moves left return 'L'
            * if it moves down return 'D'
            * if it moves up return 'U'
#### Detailed explanation for the search algorithm

1. Firstly, Algorithm will find the initial position of the Pichu and store it in  "pichu_loc" and add the tuple (pichu_loc, "") to the fringe, "" because the path Pichu moved is empty initially. (line 59, 60)
2. Initialize an empty list to store explored locations. (line 61)
3. loop till fringe is empty (line 62)
4. Pop the last element from the fringe and store it in _(curr\_move, curr\_dist)_ = (current location of Pichu, the path traveled by Pichu)
5. find the successors of the poped state from the fringe, here the successor function is _moves(map, row, col)_. moves method gives all possible moves from the current location. (line 64)
6. loop through all the successors and explore the move to reach the goal state (line 64)
6. for each possible move check whether it is an explored list (line 65). if it is in the explored list leave the move and take another move from the successor function  
7. if it is not in an explored list make the Pichu move in the direction. and find the direction of the move and store in  _move\_direction_.
8. check the new location is goal state by comparing the location of @ and location of Pichu are same (line 67). if it is the goal state add the new direction to _curr\_dist_ (line 68) and return the length of _(curr\_dist)_ which gives no of steps traveled by Pichu and _curr\_dist_ which is the path traveled by Pichu.
9. if it is not the goal, add the (new location, the path traveled to reach that location) in front of the fringe because it is queue(adding front and removing last)(line70,71)
10. add the location into explored location and continue the next possible successor(line 72)
11. when fringe gets empty that means we haven't reached a solution that is there is no solution so return -1 as length traveled and empty path 


---


## Part 2: Hide and Seek

### Search Abstraction

1. **Initial State**:- one Pichu, one @ and walls on the board
2. **Goal State**:- k pichus on the board without seeing each other column and row-wise 
3. **Valid States**:- states we get by adding one Pichu in any of the '.' location on the board so that no two pichus see each other row and column-wise till the count of pichus reach k
4. **Successor function**:- Successor function gives the next possible boards by adding a Pichu to any "." so that no two pichus see each other column and row-wise
5. **Cost function**:- cost function is same for every step of adding Pichu and we can ignore for this problem.


### Implementation to make code work better or Explanation for the latest code.

 This algorithm recursively add pichus to the board so that no two pichus see each other row and column-wise till it reaches goal state that means k pichus on board

#### Newly created Methods

    1. recursive_add_k_pichu_optimized function:
        parameters:-
                * k - is the no of pichus in the goal state
                * board - board on which pichus should be added
                * limit - limit gives the number of pichus yet to be added or how deep yet algorithm should go

        * This function  recursively calls itself till it adds k-1 pichus because there is already one Pichu in the board
        * This method keeps track of explored states to avoid exploring them again
        * This method tends to go deep till kth level because there will not be any goal state till the kth level
        * line 128 check the board is goal state if it is goal state returns (board, True)
        * line 131 return (board , false) Solution does not exit it that path or subtree
        * line 133 for loop iterates for all possible state in that level till it reaches the goal
        * line 134 ignore already visited states because we already explored that subtree
        * line 135 recursively go deep into the subtree till reaches kth level
        * line 136 add the state into the explored state

    2. successors(board)
        * return all possible board which will be generated by adding a Pichu so that no two pichus see each other row or column-wise

    3. isSafe(board,row,col)
        * Checks whether (row, column) is safe to place Pichu so that no two pichus see each other row or column-wise
        * return true if safe else false

    
#### Solve function
    1. if k>0 it will go to else part and call recursive_add_k_pichu_optimized
    2. if result is true then board is goal return (board, true)
    3. else returns (empty board, false)

### Pain points
    1. method recursive_add_k_pichu takes a long time(which is possible for timeout) if there is no solution for k pichus on the board, so I ignored explored states so that it will reduce time.
    2. Ignoring Explored states greatly reduced time, but it takes more space to store explored states which is a drawback.
    3. I tried Backtracking but backtracking took more time than _recursive\_add\_k\_pichu_ 
    4. Hope recursive_add_k_pichu_optimized will not fail by out of space error.

---


##  Extra credits

### Search Abstraction

1. **Initial State**:- one Pichu, one @ and walls on the board
2. **Goal State**:- maximum pichus on the board without seeing each other column and row and diagonal wise 
3. **Valid States**:- states we get by adding one Pichu in any of the '.' location on the board, so that no two pichus see each other row, column, and diagonal wise
4. **Successor function**:- Successor function gives next possible boards by adding a Pichu to any "." so that no two pichus see each other column and row and diagonal wise
5. **Cost function**:- cost function is same for every step of adding pichu and we can ignore for this problem.


### Implementation to make code work better or Explanation for the latest code.

 This algorithm recursively add pichus to the board so that no two pichus see each other row and column and diagonal wise till it reaches goal state that means maximum no of  pichus on board

#### Newly created Methods

    1. recursive_add_max_pichu_optimized function:
        parameters:-
                * k - is the no of pichus in the goal state
                * board - board on which pichus should be added
                * limit - limit gives the number of pichus yet to be added or how deep yet algorithm should go

        * This function adds recursively calls itself till it adds k-1 pichus because there is already one Pichu in the board
        * This method keeps track of explored states to avoid exploring them again
        * This method tends to go deep till kth level because there will not be any goal state till the kth level
        * line 157 check the board is goal state if it is goal state returns (board, True)
        * line 159 return (board, false) Solution does not exit it that path or subtree
        * line 162 for loop iterates for all possible state in that level till it reaches the goal
        * line 163 ignore already visited states because we already explored that subtree
        * line 164 recursively go deep into the subtree till reaches kth level
        * line 165 add the state into the explored state

    2. successors_max_pichu(board) 
        * return all possible board which will be generated by adding a Pichu so that no two pichus see each other row or column or diagonal wise

    3. isSafe(board,row,col)
        * Checks whether (row, column) is safe to place Pichu so that no two pichus see each other row or column-wise
        * return true if safe else false
       
    4. isSafe_max_pichu
        * check whether (row, column) is safe to add Pichu so that no two pichus see each other row or column or diagonal wise
    
#### Solve function
    1. if k = 0 it will assign preresult with (initial board, True) because already a Pichu exists on the board k==1 is success
    2. So algorithm starts from k=2 
    3. line 197 it will loop by incrementing k till the algorithm doesn't find the solution for k
    4. Once the recursive_add_max_pichu_optimized returns false at k the algorithm returns the last successful goal state which is stored in preresult and maximum pichus possing is k-1

### Pain points
    1. method recursive_add_max_pichu_takes a long time(which is possible for timeout) if there is no solution for k pichus on the board 
    so I ignored explored states so that it will reduce time.
    2. Ignoring Explored states greatly reduced time, but it takes more space to store explored states which is a drawback.
    3. I tried Backtracking but backtracking took more time than recursive_add_max_pichu 
    4. Hope  recursive_add_max_pichu_optimized will not fail by out of space error.

Please feel free to give suggestions :)


