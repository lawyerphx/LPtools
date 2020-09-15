# LPtools
Linear Programming Solving Tools for IE6001@NUS

### explicit functions

`LP.py`  standard solver for LP problem.
* `LPSolver` a class that storage the infomation needed for LP problem (A, b, c).
* `.add_line` add a new line for A.
* `.initBasicSet` the first stage of simplex algo: find a BFS.
* `.getShadowPrice` get the shadow price of b.

`simplex` an implementation of simplex algorithm.
* `Simplex` a class that implements classic simplex algorithm.
* `.add_constraint` add one constraint to the initial tableau.
* `.set_index`  set the basic variable set.
* `.solveStandard` with standard rule. (faster)
* `.solveBlandRule` with bland's rule. (slower, but can avoid loop)

`test.py` some test cases.

### Todo
* About duality.
* Refine the first stage algorithm implemented in `LPSolver`
* Make a balance between two rules.
* run TP-H