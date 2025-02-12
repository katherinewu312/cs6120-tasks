# TODO: maybe switch to const prop? (its supposed to be easier)

import json
import sys
from typing import List, Dict, Set

from cfg import build_cfg, form_basic_blocks

def reaching_defs_transfer():
    raise NotImplementedError

def get_defs(block: List[Dict]) -> Set[str]:
    """Returns the set of variables that were defined in a block"""
    defns = set()
    for instr in block:
        if instr["dest"]:
            defns.add(instr["dest"])
    return defns


def get_kills(_block: List[Dict], _existing_defns: Set[str]) -> Set[str]:
    """Returns the set of kills in a block"""
    pass 

def reaching_defs(blocks: List[List[Dict]], cfg: Dict): 
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
        