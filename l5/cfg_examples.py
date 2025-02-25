
# ---------------------------------------------------------------------------- #
#                              Some example CFGs                               #
# ---------------------------------------------------------------------------- #

# CFG example from CS 4120 lecture notes
# https://www.cs.cornell.edu/courses/cs4120/2023sp/notes.html?id=reachdef
#
#                    (7)
#                     |
#                     v
#    (1)------------>(8)
#    / \
#   /   \
#  v     v
# (2)   (3)
#  \     /
#   \   /
#    v v
#    (4)
#     |
#     v
#    (5)<---(6)
# 
def cs4120_example():
    nodes = list(range(10))
    cfg = {v: [] for v in nodes}
    cfg[1] = [2, 3, 8]
    cfg[2] = [4]
    cfg[3] = [4]
    cfg[4] = [5]
    cfg[6] = [5]
    cfg[7] = [8]

    # 0 is a dummy initial block whose successors are all the "real"
    # entry blocks in the CFG
    cfg[0] = [1, 6, 7]

    # 9 is dummy final block whose predecessors are all the "real"
    # final blocks in the CFG
    cfg[5] = [9]
    cfg[8] = [9]
    cfg[9] = []

    return cfg


# CFG example taken from Princeton COS 320 slides
# https://www.cs.princeton.edu/courses/archive/spring22/cos320/lectures/ssa.pdf
# 
#        1
#        |
#        v
#        2
#       / \
#      v   v
#     3     4
#    ^ \    ^
#    |  |   |
#    |  |   |
#    | /    |
#    | v    v
#     5 --> 6 
#        |
#        v
#        7
# 
def princeton_cfg():
    nodes = list(range(9))

    cfg = {v: [] for v in nodes}
    cfg[1] = [2]
    cfg[2] = [3, 4]
    cfg[3] = [5]
    cfg[4] = [6]
    cfg[5] = [3, 6]
    cfg[6] = [2, 7]

    # Dummy initial block
    cfg[0] = [1]

    # Dummy final block
    cfg[7] = [8]
    cfg[8] = []
    return cfg