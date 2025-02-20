import json
import sys

from cfg import form_basic_blocks, build_cfg

if __name__ == "__main__":
    program = json.load(sys.stdin)
    for func in program["functions"]:
        bbs = form_basic_blocks(func)
        c = build_cfg(bbs)
        print(func["name"])