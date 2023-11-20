# Routing-and-Navigation
Implementation of graph search algorithms to navigate from one city to another. Uses BFS, DFS, IDS, Uniform-cost (Dijkstra), and A-star routing algorithms with distance, time, or number of turns as costs.

The program runs as per the following command line format:
./route.py [start-city] [end-city] [routing-algorithm] [cost-function]
where:
• start-city and end-city are the cities we need a route between. • routing-algorithm is one of:
  – bfs uses breadth-first search (which ignores edge weights in the state graph)
  – uniform is uniform cost search (the variant of bfs that takes edge weights into consideration)
  – dfs uses depth-first search
  – ids uses iterative deepening search
  – astar uses A* search, with a suitable heuristic function
• cost-function is one of:
  – segments tries to find a route with the fewest number of “turns” (i.e. edges of the graph)
  – distance tries to find a route with the shortest total distance
  – time tries to find the fastest route, for a car that always travels at the speed limit

The output of the program is of the following format:
[optimal?] [total-distance-in-miles] [total-time-in-hours] [start-city] [city-1] [city-2] ... [end-city]
where:
•[optimal?] is either yes or no to indicate whether the program can guarantee that the solution found is one with the lowest cost

# Search Algorithms(Knowledge Representation)
1. Breadth-First-Search(BFS)
2. Depth-First-Search(DFS)
3. Iterative Deepening Search(IDS)
4. Uniform Cost Search
5. A-star search

# Approach
1. Initialization:
It reads GPS data (city-gps.txt) and road segments data (road-segments.txt) from text files.
It extracts latitude and longitude coordinates for cities and road segment information.

2. Command Line Arguments:
Takes command line arguments for the start city, end city, routing algorithm, and cost function.

3. Search Algorithms:
It provides implementations for several search algorithms:
Breadth-First Search (BFS)
Depth-First Search (DFS)
Iterative Deepening Search (IDS)
Uniform-Cost Search
A* Search

4. Heuristic Functions:
Different heuristic functions are defined based on the chosen cost function (segments, distance, or time).
These heuristic functions help guide the search algorithms towards the goal city.

5. Successor Function:
Defines a successor function that generates possible child nodes (cities) given a parent node (current state).

6. Goal State:
The goal state is determined by checking if the current city matches the end city.

7. Handling Noise in Data:
Accounts for potential noise in the data, such as unavailable or incorr<img width="587" alt="Screenshot 2023-11-20 at 8 35 22 AM" src="https://github.com/Vaibhav-09-P/Routing-and-Navigation/assets/134619542/52701c9c-a42f-43cc-9c5d-77b6cc2e0d75">
ect GPS locations.
In case of A* search with distance or time as costs, the heuristic is designed to handle inaccuracies in GPS data.

8. Evaluation Functions:
Evaluation functions are defined to calculate the cost of reaching a child node from a parent node based on the chosen algorithm and cost function.

9. Solution Function:
The solve function determines the appropriate search algorithm based on user input and calls it to find the solution.

10. Printing Directions:
If a solution is found, it prints the optimal route, including directions and details about each road segment.
If no route is found, it informs the user.


# Visuals and GUI

The project contains a graphical user interface (GUI) that that allows users to input start city, end city, algorithm used, and hueristic. The GUI displays number of turns to be taken by the selected algorithm path, which cities it has to visit before reaching the destination city, and how much time it will take to reach them.
