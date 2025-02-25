import json
import sys

from cfg import form_basic_blocks, build_cfg, get_pred_cfg

def get_dominators(cfg: dict[int, list[int]]) -> dict[int, set[int]]:
    """Computes dominators for a CFG and returns a mapping of block -> list of blocks that dominate that block"""
    dom = {k: set(cfg.keys()) for k in cfg}
    dom[0] = {0}
    pred_cfg = get_pred_cfg(cfg)

    changing = True
    while changing:
        changing = False
        for vertex in cfg:
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


def get_all_paths(cfg, src, dest, path):
    """Enumerates all paths from `src` to `dest` in the `cfg`
    - `path` is the path that has been traversed so far 
    """

    path = path + [src]
    if src == dest:
        return [path]
    if src not in cfg.keys():
        return []
    paths = []
    for neighbor in cfg[src]:
        if neighbor not in path:
            newpaths = get_all_paths(cfg, neighbor, dest, path)
            for newpath in newpaths:
                if path not in paths:
                    paths.append(newpath)
    return paths    


if __name__ == "__main__":
    program = json.load(sys.stdin)
    for func in program["functions"]:
        bbs = form_basic_blocks(func)
        c = build_cfg(bbs)
        print(func["name"])
        doms = get_dominators(c)
        print(doms)