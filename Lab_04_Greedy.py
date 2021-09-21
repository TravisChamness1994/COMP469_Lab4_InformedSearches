# Lab 04
# Greedy Search Implementation
# By: Daniel Ramirez and Travis Chamness
# Date: 09/20/21

import sys

maze = []
startNode = None
goalNode = None
fringe = []
visited = []
path = []
pathCost = None
ULDR  = None#funfun
currentNode = None

ROBOT = 'R'
DIAMOND = 'D'

class node:
    def __init__(self,parent,data,cost,children, forwardCost):
        self.parent = parent
        self.data = data
        self.cost = cost
        self.forwardCost = forwardCost
        self.children = []

#Stolen from Lab 3
def create_map():
    # map_name = input("Enter map name(try \"mazeMap.txt\"): ")
    map_name = "labGivenMaze.txt"
    # map_name = "maze1.txt"
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
    find_goal_start = True
    startNode, goalNode = print_maze_id_start_goal(find_goal_start)
    startNode = heuristic_function(startNode)
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
                startNode = node(None,[i,j],0,None, None)
            elif val == DIAMOND:
                goalNode = node(None, [i,j], 0, None, 0)
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
    smallestCostNode = node(None, None,None, None, maxCost)
    for index,element in enumerate(fringe):
        if element.forwardCost < smallestCostNode.forwardCost: #change not in visited with travis node function, will have to make function go through all nodes in visited to see their data
            smallestCostNode = element
            nodeIndex = index

    if(smallestCostNode.forwardCost == maxCost):
        print("All nodes left have been visited")
        ## what should the algorithm do if nodes in fringe have already been visited
        return currentNode
    else:
        fringe.pop(nodeIndex)
        return smallestCostNode

def goalTest():
    global goalNode
    global currentNode
    if currentNode.data == goalNode.data:
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
            child = node(currentNode, [currentNode.data[0]+moves[0],currentNode.data[1] + moves[1]], None, None, None)
            # Robot and Diamond both account for 0 cost, but must be handled respecitively as 0 cost
            child = heuristic_function(child)
            if maze[child.data[0]][child.data[1]] != 'R' and maze[child.data[0]][child.data[1]] != 'D': #TODO Remove if-else statement
                child.cost = currentNode.cost + maze[child.data[0]][child.data[1]]
            else:
                #Else the most is Diamond or Robot and incur 0 cost to child
                child.cost = currentNode.cost
            currentNode.children.append(child)
            fringe.append(child)
    #after finding all children of currentNode, place it in visited
    visited.append(currentNode)

def in_visited():
    global visited
    global currentNode

    in_visited = False
    for node in visited:
        if currentNode.data == node.data:
            in_visited = True
        if in_visited:
            break
    return in_visited

def populate_path():
    global currentNode
    global pathCost
    global path

    pathCost = currentNode.cost
    while currentNode != None:
        path.insert(0,currentNode.data)
        currentNode = currentNode.parent

def heuristic_function(node):
    global goalNode
    node.forwardCost = abs(goalNode.data[0] - node.data[0]) + abs(goalNode.data[1] - node.data[1])
    return node

def main():
    global currentNode
    global fringe
    global currentNode
    global path
    goalFound = False
    initialization()
    while fringe:
        currentNode = lowestCostNode(currentNode)
        goalFound = goalTest()
        if not goalFound and not in_visited(): #reduced goalTest(currentNode) == False to logical equiv with not statement
            successor_function()
        elif goalFound:
            populate_path()
            break
    print(path)
    print(pathCost)
    return path, pathCost
main()