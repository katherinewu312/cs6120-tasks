Group (@ngernest, @katherinewu312, @samuelbreckenridge)

[Code](https://github.com/katherinewu312/cs6120-tasks/tree/main/l5)               
(Sam: dominators, Katherine: dominator tree, Ernest: dominance frontier)          

To test our dominators code, we implemented a [version of DFS](https://github.com/katherinewu312/cs6120-tasks/blob/590ae42f591a1606f870639dcb3568911f60fac8/l5/dfs.py#L5) which enumerates all paths (without repeating nodes) between two nodes within a CFG. We then used DFS to enumerate all paths from the entry node to each node `v` in a CFG and checked that the intersection of all those paths contained `v`'s dominators. 

For dominance frontiers, we implemented a few helper functions which indicate for two nodes `x` and `y`, whether `x` (strictly) dominates `y`. With this in place, the main logic for constructing DFs could be encapsulated using just one Python set comprehension! To test our DF implementation, we implemented unit tests which checked that no condition in the definition of DFs is violated. Specifically, we check that for every node `A`, `A` does not strictly dominate any node in its DF, and that `A` dominates some predecessor of each element in its DF. We manually constructed [some CFGs](https://github.com/katherinewu312/cs6120-tasks/blob/main/l5/cfg_examples.py) using examples from the [CS 4120 lecture notes](https://www.cs.cornell.edu/courses/cs4120/2023sp/notes.html?id=reachdef), and created [unit tests](https://github.com/katherinewu312/cs6120-tasks/blob/590ae42f591a1606f870639dcb3568911f60fac8/l5/dominance_frontier.py#L104) which checked that our algorithms computed the same DFs as the lecture notes. We also manually compared the results of our Turnt tests with those in the [Bril dominator examples repo](https://github.com/sampsyo/bril/tree/main/examples/test/dom) to check that our code behaves the same as the reference implementation.










