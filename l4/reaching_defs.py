import json
import sys
from typing import List, Dict

from cfg import build_cfg, form_basic_blocks

def reaching_defs_transfer():
    raise NotImplementedError

def reaching_defs(blocks: List[List[Dict]], _cfg: Dict): 
    # Map each block to the in set of reaching defs (initially the mepty set)
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
        