Group (@ngernest, @katherinewu312, @samuelbreckenridge)

[Code](https://github.com/katherinewu312/cs6120-tasks/tree/main/l5)               
(Sam: dominators, Katherine: dominator tree, Ernest: dominance frontier)          

Our code for finding dominators is a straightforward implementation of the pseudocode discussed in class. 
Coming up with a way to algorithmically confirm the dominators we compute was probably one of the trickier parts of 
the task as it involved thinking about different (potentially naive/slow) ways to compute dominators. To check the dominators output by our code, we implemented a [version of DFS](https://github.com/katherinewu312/cs6120-tasks/blob/590ae42f591a1606f870639dcb3568911f60fac8/l5/dfs.py#L5) which enumerates all 
paths (without repeating nodes) between two nodes within a CFG. We then used DFS to enumerate all paths from the 
entry node to each node `v` in a CFG and checked that the intersection of all those paths contained `v`'s dominators.
We run this check alongside our code for printing the dominator map so it runs for tests of our get_dominators 
functionality. As test cases for finding dominators we used a few simple bril examples which we checked manually and 
we run our implementation on all core bril benchmarks to confirm the code does not crash and the DFS based check 
passes. Running on all benchmarks revealed that our implementation did not handle functions with unreachable basic 
blocks so in the get_dominators function we added a pass to remove non-entry basic blocks with no predecessors.

For the dominance tree, each node's children are those nodes it immediately dominates. To implement the tree, which we represent as a mapping from nodes to its successors, we first reversed the dominators set obtained from get_dominators() in [dominators.py](https://github.com/katherinewu312/cs6120-tasks/blob/main/l5/dominators.py) to obtain a post-dominance set for each vertex in the cfg. For each vertex, we then took the intersection of its post-dominance set with its set of successors in the cfg to obtain those nodes that the vertex immediately dominates. This task was pretty straightforward, and we believe our implementation for this is quite concise. We also decided to use graphviz to generate dominator trees to better illustrate the trees; a visualization can be generated if you specify a --draw option when running the program. We tested our implementation using Turnt with those tests in the [Bril dominator examples repo](https://github.com/sampsyo/bril/tree/main/examples/test/dom), and verified that our code behaves the same.

For dominance frontiers, we implemented a few helper functions which indicate for two nodes `x` and `y`, whether `x` (strictly) dominates `y`. With this in place, the main logic for constructing DFs could be encapsulated using just one Python set comprehension! To test our DF implementation, we implemented unit tests which checked that no condition in the definition of DFs is violated. Specifically, we check that for every node `A`, `A` does not strictly dominate any node in its DF, and that `A` dominates some predecessor of each element in its DF. We manually constructed [some CFGs](https://github.com/katherinewu312/cs6120-tasks/blob/main/l5/cfg_examples.py) using examples from the [CS 4120 lecture notes](https://www.cs.cornell.edu/courses/cs4120/2023sp/notes.html?id=reachdef), and created [unit tests](https://github.com/katherinewu312/cs6120-tasks/blob/590ae42f591a1606f870639dcb3568911f60fac8/l5/dominance_frontier.py#L104) which checked that our algorithms computed the same DFs as the lecture notes. We also manually compared the results of our Turnt tests with those in the [Bril dominator examples repo](https://github.com/sampsyo/bril/tree/main/examples/test/dom) to check that our code behaves the same as the reference implementation.










