import sys
import json

# Counts the number of function calls in a bril program
count = 0
program = json.load(sys.stdin)

functions = (list(program.values())[0])
for func in functions:
    for instr in func["instrs"]:
        if "op" in instr and instr["op"] == "call":
            count += 1

print(count)