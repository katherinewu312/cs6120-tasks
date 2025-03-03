import json
import sys

from cfg import form_basic_blocks, build_cfg, get_pred_cfg


def to_ssa(blocks: list[dict]) -> list[dict]:
    cfg = build_cfg(blocks)
    pred_cfg = get_pred_cfg(cfg)
    pass

if __name__ == "__main__":
    program = json.load(sys.stdin)
    for func in program["functions"]:
        bbs = form_basic_blocks(func)
        print(func["name"])
        print(func)