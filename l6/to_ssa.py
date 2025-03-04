import json
import sys
from collections import Counter

from cfg import form_basic_blocks, build_cfg, get_pred_cfg


def _get_block_label(block: list[dict]) -> str:
    """Take a basic block and return an identifying label"""
    return block[0].get("label", "entry")


def _rename_vars(blocks: list[list[[dict]]]) -> list[list[[dict]]]:
    """
    Take a list of basic blocks and return a new list with all variables renamed as
    {block_label}.{variable_name}.{counter} (counter starts from 1)
    """
    renamed_blocks = blocks.copy()
    for b in renamed_blocks:
        label = _get_block_label(b)
        seen_vars_counter = Counter()
        for instr in b:
            if args := instr.get("args"):
                new_args = [f"{label}.{a}.{seen_vars_counter[a]}" for a in args]
                instr["args"] = new_args
            if dest := instr.get("dest"):
                seen_vars_counter[dest] += 1
                instr["dest"] = f"{label}.{dest}.{seen_vars_counter[dest]}"

    return renamed_blocks


def _get_function_vars(blocks: list[list[[dict]]]) -> dict[str, str]:
    """Take a list of basic blocks and return a dict mapping dest variable names to their types"""
    all_vars = {}
    for b in blocks:
        block_vars = {i["dest"]: i["type"] for i in b if "dest" in i}
        all_vars.update(block_vars)
    return all_vars


def to_ssa(blocks: list[list[[dict]]]) -> list[list[dict]]:
    cfg = build_cfg(blocks)
    all_vars = _get_function_vars(blocks)
    ssa_blocks = _rename_vars(blocks)
    for num, block in enumerate(ssa_blocks):
        label = _get_block_label(block)

        if num != 0:
            # Get the block's copy of all shadow variables
            for v, t in all_vars.items():
                get_instr = {"op": "get", "type": t, "dest": f"{label}.{v}.0"}
                block.insert(0, get_instr)

        # Set the shadow variables of all the block's successors
        seen_vars = set()
        set_instrs = []
        for instr in reversed(block):
            # The set should follow the last assign to a variable
            if dest := instr.get("dest"):
                var = dest.split(".")[1]
                if var not in seen_vars:
                    # Need a set instr for each successor
                    for succ in cfg[num]:
                        # Ignore dummy exit node
                        if succ == len(ssa_blocks):
                            continue
                        succ_label = _get_block_label(ssa_blocks[succ])
                        set_instrs.append({"op": "set", "args": [f"{succ_label}.{var}.0", dest]})
                seen_vars.add(var)
        block.extend(set_instrs)

    return ssa_blocks


if __name__ == "__main__":
    program = json.load(sys.stdin)
    for func in program["functions"]:
        bbs = form_basic_blocks(func)
        ssa = to_ssa(bbs)
        func["instrs"] = []
        for bb in ssa:
            func["instrs"].extend(bb)
        json.dump(program, sys.stdout, indent=2)