import json
import sys

from cfg import build_cfg, form_basic_blocks


def merge_sets(sets: list[set]) -> set:
    """Return a set that is the union of the input list of sets"""
    merged = set()
    for s in sets:
        merged.update(s)
    return merged


def live_vars_transfer(block: list[dict], out_vars: set) -> set:
    """Given a block output compute the block input using the transfer function for live variable data flow"""
    in_vars = out_vars.copy()
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

    worklist = set(range(len(blocks)+1))
    while worklist:
        i = worklist.pop()
        block_out[i] = merge_sets([block_in[s] for s in cfg[i]])
        orig_block_in = block_in[i]
        if i < len(blocks):
            block_in[i] = live_vars_transfer(blocks[i], block_out[i])
        else:
            # fake last block
            block_in[i] = block_out[i]
        if block_in[i] != orig_block_in:
            # block_in changed, add predecessors to worklist
            worklist.update(pred_cfg[i])

    return block_in, block_out


if __name__ == "__main__":
    program = json.load(sys.stdin)
    for func in program["functions"]:
        bbs = form_basic_blocks(func)
        c = build_cfg(bbs)
        b_in, b_out = live_variables(bbs, c)
        print(func["name"])
        for i in range(len(bbs)+1):
            if i < len(bbs):
                print(bbs[i][0].get("label", f"b{i}"))
            else:
                print(f"b{i}")
            print(f"\tin: {sorted(b_in[i])}")
            print(f"\tout: {sorted(b_out[i])}")
