import unittest 
from cfg_examples import cs4120_example, princeton_cfg


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



class TestGetAllPaths(unittest.TestCase):
    def test_get_all_paths_cs4120_example(self):
        cfg = cs4120_example()
        paths_to = {v: [] for v in cfg.keys()}
        paths_to[0] = [[0]]
        paths_to[1] = [[0, 1]]
        paths_to[2] = [[0, 1, 2]]
        paths_to[3] = [[0, 1, 3]]
        paths_to[4] = [[0, 1, 2, 4], [0, 1, 3, 4]]
        paths_to[5] = [[0, 1, 2, 4, 5], [0, 1, 3, 4, 5], [0, 6, 5]]
        paths_to[6] = [[0, 6]]
        paths_to[7] = [[0, 7]]
        paths_to[8] = [[0, 1, 8], [0, 7, 8]]
        paths_to[9] = [
            [0, 1, 2, 4, 5, 9],
            [0, 1, 3, 4, 5, 9],
            [0, 1, 8, 9],
            [0, 6, 5, 9],
            [0, 7, 8, 9],
        ]
        for i in cfg.keys():
            actual = get_all_paths(cfg, 0, i, [])
            self.assertListEqual(paths_to[i], actual)
    
    def test_get_all_paths_princeton(self):
        cfg = princeton_cfg()
        paths_to = {v: [] for v in cfg.keys()}
        paths_to[0] = [[0]]
        paths_to[1] = [[0, 1]]
        paths_to[2] = [[0, 1, 2]]
        paths_to[3] = [[0, 1, 2, 3]]
        paths_to[4] = [[0, 1, 2, 4]]
        paths_to[5] = [[0, 1, 2, 3, 5]]
        paths_to[6] = [[0, 1, 2, 3, 5, 6], [0, 1, 2, 4, 6]]
        paths_to[7] = [[0, 1, 2, 3, 5, 6, 7], [0, 1, 2, 4, 6, 7]]
        paths_to[8] = [[0, 1, 2, 3, 5, 6, 7, 8], [0, 1, 2, 4, 6, 7, 8]]

        for i in cfg.keys():
            actual = get_all_paths(cfg, 0, i, [])
            self.assertListEqual(paths_to[i], actual)

if __name__ == "__main__":
    unittest.main()            
    