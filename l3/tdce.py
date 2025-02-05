import json
import sys
from util import form_basic_blocks

# Program for trivial dead code elimination

basic_blocks = None

def tdce_loop(func):
    global basic_blocks
    changed = False
    used = set() # for globally unused vars
    for basic_block in basic_blocks:
        for instr in basic_block:
            if 'args' in instr: 
                used.update(instr['args'])
    
    for basic_block in basic_blocks:
        last_def = dict() # for defined but unused vars (vars -> index of instr)
        for i,instr in enumerate(basic_block):                
            if 'args' in instr:
                for arg in instr['args']:
                    if arg in last_def: del last_def[arg]
            
            if 'dest' in instr:
                var = instr['dest']
                if var not in used:
                    basic_block.remove(instr)
                    changed = True
                    
                if var in last_def:
                    # var was previously defined, delete this prior instance
                    index = last_def[var]
                    del basic_block[index]
                    del last_def[var]
                    changed = True
                    
                last_def[var] = i

    return changed
    
    
def tdce():
    global basic_blocks
    program = json.load(sys.stdin)
    for func in program["functions"]:
        # initialize basic blocks for this function
        basic_blocks = form_basic_blocks(func)
        # iterate until convergence
        while tdce_loop(func):
            pass
        
        func['instrs'] = [x for xs in basic_blocks for x in xs] # flatten list
        
    json.dump(program, sys.stdout)

    
if __name__ == '__main__':
    tdce()