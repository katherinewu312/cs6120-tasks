import json
import sys

from cfg import form_basic_blocks, build_cfg, get_pred_cfg, add_entry_block
from dfs import get_all_paths


def get_dominators(cfg: dict[int, list[int]]) -> dict[int, set[int]]:
    """Computes dominators for a CFG and returns a mapping of block -> list of blocks that dominate that block"""
    clean_cfg = cfg.copy()
    _prune_unreachable_blocks(clean_cfg)
    dom = {k: set(clean_cfg.keys()) for k in clean_cfg}
    dom[0] = {0}
    pred_cfg = get_pred_cfg(clean_cfg)

    changing = True
    while changing:
        changing = False
        for vertex in clean_cfg:
            initial_doms = dom[vertex]
            if vertex == 0:
                continue
            pred_vertices = pred_cfg[vertex]
            pred_doms = dom[pred_vertices[0]]
            for v in pred_vertices[1:]:
                pred_doms = pred_doms.intersection(dom[v])
            dom[vertex] = {vertex}.union(pred_doms)
            if initial_doms != dom[vertex]:
                changing = True

    return dom


def _prune_unreachable_blocks(cfg:dict[int, list[int]]) -> None:
    # Remove unreachable blocks
    # e.g. https://cs6120.zulipchat.com/#narrow/channel/254729-general/topic/is-decreasing.2Ebril.20dominance.20frontier
    unreachable = []
    pred_cfg = get_pred_cfg(cfg)
    for b in pred_cfg:
        if b != 0 and not pred_cfg[b]:
            unreachable.append(b)
    for b in unreachable:
        del cfg[b]


if __name__ == "__main__":
    program = json.load(sys.stdin)
    for func in program["functions"]:
        bbs = form_basic_blocks(func)
        bbs = add_entry_block(bbs)
        c = build_cfg(bbs)
        pc = get_pred_cfg(c)
        print(func["name"])
        doms = get_dominators(c)
        print(doms)
        
        # Use DFS to find all paths from entry and compare to dominators
        for k,v in doms.items():
            paths = get_all_paths(c, 0, k, [])
            dfs_doms = set(paths[0])
            for p in paths[1:]:
                dfs_doms = dfs_doms.intersection(p)
            assert set(v) == dfs_doms