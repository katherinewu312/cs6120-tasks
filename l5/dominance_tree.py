import json
import sys

from cfg import form_basic_blocks, build_cfg

# Implemention for constructing a dominance tree for a given CFG

def get_dominance_tree(cfg: dict[int,list[int]]) -> dict[int, list[int]]:
    """Computes the dominance tree for a given CFG. For this tree, each node's children are those nodes it immediately dominates."""
    dom_tree = {k: [] for k in cfg}
    visited_nodes = set()
    for vertex in cfg:
        for successor in cfg[vertex]:
            if successor not in visited_nodes and successor != len(cfg)-1:
                dom_tree[vertex].append(successor)
                visited_nodes.add(successor)    
    return dom_tree


if __name__ == "__main__":
    program = json.load(sys.stdin)
    for func in program["functions"]:
        basic_blocks = form_basic_blocks(func)
        cfg = build_cfg(basic_blocks)
        print(func["name"])
        dom_tree = get_dominance_tree(cfg)
        print(dom_tree)