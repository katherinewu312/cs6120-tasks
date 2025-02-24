# pylint: disable=redefined-outer-name
import json
import sys

from cfg import form_basic_blocks, build_cfg, get_pred_cfg
from dominators import get_dominators
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


def get_dominance_frontier(cfg: CFG):
    """Computes the dominance frontier for every node in a CFG."""

    # Predecessors
    preds = get_pred_cfg(cfg)

    # Dominator map (maps each `v` -> set of blocks that dominate node `v`)
    doms: Dict[Idx, Set[Idx]] = get_dominators(cfg)

    # Dominance frontier
    df: Dict[Idx, Set[Idx]] = {v: set() for v in cfg}

    # ------------------------- Some helper functions ------------------------ #

    def dominates(x: Idx, y: Idx) -> bool:
        """`dominates(x, y)` indicates whether `x` dominates `y`"""
        return x in doms[y]

    def strictly_dominates(x: Idx, y: Idx) -> bool:
        """`strictly_dominates(x, y)` indicates
        whether `x` *strictly* dominates `y`"""
        result = (x != y) and dominates(x, y)
        return result

    # ---------------------- Populate dominance frontier --------------------- #

    # `a`'s dominance frontier contains `b` if `a` doesn't strictly dominate `b`
    # and `a` dominates some predecessor of `b`
    for a, succs in cfg.items():
        df[a] = {
            b
            for b in succs
            if any(
                {
                    pred
                    for pred in preds[b]
                    if (not strictly_dominates(a, b)) and dominates(a, pred)
                }
            )
        }

    return df


if __name__ == "__main__":
    program = json.load(sys.stdin)
    for func in program["functions"]:
        bbs: List[Block] = form_basic_blocks(func)
        cfg: CFG = build_cfg(bbs)
        print(func["name"])
        df = get_dominance_frontier(cfg)
        print(df)
