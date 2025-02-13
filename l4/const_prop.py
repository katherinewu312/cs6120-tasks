
import json
import sys
from copy import deepcopy
from typing import List, Dict, Set

from cfg import build_cfg, form_basic_blocks

def const_prop_merge(d1: Dict, d2: Dict) -> Dict:
    """Merge function: takes the union of two dictionaries. Any keys that are 
    mapped to different values in `d1` and `d2` are mapped to `None` in the 
    output dictionary.
    """

    merged_dict = d1 | d2
    overlapping_keys = set(d1.keys()).intersection(set(d2.keys))
    keys_with_diff_values = { k for k in overlapping_keys if d1[k] != d2[k] }
    if len(keys_with_diff_values) == 0:
        return merged_dict
    else:
        # Any variables that are mapped to different values in `d1` & `d2`
        # should just be mapped to None 
        for k in keys_with_diff_values:
            merged_dict[k] = None 
        return merged_dict


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
    block_in = { b : set() for b in blocks }

    # Map each block to the out set of reaching defs 
    block_out = { b : set() for b in blocks }

    
    raise NotImplementedError 


if __name__ == "__main__":
    program = json.load(sys.stdin)
    for func in program["functions"]:
        bbs = form_basic_blocks(func)
        c = build_cfg(bbs)
        # reaching_defs(bbs, c)
        