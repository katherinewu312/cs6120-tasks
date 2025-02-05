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


def lvn(block: list[dict]) -> list[dict]:
    """Accepts a basic block of instructions and returns a copy rewritten using LVN"""
    state = LVN([], {}, {})
    new_block = []
    for instr in block:
        if "op" not in instr:
            # Label
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
                # TODO: should break when a variable is reused later
                var = state.table[state.val_to_row[value]].var
                new_instr = {"args": [var], "dest": instr["dest"], "op": "id", "type": instr["type"]}
                state.var_to_row[instr["dest"]] = state.val_to_row[value]
            else:
                if "dest" in instr:
                    # New value
                    state.val_to_row[value] = len(state.table)
                    state.var_to_row[instr["dest"]] = len(state.table)
                    state.table.append(LVNRow(value, instr["dest"]))

                # Replace args
                new_instr = instr.copy()
                if "args" in instr:
                    new_instr["args"] = [state.table[state.var_to_row[a]].var for a in instr["args"]]

        new_block.append(new_instr)
    return new_block


if __name__ == '__main__':
    program = json.load(sys.stdin)
    for function in program['functions']:
        bbs = form_basic_blocks(function)
        new_bbs = [lvn(b) for b in bbs]
        function["instrs"] = []
        for nbb in new_bbs:
            function["instrs"].extend(nbb)
    json.dump(program, sys.stdout, indent=2)