import numpy as np

SZ = 1000
START = (SZ//2, SZ//2)

EMPTY, WALL, BLOCK, PADDLE, BALL = range(5)


NUM_OPERAND_MAP = {1:3, 2:3, 3:1, 4:1, 5:2, 6:2, 7:3, 8:3, 9:1}
def run_program(x, screen):
    x = x[:]
    i = 0
    rel_base = 0
    row, col = START
    outs = []
    num_blocks = 0
    ball_x = -1
    paddle_x = -1
    while True:
        #print(x)
        cmd = str(x[i]).rjust(5, '0')
        op = int(cmd[-2:])

        if op == 99:
            print(num_blocks)
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
            if ball_x < paddle_x:
                x[addrs[0]] = -1
            elif ball_x > paddle_x:
                x[addrs[0]] = 1
            else:
                x[addrs[0]] = 0
            i += 2
        elif op == 4:
            #print(x[addrs[0]])
            outs.append(x[addrs[0]])
            if len(outs) == 3:
                screen_x, screen_y, tile_id = outs
                if screen_x == -1 and screen_y == 0:
                    print('score: ', tile_id)
                else:
                    screen[screen_y,screen_x] = tile_id
                    if tile_id == BLOCK:
                        num_blocks += 1
                    elif tile_id == PADDLE:
                        paddle_x = screen_x
                    elif tile_id == BALL:
                        ball_x = screen_x

                outs = []
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

    screen = np.zeros((SZ,SZ), dtype=np.uint8)
    run_program(x, screen)

    if 0:
        img = 40*screen[:30, :50]
        import matplotlib.pyplot as plt
        plt.imshow(img)
        plt.show()

    screen = np.zeros((SZ,SZ), dtype=np.uint8)
    x[0] = 2
    run_program(x, screen)



if __name__ == '__main__':
    main()
