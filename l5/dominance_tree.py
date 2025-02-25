import json
import sys

from cfg import form_basic_blocks, build_cfg
from dominators import get_dominators

# Implemention for constructing a dominance tree for a given CFG

def get_dominance_tree(doms: dict[int,set[int]], cfg: dict[int,list[int]]) -> dict[int, list[int]]:
    """Computes the dominance tree for a given CFG. 
    For this tree, each node's children are those nodes it immediately dominates."""
    dom_tree = {k: [] for k in doms}
    rev_doms = {v: {k for k, s in doms.items() if v in s} for v in set.union(*doms.values())}
    for vertex in rev_doms:
        # get the immediate successors of this node
        # but don't include the very last block, the one after the exit block
        dom_tree[vertex] = [item for item in (rev_doms[vertex] & set(cfg[vertex])) if item != len(rev_doms) - 1]
    return dom_tree
        
    
    '''
    visited_nodes = set()
    for vertex in cfg:
        for successor in cfg[vertex]:
            if successor not in visited_nodes and successor != len(cfg)-1:
                dom_tree[vertex].append(successor)
                visited_nodes.add(successor)    
    return dom_tree
    '''


if __name__ == "__main__":
    program = json.load(sys.stdin)
    for func in program["functions"]:
        basic_blocks = form_basic_blocks(func)
        cfg = build_cfg(basic_blocks)
        print(func["name"])
        doms = get_dominators(cfg)
        dom_tree = get_dominance_tree(doms, cfg)
        print(dom_tree)