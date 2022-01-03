#!/usr/local/bin/python3
# assign.py : Assign people to teams
#
# Code by: name IU ID
#
# Based on skeleton code by R. Shah and D. Crandall, January 2021
#

import sys
import time
import itertools
import random

def parse_map(filename):
    with open(filename, "r") as f:
        return [[s for s in line.split()] for line in f]

def data_student(input_file):
    d=parse_map(input_file)
    s={}
    for l in d:
        s[l[0]]= list()
        s[l[0]].extend([l[1],l[2]])
    return s

def student_friends(students_data,name):
    frnds= students_data[name][0]
    l=frnds.split('-')
    return l
def student_enemy(students_data,name):
    ene= students_data[name][1]
    l=ene.split(',')
    if '_' in l:
        l.remove('_')
    return l

def get_group_list(group_list,new,new_frnd):
    personlist=[]
    if(new==1 and len(new_frnd)>=1):
        if(len(group_list)>1):
            products = list(itertools.product([group_list], new_frnd))
            for l in products:
                g=[]
                g.extend([l[0][0],l[0][1],l[1]])
                personlist.append(g)
        else:
            products = list(itertools.product(group_list, new_frnd))
            for l in products:
                g=[]
                g.append(l[0])
                g.append(l[1])
                personlist.append(g)
    elif(new==2 and len(new_frnd)>=2):
        permutations = list(itertools.combinations(new_frnd, 2))
        products = list(itertools.product(list(group_list), permutations))
        #personlist=[]
        for l in products:
            g=[]
            g.append(l[0])
            g.extend([l[1][0],l[1][1]])
        personlist.append(g)
    elif(new==2 and len(new_frnd)==1):
        g=[]
        #personlist=[]
        g.extend(group_list)
        g.extend(new_frnd)
        personlist.append(g)
    elif(len(new_frnd)==0):
        #personlist=[]
        personlist.append(group_list)
    return personlist



def successor(students,state,students_data):
    selected_students=[]
    for l in state:
        selected_students.extend(l)
    remain=[]
    k=[]
    groups=[]
    #remaining students
    for s in students:
        if s not in selected_students:
            remain.append(s)
    k.append(random.choice(remain))
    remain.pop(remain.index(k[0]))

    #WANTS TO BE GROUP
    group_list=[]
    student_frnd= student_friends(students_data,k[0])
    student_ene = student_enemy(students_data,k[0])
    group_list.append(k[0])
    student_frnd.remove(k[0])
    new_frnd= remain.copy()
    new=0
    for fr in student_frnd:
        if(fr in remain):
            group_list.append(fr)
            new_frnd.remove(fr)
        else:
            new=new+1
    #--------------
    for i in student_ene:
        if i in new_frnd:
            new_frnd.remove(i)
    #--------------
    if new > 0:
        groups=get_group_list(group_list, new,new_frnd)
    else:
        groups.append(list(student_friends(students_data,k[0])))
    return groups

# def successor(students,state):
#     selected_students=[]
#     for l in state:
#         selected_students.extend(l)
#     remain=[]
#     k=[]
#     groups=[]
#     for s in students:
#         if s not in selected_students:
#             remain.append(s)
#     k.append(random.choice(remain))
#     remain.pop(remain.index(k[0]))

#     #one person
#     groups.append(k)

#     #two persons
#     #permutations = list(list(itertools.permutations(remain, 2)))
#     products = list(itertools.product(k, remain))
#     two_personlist=[]
#     for l in products:
#         two_personlist.append([l[0],l[1]])
#     groups.extend(two_personlist)

#     #three persons
#     permutations = list(itertools.combinations(remain, 2))
#     # two_personlist=[]
#     # for l in permutations:
#     #     two_personlist.append([l[0],l[1]])
#     three_person=[]
#     products = list(itertools.product(k,permutations))
#     for l in products:
#         three_person.append([l[0],l[1][0],l[1][1]])
#     groups.extend(three_person)

#     return groups


def get_cost(s,value,students_data):
    cost=0
    for i in s:
        l=students_data[i][0].split('-')
        if(len(s)!=len(l)):
            cost=cost+1
        for each_student in l:
            if((each_student != 'zzz') and (each_student not in s)):
                cost=cost+1
        nl=students_data[i][1].split(',')
        if(nl[0]!="_"):
            for each_student in nl:
                if each_student in s:
                    cost=cost+2
    return cost+value

def is_goal(path,students):
    selected_students=[]
    for s in path:
        selected_students.extend(s)
    for each_student in students:
        if each_student not in selected_students:
            return False
    return True

    
def selected_students(state):
    selected=[]
    for k in state:
        selected.extend(k)
    return selected
def insert_think(visited,newstate,f):
    selected_stu=[]
    for k in newstate:
        selected_stu.extend(k)
    selected= sorted(selected_stu)
    joined_string = "-".join(selected)
    if joined_string not in visited or f<visited[joined_string]:
        visited[joined_string]=f
        return 1
    return 0
        

def solver(input_file):
    """
    1. This function should take the name of a .txt input file in the format indicated in the assignment.
    2. It should return a dictionary with the following keys:
        - "assigned-groups" : a list of groups assigned by the program, each consisting of usernames separated by hyphens
        - "total-cost" : total cost (number of complaints) in the group assignment
    3. Do not add any extra parameters to the solver() function, or it will break our grading and testing code.
    4. Please do not use any global variables, as it may cause the testing code to fail.
    5. To handle the fact that some problems may take longer than others, and you don't know ahead of time how
       much time it will take to find the best solution, you can compute a series of solutions and then
       call "yield" to return that preliminary solution. Your program can continue yielding multiple times;
       our test program will take the last answer you 'yielded' once time expired.
    """
    # students_data=data_student(input_file)
    # students= students_data.keys()
    # path=[]
    # value=0
    # (path,value)=DFS_call([],0,students,sys.maxsize,students_data)
    # t=1


    #---------------------------------------------------------------------------------------
    ans_list=[]
    prevalue= sys.maxsize
    while True:   
        students_data=data_student(input_file)
        students= students_data.keys()
        visited={}
        fringe=[]
        fringe+=[(0,[],[]),]
        while len(fringe)>0:
            (value,state,path) = min(fringe)
            fringe.pop(fringe.index((value,state,path)))

            if is_goal(path,students_data.keys()):
                result = path
                break
            for s in successor(students,path,students_data):
                f=get_cost(s,value,students_data)
                path_taken = path+[s]
                #----------------------
                k=0
                k=insert_think(visited,path_taken,f)
                #----------------------
                if k==1:
                    fringe.append((f,s,path_taken))

        if(value<prevalue):
            prevalue=value
            ans_list=[]
            for l in path:
                k=""
                for i in range(0,len(l)):
                    k=k+l[i]+"-"
                ans_list.append(k[:-1])
            # Simple example. First we yield a quick solution
            yield({"assigned-groups": ans_list,
               "total-cost" : prevalue})
    #---------------------------------------------------------------------------------------------   
    # yield({"assigned-groups": ["vibvats-djcran-zkachwal", "shah12", "vrmath"],
    #        "total-cost" : 12})

    # #Then we think a while and return another solution:
    # time.sleep(10)
    # yield({"assigned-groups": ["vibvats-djcran-zkachwal", "shah12-vrmath"],
    #            "total-cost" : 10})

    # # # This solution will never befound, but that's ok; program will be killed eventually by the
    # # #  test script.
    # while True:
    #     pass
    
    # yield({"assigned-groups": ["vibvats-djcran", "zkachwal-shah12-vrmath"],
    #            "total-cost" : 9})

if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected an input filename"))

    for result in solver(sys.argv[1]):
        print("----- Latest solution:\n" + "\n".join(result["assigned-groups"]))
        print("\nAssignment cost: %d \n" % result["total-cost"])
    
