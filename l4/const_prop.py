import json
import sys
from copy import deepcopy
from typing import List, Dict, Set
from cfg import build_cfg, form_basic_blocks
from functools import reduce

import unittest
from hypothesis import given, strategies as st

# Hypothesis parameter: controls the max size of randomly generated lists/dicts
HYPOTHESIS_MAX_SIZE = 5


# Property-based tests for merge function
class TestMerge(unittest.TestCase):
    # Test that the output dict from the merge function preserves all the keys
    # in the input list of dicts
    @given(
        st.lists(
            st.dictionaries(
                st.characters(), st.integers(), max_size=HYPOTHESIS_MAX_SIZE
            ),
            max_size=HYPOTHESIS_MAX_SIZE,
        ),
    )
    def test_all_keys_present_in_merged_dict(self, dicts):
        all_keys = reduce(lambda acc, d: acc.intersection(set(d.keys())), dicts, set())
        merged_dict = const_prop_merge(dicts)
        self.assertEqual(all_keys, set(merged_dict.keys()))

    # Test whether keys mapped to different values are indeed mapped to `None`
    @given(
        st.lists(
            st.dictionaries(
                st.sampled_from(["a", "b", "c"]), st.integers(), min_size=1
            ),
            min_size=2,
            max_size=HYPOTHESIS_MAX_SIZE,
        )
    )
    def test_overlapping_keys_mapped_to_none(self, dicts):
        merged_dict = const_prop_merge(dicts)
        for key in merged_dict.keys():
            self.assertIsNone(merged_dict[key])


def const_prop_merge(dicts: List[Dict]) -> Dict:
    """Merge function for constant propagation: takes the union of all dicts
    contained within a list. Any keys that are mapped to different values
    within different dicts are automatically mapped to `None` in the output dict.

    Args:
        dicts (List[Dict]): a list of dicts

    Returns:
        Dict: the union of all the dicts
    """
    output_dict = dict()
    for d in dicts:
        for k in d.keys():
            if k in output_dict:
                if output_dict[k] != d[k]:
                    output_dict[k] = None
                else:
                    output_dict[k] = d[k]
    return output_dict


def const_prop_transfer(block: List[Dict], in_dict: Dict) -> Dict:
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


def get_predecessors(blocks: List[List[Dict]], cfg: Dict) -> Dict:
    """Creates the predecessor dictionary for a CFG,
       mapping each node's index to a list of indices for its predecesssor

    Args:
        blocks (List[List[Dict]]): a list of basic blocks
        cfg (Dict): the existing CFG

    Returns:
        Dict: Predecessor map
    """
    preds = {i: [] for i in range(len(blocks) + 1)}
    for source_node, target_nodes in cfg.items():
        for node in target_nodes:
            preds[node].append(source_node)
    return preds


# Instr = Dict[str, ...]
# Block = List[Instrs]
# CFG = Dict[Int, List[Int]] (maps each node index to a list of successors)
def const_prop(blocks: List[List[Dict]], cfg: Dict):
    entry = cfg[0]

    # Map each block to the in set of constants (initially the empty set)
    block_in = {b: set() for b in blocks}

    # Map each block to the out set of reaching defs
    block_out = {b: set() for b in blocks}

    preds = get_predecessors(blocks, cfg)

    raise NotImplementedError


if __name__ == "__main__":
    # TODO: comment out this line when done
    unittest.main()

    program = json.load(sys.stdin)
    for func in program["functions"]:
        blocks = form_basic_blocks(func)
        c = build_cfg(blocks)
    const_prop(blocks, c)
