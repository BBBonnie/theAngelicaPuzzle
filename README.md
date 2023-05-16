# theAngelicaPuzzle
cs205 Project1


# Comparison of Algorithms:
This project encompasses the implementation of three algorithms: Uniform Cost Search, A* Misplaced Tile heuristic, and A* Manhattan Distance heuristic. Here, h(n) denotes the heuristic cost and g(n) symbolizes the cost from the starting point to the current node (depth). It's assumed that for Uniform Cost Search, the heuristic cost, h(n), is zero.


## Uniform Cost Search:
Uniform Cost Search operates by expanding the node with the smallest cost every time. In this project, we assign a zero value to h(n) and use only the depth, g(n), as the cost measure. This approach, while thorough, can lead to high time complexity for puzzles of significant depth, as it necessitates the expansion of nodes at every level. In this context, the Uniform Cost Search is functionally equivalent to a Breadth-First Search.


## A* Misplaced Tile
The A* Misplaced Tile heuristic calculates the number of tiles not in their correct position relative to the goal state (excluding tile zero), using this count as the heuristic.

Current State: \
A	N	G \
E	L	I \
C	.	A \

Goal State: \
A	N	G \
E	L	I \
C	A	. \

As illustrated in the referenced current/goal states, when comparing the current state to the goal state, only tile 8 is out of place. Consequently, our heuristic, h(n), equals 1. To create this function, I compared each tile in the current state to its counterpart in the goal state. If they matched, I moved to the next tile; if not, I increased the heuristic by 1. This approach was simpler to implement compared to the A* Manhattan Distance heuristic, as it merely involves counting the number of misplaced tiles. Additionally, we maintained the depth, g(n). Assuming a puzzle has 5 misplaced tiles and requires 3 levels of expansion to reach the goal state, our total cost would be 5+3=8.

## A* Manhattan Distance
The A* Manhattan Distance heuristic measures the total distance each tile (excluding tile zero) must travel to reach its correct location in the goal state. This is conceptually similar to the A* Misplaced Tile heuristic but provides a more nuanced estimate for larger future expansions.
 
Current State: \
G	N	A \
E	L	I \
C	A	. \

Goal State: \
A	N	G \
E	L	I \
C	A	. \

As depicted in the provided current/goal states, when we compare the current state to the goal state, tiles “G”, “A” are misplaced. To correctly position tile “G”, it must move 2 steps to the right. Tile “A” needs to shift 2 steps left. Consequently, our heuristic, h(n), is 2+2=4. For the code implementation, I iterated over the puzzle, comparing each tile with the goal state. The sum of the absolute differences in row and column positions gives the total distance from the current tile position to the goal tile spot. This method is slightly more complex than implementing A* Misplaced Tile, as it involves not only locating the misplaced tiles but also calculating the respective distances.


# Conclusion:
Upon analyzing the above data, both in terms of the number of nodes and maximum queue size, the A* Manhattan Distance heuristic ranks first, the A* Misplaced Tile heuristic second, and Uniform Cost Search third.
Uniform Cost Search is the slowest, consuming the highest number of nodes and maximum queue size. This is because in this context, Breadth-First Search is equivalent to Uniform Cost Search, both requiring O(b^d) in time and space complexity. Further, Uniform Cost Search lacks a heuristic, making it notably less efficient than the A* algorithms.
When comparing the two A* heuristic algorithms, the A* Misplaced Tile heuristic is less efficient than the A* Manhattan Distance heuristic, especially when the puzzle increases in complexity. I believe this is because the A* Misplaced Tile heuristic only assesses whether a tile is in its correct position, whereas the A* Manhattan Distance heuristic considers both whether a tile is in its correct position and the number of steps required to get it there. This makes the A* Manhattan Distance heuristic is the most efficient among these three algorithms.
