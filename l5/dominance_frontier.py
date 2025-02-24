# pylint: disable=redefined-outer-name
import json
import sys

from cfg import form_basic_blocks, build_cfg
from dominators import get_dominators
from dominance_tree import get_dominance_tree
from typing import List, Dict, Set

# ---------------------------------------------------------------------------- #
#                   Some type aliases to improve readibility                   #
# ---------------------------------------------------------------------------- #

# A Bril value is either an int or a bool
type BrilValue = int | bool

# Variable names are just Python strings
type Var = str

# A Bril instruction is a dictionary (JSON)
type Instr = Dict

# A block is a list of instructions
type Block = List[Instr]

# Index for basic blocks / CFG nodes
type Idx = int

# A CFG maps each node's index to a list of successor indices
type CFG = Dict[Idx, List[Idx]]

# ---------------------------------------------------------------------------- #
#                            Dominance frontier code                           #
# ---------------------------------------------------------------------------- #


def get_immediate_dominators(cfg: CFG) -> Dict[Idx, Set[Idx]]:
    """Computes the immediate dominators for each node in a CFG"""

    # Note: the immediate dominators are just the children of each node
    # in the dominator tree (here we just need to convert the list
    # of children in `dom_tree` to a set)

    dom_tree = get_dominance_tree(cfg)
    idoms = {v: set(dom_tree[v]) for v in cfg}
    return idoms


def get_dominance_frontier(cfg: CFG):
    """Computes the dominance frontier for every node in a CFG."""

    # Dominator map (maps each `v` -> set of blocks that dominate node `v`)
    doms: Dict[Idx, Set[Idx]] = get_dominators(cfg)

    # Dominator tree
    dom_tree: Dict[Idx, List[Idx]] = get_dominance_tree(cfg)

    # Immediate dominators
    imm_doms = get_immediate_dominators(cfg)

    # Dominance frontier
    df: Dict[Idx, Set[Idx]] = {v: set() for v in cfg}

    # ------------------------- Some helper functions ------------------------ #

    def dominates(x: Idx, y: Idx) -> bool:
        """`dominates(x, y)` indicates whether `x` dominates `y`"""
        return (x in doms[y])

    def idom(x: Idx, y: Idx) -> bool:
        """`idom(x, y)` indicates whether `x` *immediately* dominates `y`"""
        return (y in imm_doms[x])

    def sdom(x: Idx, y: Idx) -> bool:
        """`sdom(x, y)` indicates whether `x` *strictly* dominates `y`"""
        result = (x != y) and dominates(x, y)
        return result
    
    # ---------------------- Populate dominance frontier --------------------- #

    for x, succs in cfg.items():
        for y in succs:
            # If `x` doesn't immediately dominate `y`, add `y` to `x`'s DF
            if not idom(x, y):
                df[x].add(y)

        # For each of `x`'s children `z` in the dominator tree,
        # check `z`'s DF and add each node in `df[z]` that isn't strictly dominated by `x`
        for z in dom_tree[x]:
            for y in df[z]:
                if not sdom(x, y):
                    df[x].add(y)
    return df


if __name__ == "__main__":
    program = json.load(sys.stdin)
    for func in program["functions"]:
        bbs: List[Block] = form_basic_blocks(func)
        cfg: CFG = build_cfg(bbs)
        print(func["name"])
        df = get_dominance_frontier(cfg)
        print(df)
