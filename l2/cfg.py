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
    by_name = dict()
    for i, basic_block in enumerate(basic_blocks):
        # Generate a name for the block
        if "label" in basic_block[0]:
            # The block has a label
            name = basic_block[0]["label"]
        else:
            # Make up a new name for this anonymous block
            # Base the name off of the index of the block
            name = str(i)
        by_name[name] = basic_block
    
    cfg = {}
    for i,(name,basic_block) in enumerate(by_name.items()):
        last = basic_block[-1]
        if "op" in last:
            if last["op"] in ["jmp", "br"]:
                cfg[name] = last["labels"]
            elif last["op"] in ["ret"]:
                cfg[name] = []
            else:
                if i < len(basic_blocks)-1:
                    cfg[name] = [list(by_name.keys())[i+1]]
                else:
                    cfg[name] = []
                    
    return cfg
                
def cfg():
    program = json.load(sys.stdin)
    
    # Prints the basic blocks in the program
    print('BASIC BLOCKS: ')
    for func in program["functions"]:
        for block in form_basic_blocks(func):
            print(block)
    
    # Prints the CFG 
    print('\nCONTROL FLOW GRAPH: ')
    for func in program["functions"]:
        basic_blocks = form_basic_blocks(func)
        cfg = build_cfg(basic_blocks)
        print(cfg)
        
    
if __name__ == '__main__':
    cfg()
                
                