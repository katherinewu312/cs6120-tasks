# pylint: disable=redefined-outer-name

import argparse
import json
import unittest
import sys

from cfg import form_basic_blocks, build_cfg, get_pred_cfg
from cfg_examples import cs4120_example, princeton_cfg
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


def dominates(doms, x: Idx, y: Idx) -> bool:
    """`dominates(x, y)` indicates whether `x` dominates `y` in the
    dominance map `doms`"""
    return x in doms[y]


def strictly_dominates(doms, x: Idx, y: Idx) -> bool:
    """`strictly_dominates(x, y)` indicates
    whether `x` *strictly* dominates `y` according to the dominance map `doms`"""
    result = (x != y) and dominates(doms, x, y)
    return result


def get_dominance_frontier(cfg: CFG) -> Dict[Idx, Set[Idx]]:
    """Computes the dominance frontier for every node in a CFG."""

    # Predecessors
    preds = get_pred_cfg(cfg)

    # Dominator map (maps each `v` -> set of blocks that dominate node `v`)
    doms: Dict[Idx, Set[Idx]] = get_dominators(cfg)

    # ------------------------- Some helper functions ------------------------ #

    # ---------------------- Populate dominance frontier --------------------- #

    # Initialize dominance frontier
    df: Dict[Idx, Set[Idx]] = {v: set() for v in cfg}

    # `a`'s dominance frontier contains `b` if `a` doesn't strictly dominate `b`
    # and `a` dominates some predecessor of `b`
    for a in cfg.keys():
        df[a] = {
            b
            for b in cfg.keys()
            if (not strictly_dominates(doms, a, b))
            and any(dominates(doms, a, pred) for pred in preds[b])
        }

    return df


# ---------------------------------------------------------------------------- #
#                                     Tests                                    #
# ---------------------------------------------------------------------------- #
# Checks whether the dominance frontier has been computed accurately
def df_well_formed(doms, df, preds) -> bool:
    result = True
    for a, bs in df.items():
        for b in bs:
            # Check that for each B in A's dominance frontier,
            # A does not strictly dominate B
            if strictly_dominates(doms, a, b):
                result = False
                continue
            # Check that A dominates some predecessor of B
            # for each B in A's dominance frontier
            if not any(dominates(doms, a, pred) for pred in preds[b]):
                result = False

    return result


class TestDominanceFrontier(unittest.TestCase):
    def test_dom_frontiers_cs4120_example(self):
        cfg = cs4120_example()
        expected_df = {v: set() for v in cfg.keys()}
        expected_df[1] = {5, 8}
        expected_df[2] = {4}
        expected_df[3] = {4}
        expected_df[4] = {5}
        expected_df[5] = {9}
        expected_df[6] = {5}
        expected_df[7] = {8}
        expected_df[8] = {9}

        df = get_dominance_frontier(cfg)
        self.assertDictEqual(df, expected_df)

        doms = get_dominators(cfg)
        preds = get_pred_cfg(cfg)
        self.assertTrue(df_well_formed(doms, df, preds))

    def test_dom_frontiers_princeton_example(self):
        cfg = princeton_cfg()
        expected_df = {v: set() for v in cfg.keys()}
        expected_df[2] = {2}
        expected_df[3] = {3, 6}
        expected_df[4] = {6}
        expected_df[5] = {3, 6}
        expected_df[6] = {2}

        df = get_dominance_frontier(cfg)
        self.assertDictEqual(df, expected_df)

        doms = get_dominators(cfg)
        preds = get_pred_cfg(cfg)

        self.assertTrue(df_well_formed(doms, df, preds))


def post_process_df(df):
    """Converts sets to sorted lists in the values of the dominance frontier
    (for the sake of consistent formatting)"""

    new_df = {k: sorted(list(v)) for (k, v) in df.items()}
    return new_df


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
            doms = get_dominators(cfg)
            df = get_dominance_frontier(cfg)
            new_df = post_process_df(df)
            print(json.dumps(new_df, indent=2, sort_keys=True))
