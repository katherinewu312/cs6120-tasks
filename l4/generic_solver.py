import sys
import json
from dataclasses import dataclass
from typing import Any, Callable
from cfg import build_cfg, form_basic_blocks

# Implemention of a generic solver that supports multiple analyses

@dataclass
class Analysis:
    forward: bool
    init: Any
    merge: Callable
    transfer: Callable

def dataflow(basic_blocks: list[list[dict]], _cfg: dict, analysis: Analysis):
    if analysis.forward:
        cfg = _cfg
        
    else:
        # Reverse cfg to obtain predecessor maps
        cfg = {i: [] for i in range(len(basic_blocks)+1)}
        for k, v in _cfg.items():
            for i in v:
                cfg[i].append(k)
    
    
    # Initialize in and out blocks
    
    # Iterate through the worklist
    
    return


DF_EXAMPLES = {
    # TODO: Implement lambdas for several examples
}

if __name__ == "__main__":
    program = json.load(sys.stdin)
    for func in program["functions"]:
        basic_blocks = form_basic_blocks(func)
        cfg = build_cfg(basic_blocks)
        df = dataflow(basic_blocks, cfg, DF_EXAMPLES[sys.argv[1]])
        
