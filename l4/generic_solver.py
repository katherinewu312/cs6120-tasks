import sys
import json
from dataclasses import dataclass
from typing import Any, Callable
from cfg import build_cfg, form_basic_blocks

from data_flow import _live_vars_transfer, _merge_sets

# Implemention of a generic solver that supports multiple analyses

@dataclass
class Analysis:
    forward: bool
    init: Any
    merge: Callable
    transfer: Callable

def dataflow(basic_blocks: list[list[dict]], _cfg: dict, analysis: Analysis):
    # Reverse cfg to obtain predecessor maps
    _pred_cfg = {i: [] for i in range(len(basic_blocks)+1)}
    for k, v in _cfg.items():
        for i in v:
            _pred_cfg[i].append(k)
    
    # Set up cfg, block_in, block_out maps and worklist
    if analysis.forward:
        cfg, pred_cfg = _cfg, _pred_cfg
        block_in : dict[int, set[str]] = {0 : analysis.init}
        block_out : dict[int, set[str]] = {b: analysis.init for b in range(len(basic_blocks) + 1)}
    else:
        # Reverse the definitions
        cfg, pred_cfg = _pred_cfg, _cfg
        block_in : dict[int, set[str]] = {len(basic_blocks): analysis.init}
        block_out: dict[int, set[str]] = {b: analysis.init for b in range(len(basic_blocks) + 1)}
    
    # Iterate through the basic blocks list
    worklist = set(range(len(basic_blocks)))
    while worklist:
        i = worklist.pop()
        block_in[i] = analysis.merge([block_out[s] for s in pred_cfg[i]])
        orig_block_out = block_out[i]
        block_out[i] = analysis.transfer(basic_blocks[i], block_in[i])
        if block_out[i] != orig_block_out:
            worklist.union(set(cfg[i]))
    
    return block_in, block_out


DF_EXAMPLES = {
    "live" : Analysis(
        forward=False,
        init=set(),
        merge=_merge_sets,
        transfer=_live_vars_transfer
    )
    
    # TODO: Implement analyses for reaching defs, constant prop, avalialble exps, etc.   
}

if __name__ == "__main__":
    program = json.load(sys.stdin)
    for func in program["functions"]:
        basic_blocks = form_basic_blocks(func)
        cfg = build_cfg(basic_blocks)
        b_in, b_out = dataflow(basic_blocks, cfg, DF_EXAMPLES[sys.argv[1]])
        print(func["name"])
        for i in range(len(basic_blocks)+1):
            if i < len(basic_blocks):
                print(basic_blocks[i][0].get("label", f"b{i}"))
            else:
                print(f"b{i}")
            print(f"in: {b_in[i]}")
            print(f"out: {b_out[i]}")