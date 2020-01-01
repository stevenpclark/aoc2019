import random
import itertools
import numpy as np

SZ = 50

NUM_OPERAND_MAP = {1:3, 2:3, 3:1, 4:1, 5:2, 6:2, 7:3, 8:3, 9:1}
def run_program(x, inps):
    x = x[:]
    i = 0
    rel_base = 0
    num_affected = 0
    while True:
        cmd = str(x[i]).rjust(5, '0')
        op = int(cmd[-2:])

        if op == 99:
            break

        modes = [int(c) for c in reversed(cmd[0:-2])]

        addrs = []
        num_operands = NUM_OPERAND_MAP[op]
        for j, mode in enumerate(modes[:num_operands]):
            if mode == 0: #position mode
                addrs.append(x[i+j+1])
            elif mode == 1: #immediate mode
                addrs.append(i+j+1)
            elif mode == 2: #relative mode
                addrs.append(rel_base + x[i+j+1])
            else:
                raise Exception('bad')

        if op == 1:
            x[addrs[2]] = x[addrs[0]] + x[addrs[1]]
            i += 4
        elif op == 2:
            x[addrs[2]] = x[addrs[0]] * x[addrs[1]]
            i += 4
        elif op == 3:
            #INPUT
            inp = inps.pop()
            x[addrs[0]] = inp
            i += 2
        elif op == 4:
            output = x[addrs[0]]
            num_affected += output
            i += 2
        elif op == 5: #jump-if-true
            if x[addrs[0]]:
                i = x[addrs[1]]
            else:
                i += 3
        elif op == 6: #jump-if-false
            if not x[addrs[0]]:
                i = x[addrs[1]]
            else:
                i += 3
        elif op == 7: #less-than
            x[addrs[2]] = int(x[addrs[0]]<x[addrs[1]])
            i += 4
        elif op == 8: #equals
            x[addrs[2]] = int(x[addrs[0]]==x[addrs[1]])
            i += 4
        elif op == 9:
            rel_base += x[addrs[0]]
            i += 2
        else:
            raise Exception('bad2')
    return num_affected


def main():
    random.seed(42)

    with open('input.txt') as f:
        s = f.read()

    #s = '109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99'
    #s = '1102,34915192,34915192,7,4,7,99,0'
    #s = '104,1125899906842624,99'
    #s = '3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99'
    prog = [int(s2) for s2 in s.split(',')]

    prog.extend([0]*100)
    num_affected = 0
    for y in range(50):
        for x in range(50):
            num_affected += run_program(prog, [x,y])
    print(num_affected)


    found = False
    for y in range(1209,1300):
        for x in range(int(1.5*y), y, -1):
            if run_program(prog, [x,y]) and run_program(prog, [x-99,y+99]):
                sx = x-99
                sy = y
                print(sx,sy, sx*10000+sy)
                found = True
                break
        if found:
            break

    print(sx, sy)

    print(fits(prog, sx, sy))
    print(fits(prog, sx-1, sy))
    print(fits(prog, sx-1, sy-1))
    print(fits(prog, sx-2, sy-1))
    print(fits(prog, sx-1, sy-2))
    print(fits(prog, sx-1, sy+1))
    print(fits(prog, sx+1, sy+1))
    print(fits(prog, sx-2, sy+2))



def fits(prog, sx, sy):
    return run_program(prog, [sx+99, sy]) and run_program(prog, [sx, sy+99])



if __name__ == '__main__':
    main()
