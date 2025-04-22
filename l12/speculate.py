import argparse
import json
import sys
from collections import Counter
from pathlib import Path

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('trace', type=Path, help='Path of trace')
    args = parser.parse_args()
    program = json.load(sys.stdin)
    funcs = {f["name"]: f["instrs"] for f in program["functions"]}
    trace_lines = args.trace.read_text().splitlines()

    pc_seq = []
    instrs = []
    trace_counter = Counter()
    traces = {}
    for l in trace_lines:
        pc = l[:l.find(",")]
        instr = l[l.find(",")+1:]
        parsed_pc = pc.split(":")
        func = parsed_pc[0]
        i = int(parsed_pc[1])

        # We don't handle function calls
        if func not in ["main", "guard"]:
            if len(pc_seq) > 0:
                trace_counter[tuple(pc_seq)] += 1
                traces[tuple(pc_seq)] = instrs
                pc_seq = [i]
                instrs = [instr]
            else:
                continue

        # Guard instruction
        if i == -1:
            pc_seq.append(i)
            instrs.append(instr)
        # Found a backedge
        elif len(pc_seq) > 0 and i < pc_seq[-1]:
            trace_counter[tuple(pc_seq)] += 1
            traces[tuple(pc_seq)] = instrs
            pc_seq = [i]
            instrs = [instr]
        # Trace continues
        else:
            pc_seq.append(i)
            instrs.append(instr)

    hot_trace = trace_counter.most_common()[0][0]
    trace_start_pc = hot_trace[0]
    pc_to_index = [i for i, instr in enumerate(funcs["main"]) if "label" not in instr]
    trace_start_index = pc_to_index[trace_start_pc]





