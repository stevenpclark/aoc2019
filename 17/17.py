import numpy as np


NUM_OPERAND_MAP = {1:3, 2:3, 3:1, 4:1, 5:2, 6:2, 7:3, 8:3, 9:1}
def run_program(x, inputs=None):
    x = x[:]
    i = 0
    rel_base = 0
    output = []

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
            inp = inputs.pop(0)
            print(chr(inp), end='')
            x[addrs[0]] = inp
            i += 2
        elif op == 4:
            print(x[addrs[0]])
            outp = chr(x[addrs[0]])
            #print(outp, end='')
            output.append(outp)
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
    return ''.join(output).strip()


def main():
    with open('input.txt') as f:
        s = f.read()

    x = [int(s2) for s2 in s.split(',')]

    x.extend([0]*10000)

    s = run_program(x)
    print(s)
    s = [list(s2) for s2 in s.split('\n')]

    m = np.array(s, dtype=np.chararray)
    print(m.shape)
    num_rows, num_cols = m.shape
    v = 0
    for r in range(1,num_rows-1):
        for c in range(1,num_cols-1):
            if m[r,c] == m[r-1,c] == m[r+1,c] == m[r,c-1] == m[r,c+1] == '#':
                v += r*c
    print(v)



    x[0] = 2
    inputs = list()
    inputs.extend(['A,B,A,C,A,B,C,B,C,B'])
    inputs.extend(['R,10,R,10,R,6,R,4'])
    inputs.extend(['R,10,R,10,L,4'])
    inputs.extend(['R,4,L,4,L,10,L,10'])
    inputs.extend(['n\n'])
    inputs = '\n'.join(inputs)
    print(inputs)
    inputs = [ord(c) for c in inputs]
    print(inputs)
    s = run_program(x, inputs)

    



if __name__ == '__main__':
    main()
