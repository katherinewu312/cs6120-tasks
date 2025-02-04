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