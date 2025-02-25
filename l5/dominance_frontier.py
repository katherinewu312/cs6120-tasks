# pylint: disable=redefined-outer-name

import argparse
import json
import unittest
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

    # Initialize dominance frontier
    df: Dict[Idx, Set[Idx]] = {v: set() for v in cfg}

    # `a`'s dominance frontier contains `b` if `a` doesn't strictly dominate `b`
    # and `a` dominates some predecessor of `b`
    for a in cfg.keys():
        df[a] = {
            b
            for b in cfg.keys()
            if (not strictly_dominates(a, b))
            and any(dominates(a, pred) for pred in preds[b])
        }

    return df


class TestDominanceFrontier(unittest.TestCase):
    # Dominance Frontier example from CS 4120 lecture notes
    # https://www.cs.cornell.edu/courses/cs4120/2023sp/notes.html?id=reachdef
    #
    #
    #                    (7)
    #                     |
    #                     v
    #    (1)------------>(8)
    #    / \
    #   /   \
    #  v     v
    # (2)   (3)
    #  \     /
    #   \   /
    #    v v
    #    (4)
    #     |
    #     v
    #    (5)<---(6)
    #
    # - DF[1] = {5, 8}
    # - DF[2] = {2}
    # - DF[3] = {2}
    # - DF[4] = {5}
    def test_cs4120_example(self):
        nodes = list(range(10))

        cfg = {v: [] for v in nodes}
        cfg[1] = [2, 3, 8]
        cfg[2] = [4]
        cfg[3] = [4]
        cfg[4] = [5]
        cfg[6] = [5]
        cfg[7] = [8]

        # 0 is a dummy initial block whose successors are all the "real"
        # entry blocks in the CFG
        cfg[0] = [1, 6, 7]

        # 9 is dummy final block whose predecessors are all the "real"
        # final blocks in the CFG
        cfg[5] = [9]
        cfg[8] = [9]
        cfg[9] = []

        expected_df = {v: set() for v in nodes}
        expected_df[1] = {5, 8}
        expected_df[2] = {4}
        expected_df[3] = {4}
        expected_df[4] = {5}
        expected_df[5] = {9}
        expected_df[6] = {5}
        expected_df[7] = {8}
        expected_df[8] = {9}

        actual_df = get_dominance_frontier(cfg)
        self.assertDictEqual(actual_df, expected_df)


if __name__ == "__main__":
    # Set up an optional cmd-line argument `--test` that runs the test suite
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true", help="Runs unit tests")
    args = parser.parse_args()

    if args.test:
        unittest.main(argv=["first-arg-is-ignored"])
    else:
        program = json.load(sys.stdin)
        for func in program["functions"]:
            bbs: List[Block] = form_basic_blocks(func)
            cfg: CFG = build_cfg(bbs)
            print(func["name"])
            df = get_dominance_frontier(cfg)
            print(df)
