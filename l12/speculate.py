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

    # Every time there's aa backedge, we start a new sequence of PCs
    # We count which sequence of PCs separated by a backedge happens most frequently
    pc_seq = []
    instrs = []
    trace_counter = Counter()
    traces = {}
    for l in trace_lines:
        pc = l[:l.find(",")]
        instr = json.loads(l[l.find(",")+1:])
        parsed_pc = pc.split(":")
        func = parsed_pc[0]
        i = int(parsed_pc[1])

        # Truncate the candidate sequences of PCs when we encounter a function call,
        # or if we see an effect operation like print / ret
        if func not in ["main", "guard"] or instr["op"] in ("print", "ret"):
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
    pc_to_index = [i for i, instr in enumerate(funcs["main"]) if "label" not in instr]
    trace_to_stitch = traces[hot_trace]
    stitched_instrs = funcs["main"].copy()
    trace_start_index = pc_to_index[hot_trace[0]]
    trace_end_index = pc_to_index[hot_trace[-1]]

    stitched_instrs.insert(trace_end_index, {"label": "hotpathsuccess"})

    trace_to_stitch.insert(0, {"op": "speculate"})
    trace_to_stitch.append({"op": "commit"})
    trace_to_stitch.append({"op": "jmp", "labels": ["hotpathsuccess"]})
    trace_to_stitch.append({"label": "hotpathfail"})

    stitched_instrs[trace_start_index-1:trace_start_index-1] = trace_to_stitch
    for func in program["functions"]:
        if func["name"] == "main":
            func["instrs"] = stitched_instrs

    # print(stitched_instrs)

    json.dump(program, sys.stdout, indent=2)


