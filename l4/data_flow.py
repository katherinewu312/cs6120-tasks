import json
import sys

from cfg import build_cfg, form_basic_blocks

def live_variables(blocks: list[list[dict]], cfg: dict) -> dict:
    # Maps block to in set of live vars
    block_in : dict[int, set] = {b: set() for b in range(len(blocks))}
    # Maps block to out set of live vars
    block_out: dict[int, set] = {len(blocks): set()}

    # Reverse cfg to obtain predecessor maps
    pred_cfg = {b: [] for b in range(len(blocks)+1)}
    for k, v in cfg.items():
        for b in v:
            pred_cfg[b].append(k)

    worklist = list(range(len(blocks)))
    return {}

if __name__ == "__main__":
    program = json.load(sys.stdin)
    for func in program["functions"]:
        bbs = form_basic_blocks(func)
        c = build_cfg(bbs)
        lvs = live_variables(bbs, c)
