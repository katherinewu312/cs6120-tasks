import argparse
import json
import sys
from collections import Counter
from pathlib import Path
import subprocess

'''
Usage: 
$ python3 speculate.py --trace <filename>, must supply trace file obtained from a prior 'deno run brili.ts [-p args]' command.
If using this command, must first run
    $ bril2json < test.bril | deno run brili.ts [-p args]
    to then run
    $ bril2json < test.bril | python3 speculate.py --trace trace.txt

$ python3 speculate.py --run-brili [-p args], avoids hard-coding trace.txt as an argument to speculate.py
Does the speculative optimization in one command instead of two, unlike the above.
'''

if __name__ == "__main__":    
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--trace", type=Path, help="Path of the trace file")
    group.add_argument("--run-brili-ts", action="store_true", help="Run brili.ts")
    parser.add_argument('-p', '--params', nargs='*', help='Arguments to pass to brili.ts')
    args = parser.parse_args()
    
    program = json.load(sys.stdin)
    funcs = {f["name"]: f["instrs"] for f in program["functions"]}

    if args.trace:
        trace_lines = args.trace.read_text().splitlines()

    elif args.run_brili_ts:
        cmd = ["deno", "run", "--allow-write", "brili.ts"]
        if args.params:
            cmd.append("-p")
            cmd.extend(args.params)
        subprocess.run(cmd, input=json.dumps(program), text=True, stdout=subprocess.DEVNULL, stderr = subprocess.DEVNULL)
        with open('trace.txt', 'r') as trace_file:
            trace_lines = trace_file.read().splitlines()

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
    trace_start_index = hot_trace[0]
    trace_end_index = hot_trace[-1] + 1

    stitched_instrs.insert(trace_end_index, {"label": "hotpathsuccess"})

    trace_to_stitch.insert(0, {"op": "speculate"})
    trace_to_stitch.append({"op": "commit"})
    trace_to_stitch.append({"op": "jmp", "labels": ["hotpathsuccess"]})
    trace_to_stitch.append({"label": "hotpathfail"})

    stitched_instrs[trace_start_index:trace_start_index] = trace_to_stitch
    for func in program["functions"]:
        if func["name"] == "main":
            func["instrs"] = stitched_instrs

    # print(stitched_instrs)

    json.dump(program, sys.stdout, indent=2)


