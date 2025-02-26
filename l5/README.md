# Lesson 5: Global Analysis

**Code overview**:
- [`dominance.py`](./dominators.py): Finds dominators for a function
- [`dominance_tree.py`](./dominance_tree.py): Constructs the dominance tree
- [`dominance_frontier.py`](./dominance_frontier.py): Compute the dominance frontier
- [`cfg.py`](./cfg.py): Code for forming basic blocks + building CFGs
- [`cfg_examples.py`](./cfg_examples.py): Example CFGs implemented using Python data structures 
- [`dfs.py`](./dfs.py): Enumerates all paths between two nodes in a CFG using DFS 

**Testing on core benchmarks using Turnt**
To confirm (using Turnt) that our implementation works on the core Bril benchmarks, `cd` into the [`test/core_benchmarks`](./test/core_benchmarks/) subdirectory and run the following:
```bash 
$ cd test/core_benchmarks
$ turnt *.bril --env doms
$ turnt *.bril --env tree
$ turnt *.bril --env frontier
```
