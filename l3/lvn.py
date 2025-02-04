import json
import sys

from util import form_basic_blocks


if __name__ == '__main__':
    program = json.load(sys.stdin)
    for function in program['functions']:
        bb = form_basic_blocks(function)
        print(bb)