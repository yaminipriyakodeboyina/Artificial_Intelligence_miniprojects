# a2

 (1) a description of how you formulated each problem; (2) a brief description of how your program works; (3) and discussion of any problems you faced, any assumptions, simplifications, and/or design decisions you made.

 ## Part1

### Design

Get the initial state from the input.
Evaluation function is know how to good is a state to select.
Used MinMax algorithm. Max node take max of min values of min nodes and min nodes take minimum value of max values of max nodes 
I used alpha beta pruning to reduce time it takes to search the tree
The algorithm searche to depth 2 at first iteration and increases the depth as to 3,4,5 ...
every iterartion displays the result once it is fully completed

### Assumption
    evaluation function is calculated as 
        score=no.of player pichu+ N(no of player pikachu) - no.of other player pichu+ N(no of other player pikachu)
        N= length of board


## Part2

    1.role the dice, calculated which subset of dice to roll by calculating expected value of every possible subset of dice roll.
    2.Score as assigned similar in question.
        1.Premis, secundus, tertium,Quartus,Quintus,Sextus will have bonus if they are added upto or more than 63
        2.so I gave more preference to Premis, secundus, tertium,Quartus,Quintus,Sextus to add upto 63 and removed the preference once added to 63
        3.if I have to get 63 atleast each roll of that category should have 3 or more value on the dice.
            3+6+9+12+15+18=63
    3. I sacrificed least probability categories to 0 to get the bonus 35
    I gave preference in order Premis, secundus, tertium,Quartus,Quintus,Sextus to get 35

    Average value comes around 220


## part3

calculated probability 0f a tweet is Eastcoast(A) and Westcoast(B)
P(A) and P(B) is calculated

1. calculated total distict words in in train document. total words in in setences belong to class A and B
2. for every word in sentence calculated the condition probability of using train data bu using formula

1st approach
P(word/A)=|word intersection A|/|A|
|word intersection A| :- no of times word occur in class A
|A| -Total no of words on class A
calculated P(word/B) in same way

Later used:-
used the laplace smoothing with value 1 as few of the words in train data are not present in either one of the classes A and B in train data

calculated percentage using e^log to eliminatate in accuracy when multiplying two probabilites
    p1*p2=e**(log((p1)+log(p2)))

P(A|w1,w2,...,wn)/P (B|w1, w2, ..., wn)>1 then it is Eastcoast which is classA else it is westcoast classB











