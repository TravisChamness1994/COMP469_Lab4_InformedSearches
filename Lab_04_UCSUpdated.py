"""
Created on Sun Sep 19 12:15:01 2021
Updated 09/19/21 4:02 pm
@author: Daniel & Smooch Master 420 BLAYZE Dingo
"""
import sys

maze = []
startNode = None
goalNode = None
fringe = []
visited = []
ULDR  = None#funfun
currentNode = None

ROBOT = 'R'
DIAMOND = 'D'

class node:
    def __init__(self,parent,data,cost,children):
        self.parent = parent
        self.data = data
        self.cost = cost
        self.children = []

#Stolen from Lab 3
def create_map():
    # map_name = input("Enter map name(try \"mazeMap.txt\"): ")
    map_name = "labGivenMaze.txt"
    file = open(map_name, "r")

    maze = []
    line = []
    while 1:
        char = file.read(1)
        if not char:
            break
        elif char == '1':
            line.append(1)
        elif char == '3':
            line.append(3)
        elif char == '6':
            line.append(6)
        elif char == ROBOT:
            line.append(ROBOT)
        elif char == DIAMOND:
            line.append(DIAMOND)
        elif char == '-':
            line.append('-')
        elif char == '\n':
            maze.append(line)
            line = []
    if line:
        maze.append(line)
    file.close()
    return maze


def initialization():
    global maze
    global startNode
    global goalNode
    global fringe
    global visited
    global ULDR #funfun
    global currentNode

    maze = create_map() #Builds maps for us via txt file
    #
    # maze1 = [
    #         ["-","-","-","-","-","-","-"],
    #         ["-","R",6,6,6,"D","-"],
    #         ["-",1,1,1,1,1,"-"],
    #         ["-",1,3,3,3,1,"-"],
    #         ["-","-","-","-","-","-","-"]]
    find_goal_start = True
    startNode, goalNode = print_maze_id_start_goal(find_goal_start)
    fringe = [startNode]
    visited = []
    ULDR = [[-1,0],[0,-1],[1,0],[0,1]]  #recheck movement coordinates
    currentNode = None

# "Print maze and ID the Start and Goal"
# Allows user to print a maze, and on request of a Boolean True find_goal_start parameter, return the start and goal nodes.
def print_maze_id_start_goal(find_goal_start = False):
    for i, row in enumerate(maze):
        for j, val in enumerate(row):
            if val == ROBOT:
                startNode = node(None,[i,j],0,None)
            elif val == DIAMOND:
                goalNode = node(None, [i,j],0, None)
            print(val, end=' ')
        print()
    if find_goal_start:
        return startNode, goalNode #returns the goal and start node if requested by user via parameter
    else:
        return ""  # effectively return nothing

def lowestCostNode(currentNode):
    '''This will pick the lowest cost node from the fringe '''
    global fringe
    nodeIndex = None
    maxCost = sys.maxsize #acts as the largest possible integer
    smallestCostNode = node(None, None,maxCost, None)
    for index,element in enumerate(fringe):
        if element.cost < smallestCostNode.cost and element not in visited: #change not in visited with travis node function, will have to make function go through all nodes in visited to see their data
            smallestCostNode = element
            nodeIndex = index
    
    if(smallestCostNode.cost == maxCost):
        print("All nodes left have been visited")
        ## what should the algorithm do if nodes in fringe have already been visited
        return currentNode
    else:
        fringe.pop(nodeIndex)
        return smallestCostNode
   
def goalTest(sampleNode):
    if sampleNode.data == goalNode.data:
        return True
    else:
        return False
    
def successor_function():
    #this will go inside the while loop in main()
    global currentNode
    global fringe
    global ULDR
    global visited

    # currentNode = lowestCostNode(currentNode) #from fringe
    for moves in ULDR:
        #If the move doesn't result in being on a wall
        if maze[currentNode.data[0]+moves[0]][currentNode.data[1] + moves[1]] != '-':
            child = node(currentNode, [currentNode.data[0]+moves[0],currentNode.data[1] + moves[1]], None, None)
            # Robot and Diamond both account for 0 cost, but must be handled respecitively as 0 cost
            if maze[child.data[0]][child.data[1]] != 'R' and maze[child.data[0]][child.data[1]] != 'D':
                child.cost = currentNode.cost + maze[child.data[0]][child.data[1]]
            else:
                #Els the most is Diamond or Robot and incur 0 cost to child
                child.cost = currentNode.cost
            currentNode.children.append(child)
            fringe.append(child)
    #after finding all children of currentNode, place it in visited
    visited.append(currentNode)
            
def main():
    global currentNode
    global fringe
    global currentNode

    initialization()
    while fringe:
        currentNode = lowestCostNode(currentNode)
        if not goalTest(currentNode): #reduced goalTest(currentNode) == False to logical equiv with not statement
            successor_function()
        else:
            #needs to execute commands that will RETURN plan cost and nodes to get there
            pass
    
    print("No solution found")

main()

# YO DANIEL
# For Priority Queue Testing: "TypeError: '<' not supported between instances of 'node' and 'node'"
# On briefly checking, there is no means to override < for our needs.

# fancyList = []
# node1 = node(None, [1,1], 1, None)
# node2 = node(None, [2,2], 2, None)
# node3 = node(None, [3,3], 1, None)
# node4 = node(None, [4,4], 2, None)
# fancyList.append((node1.cost, node1))
# fancyList.append((node2.cost, node2))
# fancyList.append((node3.cost, node3))
# fancyList.append((node4.cost, node4))
# fancyList.sort(reverse=True)
# print(fancyList.pop())
