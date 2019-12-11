import numpy as np

SZ = 1000
START = (SZ//2, SZ//2)
PAINT_MODE, MOVE_MODE = range(2)


def left(heading):
    return (-heading[1], heading[0])

def right(heading):
    return (heading[1], -heading[0])

NUM_OPERAND_MAP = {1:3, 2:3, 3:1, 4:1, 5:2, 6:2, 7:3, 8:3, 9:1}
def run_program(x, hull):
    x = x[:]
    i = 0
    rel_base = 0
    row, col = START
    heading = (-1, 0)
    bot_mode = PAINT_MODE
    painted_set = set()
    while True:
        #print(x)
        cmd = str(x[i]).rjust(5, '0')
        op = int(cmd[-2:])

        if op == 99:
            print(len(painted_set))
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
            #x[addrs[0]] = int(input('? '))
            x[addrs[0]] = hull[row,col]
            i += 2
        elif op == 4:
            #print(x[addrs[0]])
            out = x[addrs[0]]
            assert out in [0,1]
            if bot_mode == PAINT_MODE:
                hull[row,col] = out
                bot_mode = MOVE_MODE
                painted_set.add((row,col))
            else:
                if out == 0:
                    heading = left(heading)
                else:
                    heading = right(heading)
                row += heading[0]
                col += heading[1]
                #print(row, col)
                bot_mode = PAINT_MODE
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



def main():
    with open('input.txt') as f:
        s = f.read()

    #s = '109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99'
    #s = '1102,34915192,34915192,7,4,7,99,0'
    #s = '104,1125899906842624,99'
    #s = '3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99'
    x = [int(s2) for s2 in s.split(',')]

    x.extend([0]*1000000)

    hull1 = np.zeros((SZ,SZ), dtype=np.uint8)
    run_program(x, hull1)

    hull2 = np.zeros((SZ,SZ), dtype=np.uint8)
    hull2[START] = 1
    run_program(x, hull2)

    rspan, cspan = 8,60
    img = 255*hull2[SZ/2-1:SZ/2-1+rspan, SZ/2:SZ/2+cspan]

    import matplotlib.pyplot as plt
    plt.imshow(img)
    plt.show()


if __name__ == '__main__':
    main()
