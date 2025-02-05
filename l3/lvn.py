import json
import sys
from dataclasses import dataclass

from util import form_basic_blocks

@dataclass
class LVNRow:
    value: tuple
    var: str

@dataclass
class LVN:
    table: list[LVNRow]
    var_to_row: dict[str, int] # Maps from a variable to a table index
    val_to_row: dict[tuple, int] # Maps from a value to a table index


def lvn(block: list[dict], reserved_vars: set[str]) -> list[dict]:
    """Accepts a basic block and a set of reserved variable names and returns a copy rewritten using LVN"""
    state = LVN([], {}, {})
    new_block = []
    for index, instr in enumerate(block):
        if "op" not in instr or instr["op"] == "jmp":
            # Label or jump
            new_instr = instr
        else:
            if instr["op"] == "const":
                # const instructions have an explicit value
                value = (instr["op"], instr["value"])
            else:
                # Other instructions we map arguments to rows in the table
                # Handle unknown variables which must have been defined in a prior block
                for var in [a for a in instr["args"] if a not in state.var_to_row]:
                    state.var_to_row[var] = len(state.table)
                    state.table.append(LVNRow((), var))
                value = (instr["op"], *[state.var_to_row[v] for v in instr["args"]])

            if value in state.val_to_row:
                # Value has been computed before
                var = state.table[state.val_to_row[value]].var
                new_instr = {"args": [var], "dest": instr["dest"], "op": "id", "type": instr["type"]}
                state.var_to_row[instr["dest"]] = state.val_to_row[value]
            else:
                new_instr = instr.copy()
                if "dest" in instr:
                    # Check if dest is overwritten later, conservatively assume value will be different
                    var_overwrites = [i["dest"] for i in block[index+1:] if "dest" in i]
                    if instr["dest"] in var_overwrites:
                        # Generate new variable name
                        attempt = 1
                        new_dest = f"{instr['dest']}_{attempt}"
                        while new_dest in reserved_vars:
                            attempt += 1
                            new_dest = f"{instr['dest']}_{attempt}"
                        reserved_vars.add(new_dest)
                    else:
                        new_dest = instr["dest"]
                    new_instr["dest"] = new_dest

                    # New value
                    state.val_to_row[value] = len(state.table)
                    state.var_to_row[new_dest] = len(state.table)
                    state.table.append(LVNRow(value, new_dest))

                # Replace args
                if "args" in instr:
                    new_instr["args"] = [state.table[state.var_to_row[a]].var for a in instr["args"]]

        new_block.append(new_instr)
    return new_block


if __name__ == '__main__':
    program = json.load(sys.stdin)
    for function in program['functions']:
        bbs = form_basic_blocks(function)
        rvs = set(instr["dest"] for instr in function["instrs"] if "dest" in instr)
        new_bbs = [lvn(b, rvs) for b in bbs]
        function["instrs"] = []
        for nbb in new_bbs:
            function["instrs"].extend(nbb)
    json.dump(program, sys.stdout, indent=2)