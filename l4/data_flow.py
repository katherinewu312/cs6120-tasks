import json
import sys

from cfg import build_cfg, form_basic_blocks

def live_variables(blocks: list[dict], cfg: dict) -> dict:
    """TODO"""
    raise NotImplementedError

if __name__ == "__main__":
    program = json.load(sys.stdin)
    for func in program["functions"]:
        bbs = form_basic_blocks(func)
        c = build_cfg(bbs)

