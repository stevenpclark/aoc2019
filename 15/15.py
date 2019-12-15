import random
import numpy as np

SZ = 1000
START = (SZ//2, SZ//2)

UNKNOWN = 10000
WALL = 8000
FLOODED = 7000

BLOCKED = 0
MOVED = 1
MOVED_AND_FOUND = 2

NORTH, SOUTH, WEST, EAST = range(1,5)

NUM_OPERAND_MAP = {1:3, 2:3, 3:1, 4:1, 5:2, 6:2, 7:3, 8:3, 9:1}
def run_program(x, world):
    x = x[:]
    i = 0
    rel_base = 0
    row, col = START
    world[START] = 0
    dist = 0
    last_inp = None
    while True:
        #print(x)
        cmd = str(x[i]).rjust(5, '0')
        op = int(cmd[-2:])

        if op == 99:
            break

        modes = [int(c) for c in reversed(cmd[0:-2])]
        #print('modes:', modes)

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

        #print('i: %04d  cmd: %s  op: %d  rel_base: %d  addrs: %s'%(i, cmd, op, rel_base, addrs))

        if op == 1:
            x[addrs[2]] = x[addrs[0]] + x[addrs[1]]
            i += 4
        elif op == 2:
            x[addrs[2]] = x[addrs[0]] * x[addrs[1]]
            i += 4
        elif op == 3:
            #INPUT
            if world[row-1, col] == UNKNOWN:
                inp = NORTH
            elif world[row+1, col] == UNKNOWN:
                inp = SOUTH
            elif world[row, col-1] == UNKNOWN:
                inp = WEST
            elif world[row, col+1] == UNKNOWN:
                inp = EAST
            else:
                inp = random.randint(1,4)
            x[addrs[0]] = inp
            last_inp = inp
            i += 2
        elif op == 4:
            #RESPONSE
            response = x[addrs[0]]
            if response == BLOCKED:
                if last_inp == NORTH:
                    world[row-1, col] = WALL
                elif last_inp == SOUTH:
                    world[row+1, col] = WALL
                elif last_inp == WEST:
                    world[row, col-1] = WALL
                else:
                    world[row, col+1] = WALL
            else:
                if last_inp == NORTH:
                    row -= 1
                elif last_inp == SOUTH:
                    row += 1
                elif last_inp == WEST:
                    col -= 1
                else:
                    col += 1

                dist = min(dist+1, world[row, col])
                world[row, col] = dist

                #print(dist, row, col)

                if response == MOVED_AND_FOUND:
                    world[row, col] = 3
                    print('arrived at oxygen system: %s in %d moves'%((row, col), dist))
                    return (row, col)
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

def flood_fill(world, r, c, depth):
    max_depth = depth
    world[r,c] = FLOODED
    for r2, c2 in ((r-1,c), (r,c-1), (r+1,c), (r,c+1)):
        if world[r2,c2] < FLOODED:
            max_depth = max(max_depth, flood_fill(world, r2, c2, depth+1))
    return max_depth



def main():
    random.seed(42)

    with open('input.txt') as f:
        s = f.read()

    #s = '109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99'
    #s = '1102,34915192,34915192,7,4,7,99,0'
    #s = '104,1125899906842624,99'
    #s = '3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99'
    x = [int(s2) for s2 in s.split(',')]

    x.extend([0]*1000000)

    world = UNKNOWN*np.ones((SZ,SZ), dtype=np.uint16)
    end_row, end_col = run_program(x, world)

    world[START] = 2

    if 1:
        r1, c1 = START
        span = 30
        img = world[r1-span:r1+span, c1-span:c1+span]
        import matplotlib.pyplot as plt
        plt.imshow(img)
        plt.show()

    max_depth = flood_fill(world, end_row, end_col, 0)
    print(max_depth)


if __name__ == '__main__':
    main()
