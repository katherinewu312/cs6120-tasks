import json
import sys

from cfg import build_cfg, form_basic_blocks


def _merge_sets(sets: list[set]) -> set:
    """Return a set that is the union of the input list of sets"""
    merged = set()
    for s in sets:
        merged.union(s)
    return merged


def _live_vars_transfer(block: list[dict], out_vars: set) -> set:
    """Given a block output compute the block input using the transfer function for live variable data flow"""
    in_vars = set()
    for i, instr in enumerate(reversed(block)):
        # Remove variables that are killed
        if "dest" in instr:
            in_vars.discard(instr["dest"])
        # Add variables that are used
        if "args" in instr:
            for arg in instr["args"]:
                in_vars.add(arg)
    return in_vars


def live_variables(blocks: list[list[dict]], cfg: dict) -> tuple[dict, dict]:
    # Maps block to in set of live vars
    block_in : dict[int, set[str]] = {b: set() for b in range(len(blocks)+1)}
    # Maps block to out set of live vars
    block_out: dict[int, set[str]] = {len(blocks): set()}

    # Reverse cfg to obtain predecessor maps
    pred_cfg = {i: [] for i in range(len(blocks)+1)}
    for k, v in cfg.items():
        for i in v:
            pred_cfg[i].append(k)

    worklist = set(range(len(blocks)))
    while worklist:
        i = worklist.pop()
        block_out[i] = _merge_sets([block_in[s] for s in cfg[i]])
        orig_block_in = block_in[i]
        block_in[i] = _live_vars_transfer(blocks[i], block_out[i])
        if block_in[i] != orig_block_in:
            # block_in changed, add predecessors to worklist
            worklist.union(set(pred_cfg[i]))

    return block_in, block_out


if __name__ == "__main__":
    program = json.load(sys.stdin)
    for func in program["functions"]:
        bbs = form_basic_blocks(func)
        c = build_cfg(bbs)
        b_in, b_out = live_variables(bbs, c)
        print(func["name"])
        for bb in range(len(bbs)+1):
            print(bb)
            print(b_in[bb])
            print(b_out[bb])

