
import json
import sys
from copy import deepcopy
from typing import List, Dict, Set

from cfg import build_cfg, form_basic_blocks

def reaching_defs_transfer():
    raise NotImplementedError

def const_prop_transfer(block: List[Dict], in_dict: Dict):
    out_dict = deepcopy(in_dict)
    for instr in block:
        if "dest" in instr and "args" in instr:
            dest = instr["dest"]
            args = instr["args"]
            if args in in_dict:
                in_dict[dest] = pass # TODO: figure out what to do 
            else:
                in_dict[dest] = None 
    pass 



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
        