import numpy as np


NUM_OPERAND_MAP = {1:3, 2:3, 3:1, 4:1, 5:2, 6:2, 7:3, 8:3, 9:1}
def run_program(x):
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
            x[addrs[0]] = inp
            i += 2
        elif op == 4:
            output.append(chr(x[addrs[0]]))
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

    



if __name__ == '__main__':
    main()
