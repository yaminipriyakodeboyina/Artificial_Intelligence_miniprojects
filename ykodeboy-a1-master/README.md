# a1

## Part 1


    State Space:- Any posssible board
    Goal State: The Goal state for this problem is continuous arrangement of numbers from 1 to 20 in the form [[1,2,3,4,5],[6,7,8,9,10],[11,12,13,14,15],[16,17,18,19,20]] in the fewest possible number of possible moves.
    Edge weights: The edge weights for any move for this problem is constant as the cost function function increases by only one no matter which possible step we take.
    Successor function:- The successor function gives the set of all possible states that can be obtained when the successor function is applied to the current state, by moving 
			the respective row or column pertaining to the given constraints:sliding the first and third rows to the left only and the second and fourth rows to the right only and first,third and fifth columns can only be slid up and by sliding second and fourth columns to the down.

    keep the intial board in fringe
    pop the min cost value in fringe
    get the successors for the poped out state and calculate cost and appened them to fringe til we get goal state.
    we are not visiting the already visited staes if there cost function is more than existing cost function of that state

    heuristic :- sum of manhattan distance of each element in a row and dividing it by 5 as there are 5 elements in row. + sum of manhattan distance for each element in column and dividing it by 4 as there are 4 elements in column.
    
    cost function: 1+h(x)




## Part 2
    initial state:- Initial start city
    state space:- all the cities and junctions are part of state space 
    Successor function:- all the connected cities for the current state
    goal state:- current nodes as end city
    
    Heuristic:
        distance:
            Haversine distance between the nodes. edge cost as distance between nodes given in road-segment.txt
        Time:
            Haversne distance/max speed limit .Max speed limt of all states because it make the heuristic admissible. it never over estimates the heuristic value of time. edge cost as the length of the connecting road/speed limit of the connecting route.
        Safe:
            edge cost id the length of the connecting road multipled by the accident probability of the road. heuristic is 0 as it never overestimates
        segment:
            Heuristic is the haversine distance/max segement length of  all roads so heuristic never over estimates. edge weight is is 1.
    
    Procedure:
        keep the initial state into the fringe. 
            check for goal state. if goal display
            take min from fringe calculates cost by edge weight+heuristic values and append them to fringe
            we are not visiting the already visited states if their cost is greater than exixting cost of that state. (optimised the code to great level)
        

    heuristic for the junction nodes is taken as 0

## Part 3
    Initial state:- Initial state is no  student assigned to any group
    statespace: combination of the groups in a way that satisfies the preferences of student selected randomnly.(optimised the code to great level)
    Cost function:- calculating the total complaints of that particular group.
    Successor function:- randomn select a student and get all possible groups which satisfies his prefence
    goal state:- list of stuident groups with least complaints

    Procedure:
        keep the initial state into the fringe. 
            check for goal state. if goal display
            take min from fringe calculates cost using cost function  and append them to fringe
            we are not visiting the already visited states if their cost is greater than existing cost of that state. (By using this idea we are getting results quicker)



            
        



