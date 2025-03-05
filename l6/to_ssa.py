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
    dest_vars = _get_all_dest_vars(renamed_blocks)
    for b in renamed_blocks:
        label = _get_block_label(b)
        seen_vars_counter = Counter()
        for instr in b:
            if args := instr.get("args"):
                # Rename all args except function args
                new_args = [f"{label}.{a}.{seen_vars_counter[a]}" if a in dest_vars else a for a in args ]
                instr["args"] = new_args
            if dest := instr.get("dest"):
                seen_vars_counter[dest] += 1
                instr["dest"] = f"{label}.{dest}.{seen_vars_counter[dest]}"

    return renamed_blocks


def _get_all_dest_vars(blocks: list[list[[dict]]]) -> dict[str, str]:
    """Take a list of basic blocks and return a dict mapping dest variable names to their types"""
    all_vars = {}
    for b in blocks:
        block_vars = {i["dest"]: i["type"] for i in b if "dest" in i}
        all_vars.update(block_vars)
    return all_vars


def to_ssa(blocks: list[list[[dict]]], func_args: list[dict]) -> list[list[dict]]:
    """Take a list of basic blocks and return the same blocks converted to SSA form"""
    cfg = build_cfg(blocks)
    func_arg_to_type = {a["name"]: a["type"] for a in func_args}
    dest_vars = _get_all_dest_vars(blocks)
    ssa_blocks = _rename_vars(blocks)
    for num, block in enumerate(ssa_blocks):
        label = _get_block_label(block)

        if num != 0:
            # Get the block's copy of all shadow variables
            for v, t in dest_vars.items():
                get_instr = {"op": "get", "type": t, "dest": f"{label}.{v}.0"}
                block.insert(1, get_instr)  # After label
        else:
            # Handle undefined paths by explicitly setting all vars at entry
            for v, t in dest_vars.items():
                if v not in func_arg_to_type:
                    # var is undefined
                    init_instr = {"op": "undef", "type": t, "dest": f"{label}.{v}.0"}
                else:
                    # rename function argument
                    init_instr = {"op": "id", "type": func_arg_to_type[v], "dest": f"{label}.{v}.0", "args": [v]}
                if "label" in block[0]:
                    block.insert(1, init_instr)  # After label
                else:
                    block.insert(0, init_instr)


        # Set the shadow variables of all the block's successors
        seen_vars = set()
        orig_block_len = len(block)
        for i, instr in enumerate(reversed(block)):
            # The set should follow the last assign to a variable
            if dest := instr.get("dest"):
                # Parse dest to find original var name
                parsed_var = dest[len(label):].split(".")
                var = ".".join(parsed_var[1:-1])
                if var not in seen_vars:
                    # Need a set instr for each successor
                    for succ in cfg[num]:
                        # Ignore dummy exit node
                        if succ == len(ssa_blocks):
                            continue
                        succ_label = _get_block_label(ssa_blocks[succ])
                        set_instr = {"op": "set", "args": [f"{succ_label}.{var}.0", dest]}
                        block.insert(orig_block_len-i, set_instr)
                seen_vars.add(var)


    return ssa_blocks


if __name__ == "__main__":
    program = json.load(sys.stdin)
    for func in program["functions"]:
        bbs = form_basic_blocks(func)
        ssa = to_ssa(bbs, func.get("args", []))
        func["instrs"] = []
        for bb in ssa:
            func["instrs"].extend(bb)
    json.dump(program, sys.stdout, indent=2)