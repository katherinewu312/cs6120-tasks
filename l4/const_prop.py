# pylint: disable=redefined-outer-name

import json
import sys
from copy import deepcopy
from typing import List, Dict, Set, Optional, Tuple
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


def const_prop_merge(
    dicts: List[Dict[str, Optional[int | bool]]],
) -> Dict[str, Optional[int | bool]]:
    """Merge function for constant propagation: takes the union of all dicts
    contained within a list. Any keys that are mapped to different values
    within different dicts are automatically mapped to `None` in the output dict.

    Args:
        dicts (List[Dict]): a list of dicts

    Returns:
        Dict: the union of all the dicts
    """
    output_dict: Dict[str, Optional[int | bool]] = dict()
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


def get_predecessors(
    blocks: List[List[Dict]], cfg: Dict[int, List[int]]
) -> Dict[int, List[int]]:
    """Creates the predecessor dictionary for a CFG,
       mapping each node's index to a list of indices for its predecesssor

    Args:
        blocks (List[List[Dict]]): a list of basic blocks
        cfg (Dict): the existing CFG

    Returns:
        Dict: Predecessor map
    """
    preds: Dict[int, List[int]] = {i: [] for i in range(len(blocks) + 1)}
    for source_node, target_nodes in cfg.items():
        for node in target_nodes:
            preds[node].append(source_node)
    return preds


# Instr = Dict[str, ...]
# Block = List[Instrs]
# CFG = Dict[Int, List[Int]] (maps each node index to a list of successors)
def const_prop(
    blocks: List[List[Dict]], cfg: Dict[int, List[int]]
) -> Tuple[Dict, Dict]:
    n = len(blocks)

    # Map each block to the in set of constants (initially the empty dict)
    block_in: Dict[int, Dict[str, Optional[int | bool]]] = {
        b: dict() for b in range(n + 1)
    }

    # Map all blocks to the empty dict
    block_out: Dict[int, Dict[str, Optional[int | bool]]] = {
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
    # TODO: comment out this line when done
    # unittest.main()

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
            print(f"\tin: {sorted(block_in[i])}")
            print(f"\tout: {sorted(block_out[i])}")
