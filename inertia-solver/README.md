# inertia-solver

## Introduction
This project is just a solver for an online game called [Inertia](https://www.chiark.greenend.org.uk/~sgtatham/puzzles/js/inertia.html). To win the game you must move the ball avoiding mines and collect all the gems. There are eight ways to move the ball (north, south, east, west, north east, north west, south east, south west). When the ball moves in a direction it continues its movement until it hits a wall, lands on a broken circle, or reaches an end of the grid.

Each game is encoded to a string which is concatenated to the end of a link with the dimensions of the grid. This string uniquely identifies a game. The grid is encoded as follows:
- 's' for the broken circle.
- 'b' for blank space.
- 'w' for a wall.
- 'm' for a mine.
- 'g' for a gem.
- The ball's position is just one of 's' or 'b' capitalized i.e. 'S' or 'B'.

With the dimensions you can reconstruct the game from this string. 

The solution introduced here works as follows:
- The grid's information and the ball movements rules are encapsulated in the **InertiaGame** class located in _inertia_game.h_.
- The solver is located in the _inertia_solver.cpp_ file.
- The algorithm solving the game could be considered as a **Greedy Best First algorithm** that chooses a path according to the nearest gem to the current ball position.
- The heuristic used in the algorithm is the **Taxicab metric** which is also known as the **Manhattan distance**.
- To avoid moving in an infinite cycle, each block visited (stopped at) by the movement of the ball in the chosen path is recoreded starting from the initial position of the ball.
- If the ball couldn't move any further by any move excluding cycles, then the ball is considered to be trapped and then the algorithm needs to determine another path.
- Each time the algorithm wants to decide the next move, it takes all the possible moves and assigns to them a weight according to the heuristic, then sorts the moves according to the weights. This information is recorded along the path.

## Building and running the solver
To build the solver run _build.sh_ (_build_debug.sh_ is for building with debug symbols). Run inertia-solver and see the usage. There is an example run command in the file _run_example.sh_ with a game id string acquired from the game's original website.

## GUI Solver
To run the automation client that solves the game in the browser, see the python file "inertia_solver_gui.py". Note that selenium chrome webdriver is used and it could be changed to any supported browser. The game is defined at the beginning of the script. See this [video](https://www.youtube.com/watch?v=5r3UfF7sOWY).
