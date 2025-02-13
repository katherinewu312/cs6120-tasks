# pylint: disable=redefined-outer-name, cell-var-from-loop

import argparse
import json
import sys
from copy import deepcopy
from typing import List, Dict, Optional, Tuple
from cfg import build_cfg, form_basic_blocks
from functools import reduce

import unittest
from hypothesis import given, strategies as st

# Some type aliases to improve readibility + help with Mypy type checking

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


# Property-based tests for merge function
class TestMerge(unittest.TestCase):
    # Generates non-empty lists of random dicts
    # mapping {'a', 'b', 'c', 'd'} -> int
    char_to_int_dict = st.dictionaries(
        keys=st.sampled_from(["a", "b", "c", "d"]),
        values=st.integers(),
        min_size=1,
        max_size=5,
    )

    # Generates a list of disjoint dicts (disjoint keys & disjoint values)
    disjoint_dicts = st.lists(
        char_to_int_dict,
        min_size=2,
        unique_by=lambda d: frozenset(d.items()),
    ).filter(
        lambda dicts: all(
            len(set(d1.keys()) & set(d2.keys())) == 0
            and len(set(d1.values()) & set(d2.values())) == 0
            for i, d1 in enumerate(dicts)
            for d2 in dicts[i + 1 :]
        )
    )

    # Test that the output dict from the merge function preserves all the keys
    # in the input list of dicts
    @given(
        st.lists(
            char_to_int_dict,
            min_size=1,
            max_size=5,
        ),
    )
    def test_all_keys_present_in_merged_dict(self, dicts):
        merged_dict = const_prop_merge(dicts)
        merged_dict_keys = set(merged_dict.keys())
        for d in dicts:
            d_keys = set(d.keys())
            self.assertTrue(d_keys.issubset(merged_dict_keys))

    # Test whether keys mapped to different values are indeed mapped to `None`
    @given(
        st.lists(
            char_to_int_dict,
            min_size=2,
            max_size=5,
        )
    )
    def test_overlapping_keys_mapped_to_none(self, dicts):
        merged_dict = const_prop_merge(dicts)
        for key in merged_dict.keys():
            all_values_same = reduce(
                lambda acc, d: acc and (d[key] == merged_dict[key])
                if key in d
                else acc,
                dicts,
                True,
            )
            value_is_none = merged_dict[key] is None
            self.assertTrue(all_values_same or value_is_none)

    # Test that all key-value pairs in disjoint dicts are preserved
    @given(disjoint_dicts)
    def test_disjoint_dicts(self, dicts):
        naive_dict_union = reduce(lambda acc, d: d | acc, dicts, dict())
        merged_dict = const_prop_merge(dicts)
        self.assertEqual(naive_dict_union, merged_dict)


def const_prop_merge(
    dicts: List[Dict[Var, Optional[BrilValue]]],
) -> Dict[Var, Optional[BrilValue]]:
    """Merge function for constant propagation: takes the union of all dicts
    contained within a list. Any keys that are mapped to different values
    within different dicts are automatically mapped to `None` in the output dict.

    Args:
        dicts (List[Dict]): a list of dicts

    Returns:
        Dict: the union of all the dicts
    """
    output_dict: Dict[Var, Optional[BrilValue]] = dict()
    for d in dicts:
        for k in d.keys():
            if k in output_dict:
                if output_dict[k] != d[k]:
                    output_dict[k] = None
            else:
                output_dict[k] = d[k]
    return output_dict


def const_prop_transfer(
    block: Block, in_dict: Dict[Var, Optional[BrilValue]]
) -> Dict[Var, Optional[BrilValue]]:
    """Transfer function for constant propagation

    Args:
        block (List[Dict]): The current block we're working on
        in_dict (Dict): Input map, maps variables' names to their values
                        (if they exist, otherwise they're mapped to `None`)

    Returns:
        Dict: Updated map from variable names to (possibly `None`) values
    """

    # Python's default `copy` method creates a shallow copy, whereas
    # we want `out_dict` to be independent from `in_dict`, so we use `deepcopy`
    out_dict = deepcopy(in_dict)
    for instr in block:
        if "dest" in instr:
            dest = instr["dest"]
            if instr["op"] == "const":
                # Only handle Constant instructions
                out_dict[dest] = instr["value"]
            else:
                out_dict[dest] = None
    return out_dict


def get_predecessors(blocks: List[Block], cfg: CFG) -> Dict[Idx, List[Idx]]:
    """Creates the predecessor dictionary for a CFG,
       mapping each node's index to a list of indices for its predecesssor

    Args:
        blocks (List[List[Dict]]): a list of basic blocks
        cfg (Dict): the existing CFG

    Returns:
        Dict: Predecessor map
    """
    preds: Dict[Idx, List[Idx]] = {i: [] for i in range(len(blocks) + 1)}
    for source_node, target_nodes in cfg.items():
        for node in target_nodes:
            preds[node].append(source_node)
    return preds


def const_prop(
    blocks: List[Block], cfg: CFG
) -> Tuple[
    Dict[Idx, Dict[Var, Optional[BrilValue]]],
    Dict[Idx, Dict[Var, Optional[BrilValue]]],
]:
    """Main function that performs the constant propagation dataflow analysis

    Args:
        blocks (List[Block]): list of basic blocks
        cfg (CFG): the CFG

    Returns:
        A pair consisting of `(block_in, block_out)` (two dictionaries which map
        each block's index to a dict containing the constants in that block)
    """

    n = len(blocks)

    # Map each block's index to the in set of constants (initially the empty dict)
    block_in: Dict[Idx, Dict[Var, Optional[BrilValue]]] = {
        b: dict() for b in range(n + 1)
    }

    # Map all blocks' indices to the empty dict
    block_out: Dict[Idx, Dict[Var, Optional[BrilValue]]] = {
        b: dict() for b in range(n + 1)
    }

    preds = get_predecessors(blocks, cfg)

    worklist = set(range(len(blocks) + 1))
    while len(worklist) > 0:
        b_idx = worklist.pop()
        block_in[b_idx] = const_prop_merge([block_out[p] for p in preds[b_idx]])
        original_block_out = block_out[b_idx]
        if b_idx < n:
            block_out[b_idx] = const_prop_transfer(blocks[b_idx], block_in[b_idx])
        else:
            # Handle fake last block
            block_in[b_idx] = block_out[b_idx]
        if block_out[b_idx] != original_block_out:
            successors = cfg[b_idx]
            worklist.update(successors)

    return (block_in, block_out)


if __name__ == "__main__":
    # Set up an optional cmd-line argument `--test` that runs the test suite
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true", help="Run Hypothesis tests")
    args = parser.parse_args()

    if args.test:
        unittest.main(argv=["first-arg-is-ignored"])
    else:
        program = json.load(sys.stdin)
        for func in program["functions"]:
            blocks = form_basic_blocks(func)
            cfg = build_cfg(blocks)
            block_in, block_out = const_prop(blocks, cfg)
            for i in range(len(blocks) + 1):
                if i < len(blocks):
                    print(blocks[i][0].get("label", f"b{i}"))
                else:
                    print(f"b{i}")
                print(f"\tin: {block_in[i]}")
                print(f"\tout: {block_out[i]}")
