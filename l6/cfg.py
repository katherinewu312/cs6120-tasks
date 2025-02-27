import sys
import json

# Implements the algorithms to form basic blocks and build a control flow graph.

def form_basic_blocks(func):
    terminators = ["jmp", "br", "ret"]
    basic_blocks = []
    block = []
    for instr in func["instrs"]:
        if "op" in instr:
            block.append(instr)
            if instr["op"] in terminators:
                basic_blocks.append(block)
                block = []
        
        else:
            # sole label
            if block:
                basic_blocks.append(block)
            
            block = [instr]
    
    # implicit return
    if block:
        basic_blocks.append(block)
        
    return basic_blocks


def build_cfg(basic_blocks):
    label_to_block = dict()
    for i, basic_block in enumerate(basic_blocks):
        # Generate a name for the block
        if "label" in basic_block[0]:
            # The block has a label
            name = basic_block[0]["label"]
            label_to_block[name] = i
    
    cfg = {}
    for i,basic_block in enumerate(basic_blocks):
        last = basic_block[-1]
        if "op" in last:
            if last["op"] in ["jmp", "br"]:
                cfg[i] = [label_to_block[l] for l in last["labels"]]
            elif last["op"] in ["ret"]:
                cfg[i] = [len(basic_blocks)]
            else:
                cfg[i] = [i+1]
        else:
            cfg[i] = [i+1]

    cfg[len(basic_blocks)] = []
    return cfg


def get_pred_cfg(cfg):
    """Reverse cfg to obtain predecessor maps"""
    pred_cfg = {i: [] for i in cfg.keys()}
    for k, v in cfg.items():
        for i in v:
            pred_cfg[i].append(k)
    return pred_cfg


def flatten(xss):
    return [x for xs in xss for x in xs]

def fresh(seed, names):
    i = 1
    while True:
        name = seed + str(i)
        if name not in names:
            return name
        i += 1

def add_entry_block(basic_blocks):
    """Ensures the list of basic blocks has a unique entry block with no predecessors,
    Returns a list of potentially modified basic blocks"""
    
    # if first block has no predecessors, return original list of basic blocks
    first_block = basic_blocks[0]
    if not any('label' in d for d in first_block):
        # if first block doesn't have a label, it cannot possibly have a predecessor as it cannot be referred back to
        return basic_blocks
    else:
        # check for any references to this label
        label = first_block[0]['label']
        for instr in flatten(basic_blocks):
            if 'labels' in instr and label in instr['labels']:
                break
        else:
            return basic_blocks
    
    # if first block has predecessors, add a new block before the original first block
    new_entry_block = [{'label': fresh('entry', basic_blocks)}]
    basic_blocks.insert(0,new_entry_block)
    return basic_blocks


def map_to_block_name(basic_blocks):
    """Produces a mapping from block number in cfg -> actual block name if one exists
    If block name does not exist, generate a fresh name"""
    name_map = dict()
    for i,basic_block in enumerate(basic_blocks):
        if not any('label' in d for d in basic_block):
            name_map[i] = fresh('b', name_map.keys())
        else:
            name_map[i] = basic_block[0]['label']
    name_map[len(basic_blocks)] = 'final'
    return name_map


def cfg():
    program = json.load(sys.stdin)
    
    # Prints the basic blocks in the program
    print('BASIC BLOCKS: ')
    for func in program["functions"]:
        basic_blocks = form_basic_blocks(func)
        for block in basic_blocks:
            print(block)
    
    # Prints the CFG 
    print('\nCONTROL FLOW GRAPH: ')
    for func in program["functions"]:
        basic_blocks = form_basic_blocks(func)
        cfg = build_cfg(basic_blocks)
        print(cfg)
        
    
if __name__ == '__main__':
    cfg()
                
                