import time
import copy
import sys
import heapq


def main():
    global puzzle, GOAL

    print_puzzle_solver_banner()
    choice = get_user_choice()

    # default puzzle
    if choice == 1:
        GOAL = [['A', 'N', 'G'], ['E', 'L', 'I'], ['C', 'A', '.']]  # goal state
        puzzle = select_default_puzzle()

    # custom puzzle
    elif choice == 2:
        print_puzzle_creation_rules()
        puzzle = get_custom_puzzle_from_user()

    # algo choice
    algo = get_user_algorithm_choice()
    # general search
    print(generalSearch(puzzle, algo))


# banner
def print_puzzle_solver_banner():
    print('======= Angelica Puzzle Solver =======')

# user choice
def get_user_choice():
    prompt = input('Type “1” to use a default puzzle, \nType “2” to create your own puzzle.\n')
    return int(prompt)

# default puzzles
def select_default_puzzle():
    # puzzle = ([['A', 'N', 'G'], ['E', 'L', 'I'], ['C', '.', 'A']])  # sample on book
    # puzzle = ([['A', 'N', 'G'], ['E', 'L', 'I'], ['C', 'A', '.']])  # depth 0
    # puzzle = (['A', 'N', 'G'], ['E', 'L', 'I'], ['.', 'C', 'A'])  # depth 2
    # puzzle = (['A', 'N', 'G'], ['L', '.', 'I'], ['E', 'C', 'A'])  # depth 4
    puzzle = (['A', 'G', 'I'], ['L', '.', 'N'], ['E', 'C', 'A'])  # depth 8
    # puzzle = (['A', 'G', 'I'], ['L', '.', 'C'], ['E', 'A', 'N'])  # depth 12
    # puzzle = (['A', 'I', 'C'], ['L', '.', 'G'], ['E', 'A', 'N'])  # depth 16
    # puzzle = (['C', 'A', 'N'], ['E', 'A', 'L'], ['I', 'G', '.'])  # depth 20
    # puzzle = (['.', 'C', 'N'], ['E', 'I', 'A'], ['G', 'L', 'A'])  # depth 24
    return puzzle

# rules 
def print_puzzle_creation_rules():
    print('Rule1: put spaces between letters (A N G E L I C A .).\n')
    print('Rule2: use . to represent blank tile.\n')
    print('Create your own puzzle now: \n')

# custom puzzle
def get_custom_puzzle_from_user():
    # first row
    row1 = input('First row: ')
    # second row
    row2 = input('Second row: ')
    # third row
    row3 = input('Third row: ')

    # split all 3 rows by spaces
    r1 = row1.split(' ')
    r2 = row2.split(' ')
    r3 = row3.split(' ')

    return r1, r2, r3

# algo choice
def get_user_algorithm_choice():
    algoChoice = input('\nChoose your algorithm: '
                       '\n1. Uniform Cost Search '
                       '\n2. A* with the Misplaced Tile heuristic. '
                       '\n3. A* with the Manhattan distance heuristic\n')
    return int(algoChoice)


# return the number of misplaced tiles
def misplacedTiles(puzzle):
    misplaceCount = 0
    # iterate through each tile
    for i in range(len(puzzle)):
        for j in range(len(puzzle)):
            # if current tile is different from goal then it's misplaced
            # also we dont count blank space as misplaced
            if puzzle[i][j] != GOAL[i][j] and puzzle[i][j] != '.':
                misplaceCount += 1

    return misplaceCount


# calculates the total Manhattan distance for all tiles in the given state to reach the goal state
# Manhattan distance for a tile is the sum of the horizontal & vertical distance from its current position to its goal position
# special consideration is given for duplicate 'A' tiles in the goal state
def manhattanDistance(state):
    total_distance = 0
    duplicate_counter = 0
    # print("state: ", state)

    # iterate over all tiles in the given state
    for i in range(len(state)):
        for j in range(len(state[i])):
            # exclude the blank tile
            if state[i][j] != '.':
                distances = []

                # iterate over all tiles in the goal state
                for goal_i in range(len(GOAL)):
                    for goal_j in range(len(GOAL[goal_i])):
                        if GOAL[goal_i][goal_j] == state[i][j]:
                            # append Manhattan distance
                            distances.append(abs(goal_i - i) + abs(goal_j - j))

                # print(f"Distances for tile {state[i][j]}: {distances}")  # Debug print
                min_distance = min(distances)
                total_distance += min_distance
                duplicate_counter += distances.count(min_distance) - 1

    return total_distance + duplicate_counter


# return new puzzle that blank tile has been moved up
def moveUp(p, row, col):
    newPuzzle = copy.deepcopy(p)

    temp = newPuzzle[row][col]
    newPuzzle[row][col] = newPuzzle[row - 1][col]  # moving up
    newPuzzle[row - 1][col] = temp  # swapping

    return newPuzzle


# return new puzzle that blank tile has been moved down
def moveDown(p, row, col):
    newPuzzle = copy.deepcopy(p)

    temp = newPuzzle[row][col]
    newPuzzle[row][col] = newPuzzle[row + 1][col]  # moving up
    newPuzzle[row + 1][col] = temp  # swapping

    return newPuzzle


# return new puzzle that blank tile has been moved left
def moveLeft(p, row, col):
    newPuzzle = copy.deepcopy(p)

    temp = newPuzzle[row][col]
    newPuzzle[row][col] = newPuzzle[row][col - 1]  # moving up
    newPuzzle[row][col - 1] = temp  # swapping

    return newPuzzle


# return new puzzle that blank tile has been moved right
def moveRight(p, row, col):
    newPuzzle = copy.deepcopy(p)

    temp = newPuzzle[row][col]
    newPuzzle[row][col] = newPuzzle[row][col + 1]  # moving up
    newPuzzle[row][col + 1] = temp  # swapping

    return newPuzzle

# return blank tile position
def findBlank(state):
    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] == '.':
                return i, j
            
    return -1, -1  # return an invalid position if there's no blank tile

# generates and returns all possible children nodes of the given node
# a child node is generated by moving the blank tile in the problem state in each of the four directions (up, down, left, right), if possible
# note only nodes representing states that have not been visited yet are returned.
def generateChildren(currentNode, visitedNodes):
    children = []
    problem = currentNode.problem
    # blank tile pos
    i, j = findBlank(problem)

    # possible directions to move the blank tile (right, left, down, up)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    for direction in directions:
        # new position of the blank tile after moving in the current direction
        ni, nj = i + direction[0], j + direction[1]

        # if the new position is valid
        if ni >= 0 and ni < len(problem) and nj >= 0 and nj < len(problem[0]):
            newProblem = [row.copy() for row in problem]
            # swap blank tile with the tile in the new position
            newProblem[i][j], newProblem[ni][nj] = newProblem[ni][nj], newProblem[i][j]

            newChild = Node(copy.deepcopy(newProblem))  

            if newChild.problem not in visitedNodes:  # check if it has been visited
                children.append(newChild)
    
    return children


# return true if the puzzle is the same as goal state
def checkGoal(puzzle):
    return puzzle == GOAL


# This function is from the psuedo-code in slides provided by Prof. Keogh
def generalSearch(problem, queueingFunction):
    # record the time when generalSearch starts running
    # tstart = time.time()
    # set the function only to run 1500 seconds
    # t = 1500

    nodesExpnd = 0  # number of expanded nodes
    maxQueue = 0  # maximum queue size
    q = []  # priority queue
    
    # start node with given problem state
    n = Node(problem)

    # init the list of visited problem states with the start state
    visited = [n.problem]

    # add start node into queue
    # q.append(n)
    heapq.heappush(q, n)
    maxQueue += 1

    # loop until the puzzle is solved
    while True:
        # if queue empty, search failed
        if len(q) == 0:
            return 'Search Failed! !'
        
        # pop the node with the highest priority (lowest value) from the queue
        # currentNode = q.pop(0)
        currentNode = heapq.heappop(q)

        # add currentNode to visited list
        visited.append(currentNode.problem)

        # display current node being expanded
        print("Expanding note with g(n) = ", currentNode.depth,
              ", h(n) = ", currentNode.heuristic, ": \n")
        currentNode.printPuzzle()

        # sort the queue based on the cost of the nodes (sum of depth and heuristic) lowest h(n) + g(n), https://thepythonguru.com/python-builtin-functions/sorted/
        q = sorted(q, key=lambda j: j.cost)

        # check if current node is the goal state
        if checkGoal(currentNode.problem):
            # display the solution statistics and terminate the search
            print("Puzzle solved!!!\n\n" + "Expanded a total of " + str(nodesExpnd) + " nodes.\n" +
                  "Maximum number of nodes in the queue was " + str(maxQueue) +
                  ".\nThe solution depth was ", str(currentNode.depth))
            return 0

        visited.append(currentNode.problem)
        
        # expand all possible children of the current node
        expndChildren = generateChildren(currentNode, visited)

        for tmp in expndChildren:
            # increment number of expended nodes
            nodesExpnd += 1

            # increment depth
            # print("tmp.depth: ", type(tmp.depth))
            tmp.depth = currentNode.depth + 1

            # set heuristic based on algoChoice
            if queueingFunction == 1:
                tmp.heuristic = 0
            if queueingFunction == 2:
                tmp.heuristic = misplacedTiles(tmp.problem)
            if queueingFunction == 3:
                # print("tmp.problem: ", type(tmp.problem))
                tmp.heuristic = manhattanDistance(tmp.problem)

            # cost of children, sum depth and heuristic
            tmp.cost = tmp.depth + tmp.heuristic
            # put temp node into queue
            # q.append(tmp)
            heapq.heappush(q, tmp)

            # update max queue size
            if len(q) > maxQueue:
                maxQueue = len(q)

            # Exit the system if exceeded runtime
            # if time.time() > tstart + t:
            #     print('Exceeded runtime..')
            #     sys.exit()


# Node class to store each expanded node
# problem store the 2D puzzle
# heuristic stores h(n)
# depth stores g(n)
# cost stores h(n)+g(n)
class Node:
    def __init__(self, p):
        self.problem = p
        self.heuristic = 0
        self.depth = 0
        self.cost = 0

    def __lt__(self, other):  # comparison based on the cost
        return self.cost < other.cost

    def printPuzzle(self):
        print(self.problem[0][0], self.problem[0][1], self.problem[0][2])
        print(self.problem[1][0], self.problem[1][1], self.problem[1][2])
        print(self.problem[2][0], self.problem[2][1], self.problem[2][2])


        
if __name__ == "__main__":
    main()
