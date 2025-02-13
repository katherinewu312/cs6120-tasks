import json
import sys
from copy import deepcopy
from typing import List, Dict, Set
from cfg import build_cfg, form_basic_blocks


def const_prop_merge(dicts: List[Dict]) -> Dict:
    """Merge function for constant propagation: takes the union of all dicts
    contained withina list. Any keys that are mapped to different values 
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


def const_prop(blocks: List[List[Dict]], cfg: Dict):
    entry = cfg[0]

    # Map each block to the in set of reaching defs (initially the empty set)
    block_in = {b: set() for b in blocks}

    # Map each block to the out set of reaching defs
    block_out = {b: set() for b in blocks}

    raise NotImplementedError


if __name__ == "__main__":
    program = json.load(sys.stdin)
    for func in program["functions"]:
        blocks = form_basic_blocks(func)
        c = build_cfg(blocks)
        # const_prop(blocks, c)
