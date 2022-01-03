#!/usr/local/bin/python3
# route.py : Find routes through maps
#
# Code by: name IU ID
#
# Based on skeleton code by V. Mathur and D. Crandall, January 2021
#


# !/usr/bin/env python3
import sys
import math
import decimal

#def RBFS():
def parse_map(filename):
    with open(filename, "r") as f:
        return [[s for s in line.split()] for line in f]


def get_dictionary_nodes():
    road_segment_array = parse_map("./road-segments.txt")
    d={}
    for line in road_segment_array:
        if line[0] not in d:
            d[line[0]]=list()
        if line[1] not in d:
            d[line[1]]=list()
        d[line[0]].append([line[1],float(line[2]),float(line[3]),line[4]])
        d[line[1]].append([line[0],float(line[2]),float(line[3]),line[4]])
    return d

def get_positions():
    city_gps=parse_map("./city-gps.txt")
    d=dict()
    for line in city_gps:
        if line[0] not in d:
            d[line[0]]= list()
            d[line[0]].extend([float(line[1]),float(line[2])])
    return d

def successors(state,d):
    return d.get(state)

def haversine(latitude1,longitude1,latitude2,longitude2):
    latitude1,longitude1,latitude2,longitude2 = map(math.radians, [latitude1,longitude1,latitude2,longitude2])
    lon =longitude2-longitude1
    la=latitude2-latitude1
    a= math.sin(la/2)**2 + math.cos(latitude1)* math.cos(latitude2)* math.sin(lon/2)**2
    b= 2 * math.asin(math.sqrt(a))*3956
    return b

def h_distance(state, next_state,position_nodes):
    if state not in position_nodes or next_state not in position_nodes:
        return 0
    lat1,long1=position_nodes.get(state)
    lat2,long2=position_nodes.get(next_state)
    return haversine(lat1,long1,lat2,long2)

def get_heuristic(path,state,next_state,position_nodes,cost_function):

    if cost_function == "distance":
        return path[1]+next_state[1]+h_distance(state[0],next_state[0],position_nodes)
    elif cost_function == "segments":
        #return len(path[0])+1+(1/next_state[1])
        #return len(path[0])+0
        return len(path[0])+1+(h_distance(state[0],next_state[0],position_nodes)/923) #725,25
    elif cost_function == "time":
        return path[2]+(next_state[1]/next_state[2])+(h_distance(state[0],next_state[0],position_nodes)/65) # 50 calculaied average speed using given data
    elif cost_function == "safe":
        if "I-" in next_state[3]:
            A=path[3]+((1/(10**6))*next_state[1])+0
        else:
            A=path[3]+((2/(10**6))*next_state[1])+0
        return A
    else:
        return 0

# def cost_function_distance(state,next_state,position_nodes):
#     f=g_distance(state,next_state)+h_distance(state,next_state)
#     return f

def is_goal(state,end):
    if (state == end):
        return True
    return False


def BestFirstSearch(start,end,edge_nodes,position_nodes,cost_function):
    fringe=[]
    visited={}
    #fringe+= [(0,(start,0,0,""),["",0]),]
    fringe+= [(0,(start,0,0,""),[[],0,0,0]),]
    while len(fringe) > 0:
        (value,state,path)= min(fringe)
        index=fringe.index((value,state,path))
        (value1,state1,path1)=fringe.pop(index)

        if is_goal(state[0],end):
            return path

        for s in successors(state[0],edge_nodes):
            #f=path[1]+s[1]+h_distance(state[0],s[0],position_nodes)
            #p=[path[0]+s[0]+" ",path[1]+s[1]]
            f=get_heuristic(path,state,s,position_nodes,cost_function)
            if s[0] not in visited or f<visited[s[0]]:
                r=str(s[3])+" for "+str(s[1])+" miles"
                if "I-" in s[3]:
                    A=path[3]+((1/(10**6))*s[1])
                else:
                    A=path[3]+((2/(10**6))*s[1])
                p=[path[0]+[(s[0],r)],path[1]+s[1],path[2]+(s[1]/s[2]),A]
                visited[s[0]]= f
                fringe.append((f,s,p))
    return []

def get_average_speed():
    total_speed=0
    max=0
    road_segment_array = parse_map("./road-segments.txt")
    for l in road_segment_array:
        if max<float(l[3]):
            max=float(l[3])
        total_speed= total_speed+ float(l[3])
    # print(max)
    return total_speed/len(road_segment_array)

def get_average_segment_length():
    total_length=0
    max=0
    road_segment_array = parse_map("./road-segments.txt")
    for l in road_segment_array:
        if max<float(l[2]) and float(l[2]) != 923:
            max=float(l[2])
        total_length= total_length+ float(l[2])
    # print(max)
    return total_length/len(road_segment_array)

def get_route(start, end, cost):
    
    """
    Find shortest driving route between start city and end city
    based on a cost function.

    1. Your function should return a dictionary having the following keys:
        -"route-taken" : a list of pairs of the form (next-stop, segment-info), where
           next-stop is a string giving the next stop in the route, and segment-info is a free-form
           string containing information about the segment that will be displayed to the user.
           (segment-info is not inspected by the automatic testing program).
        -"total-segments": an integer indicating number of segments in the route-taken
        -"total-miles": a float indicating total number of miles in the route-taken
        -"total-hours": a float indicating total amount of time in the route-taken
        -"total-expected-accidents": a float indicating the expected accident count on the route taken
    2. Do not add any extra parameters to the get_route() function, or it will break our grading and testing code.
    3. Please do not use any global variables, as it may cause the testing code to fail.
    4. You can assume that all test cases will be solvable.
    5. The current code just returns a dummy solution.
    """
    # edge_nodes={}
    edge_nodes=get_dictionary_nodes()
    position_nodes= get_positions()
    path=BestFirstSearch(start,end,edge_nodes,position_nodes,cost)
    # speed=get_average_speed()
    # length=get_average_segment_length()
    
    # route_taken = [("Martinsville,_Indiana","IN_37 for 19 miles"),
    #                ("Jct_I-465_&_IN_37_S,_Indiana","IN_37 for 25 miles"),
    #                ("Indianapolis,_Indiana","IN_37 for 7 miles")]
    
    # return {"total-segments" : len(route_taken), 
    #         "total-miles" : 51, 
    #         "total-hours" : 1.07949, 
    #         "total-expected-accidents" : 0.000051, 
    #         "route-taken" : route_taken}
    return {"total-segments" : len(path[0]), 
            "total-miles" : path[1], 
            "total-hours" : path[2], 
            "total-expected-accidents" : path[3], 
            "route-taken" : path[0]}


# Please don't modify anything below this line
#
if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise(Exception("Error: expected 3 arguments"))

    (_, start_city, end_city, cost_function) = sys.argv
    if cost_function not in ("segments", "distance", "time", "safe"):
        raise(Exception("Error: invalid cost function"))

    result = get_route(start_city, end_city, cost_function)

    # Pretty print the route
    print("Start in %s" % start_city)
    for step in result["route-taken"]:
        print("   Then go to %s via %s" % step)

    print("\n Total segments: %6d" % result["total-segments"])
    print("    Total miles: %10.3f" % result["total-miles"])
    print("    Total hours: %10.3f" % result["total-hours"])
    print("Total accidents: %15.8f" % result["total-expected-accidents"])


