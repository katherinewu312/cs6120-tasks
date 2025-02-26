import json
import sys
import argparse
from graphviz import Digraph

from cfg import form_basic_blocks, build_cfg, add_entry_block, map_to_block_name
from dominators import get_dominators

# Implemention for constructing a dominance tree for a given CFG

def get_dominance_tree(doms: dict[int,set[int]], cfg: dict[int,list[int]]) -> dict[int, list[int]]:
    """Computes the dominance tree for a given CFG. 
    For this tree, each node's children are those nodes it immediately dominates.
    Returns a mapping of vertex -> its successors in the dominance tree."""
    dom_tree = dict()
    reverse_doms = {v: {k for k, s in doms.items() if v in s} for v in set.union(*doms.values())}
    for vertex in reverse_doms:
        # get the immediate successors of this node
        # but don't include the very last block, the one after the exit block
        dom_tree[vertex] = [item for item in (reverse_doms[vertex] & set(cfg[vertex])) if item != len(reverse_doms) - 1]
    return dom_tree


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--draw', action='store_true', help="Draw and display the dominance tree graph.")
    args = parser.parse_args()
    
    program = json.load(sys.stdin)
    for func in program["functions"]:
        basic_blocks = form_basic_blocks(func)
        basic_blocks = add_entry_block(basic_blocks)
        cfg = build_cfg(basic_blocks)
        print(func["name"])
        doms = get_dominators(cfg)
        dom_tree = get_dominance_tree(doms, cfg)
        print(dom_tree)
        
        if args.draw:
            names_map = map_to_block_name(basic_blocks)
            dot = Digraph()
            for node, name in names_map.items():
                dot.node(str(node), label=name)

            for parent, children in dom_tree.items():
                for child in children:
                    dot.edge(str(parent), str(child))

            # Render the graph to a file and display
            dot.render('dominance_tree', format='png', cleanup=True)
            dot.view()
