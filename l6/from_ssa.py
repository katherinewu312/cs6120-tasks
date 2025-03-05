import json
import sys

from cfg import form_basic_blocks


def _get_var_types(blocks: list[list[dict]]) -> dict[str, str]:
    """Takes a list of basic blocks, and for every 'get' instruction, obtains the dest variable's type
    Returns a dict mapping dest variable name -> its type"""
    var_types_map = dict()
    for block in blocks:
        for instr in block:
            if "dest" in instr and instr["op"] == "get":
                var_types_map[instr["dest"]] = instr["type"]
    return var_types_map

def from_ssa(blocks: list[list[dict]]) -> list[list[dict]]:
    """Takes a list of basic blocks in SSA form and returns the same blocks converted out of SSA form"""
    var_types_map = _get_var_types(blocks)
    from_ssa_blocks = []
    for block in blocks:
        curr_block = []
        for instr in block:
            if "op" in instr and instr["op"] == "get":
                # Delete/ignore 'get' instructions
                pass
            elif "op" in instr and instr["op"] == "set":
                # Replace 'set' instructions with x: type = id y for set x y
                shadow_var, normal_var = instr["args"]
                new_instr = {"args": [normal_var], "dest": shadow_var, "op": "id", "type": var_types_map[shadow_var]}
                curr_block.append(new_instr)
            else:
                # Otherwise, preserve all other instructions
                curr_block.append(instr)
        from_ssa_blocks.append(curr_block)
                
    return from_ssa_blocks


if __name__ == "__main__":
    program = json.load(sys.stdin)
    for func in program["functions"]:
        basic_blocks = form_basic_blocks(func)
        from_ssa_blocks = from_ssa(basic_blocks)
        func["instrs"] = []
        for blocks in from_ssa_blocks:
            func["instrs"].extend(blocks)
    json.dump(program, sys.stdout, indent=2)