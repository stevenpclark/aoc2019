def run_program(x):
    i = 0
    while True:
        #print(x)
        #print('i:', i)
        cmd = str(x[i]).rjust(5, '0')
        op = int(cmd[-2:])
        #print('cmd:', cmd)
        #print('op:', op)

        if op == 99:
            break
        if op == 3:
            x[x[i+1]] = int(input('? '))
            i += 2
            continue
        if op == 4:
            print(x[x[i+1]])
            i += 2
            continue

        modes = [int(c) for c in reversed(cmd[1:-2])]
        #print('modes:', modes)
        operands = []
        for j, mode in enumerate(modes):
            if mode == 0: #position mode
                operands.append(x[x[i+j+1]])
            elif mode == 1: #immediate mode
                operands.append(x[i+j+1])
            else:
                raise Exception('bad')
        #print('operands:', operands)

        if op == 1:
            x[x[i+3]] = operands[0] + operands[1]
            i += 4
        elif op == 2:
            x[x[i+3]] = operands[0] * operands[1]
            i += 4
        elif op == 5: #jump-if-true
            if operands[0]:
                i = operands[1]
            else:
                i += 3
        elif op == 6: #jump-if-false
            if not operands[0]:
                i = operands[1]
            else:
                i += 3
        elif op == 7: #less-than
            x[x[i+3]] = int(operands[0]<operands[1])
            i += 4
        elif op == 8: #equals
            x[x[i+3]] = int(operands[0]==operands[1])
            i += 4
        else:
            raise Exception('bad2')



def main():
    with open('input.txt') as f:
        s = f.read()
    #s = '3,0,4,0,99'
    #s = '1002,4,3,4,33'
    #s = '1101,100,-1,4,0'
    #s = '3,9,8,9,10,9,4,9,99,-1,8'
    #s = '3,9,7,9,10,9,4,9,99,-1,8'
    #s = '3,3,1108,-1,8,3,4,3,99'
    #s = '3,3,1107,-1,8,3,4,3,99'
    #s = '3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9'
    #s = '3,3,1105,-1,9,1101,0,0,12,4,12,99,1'
    #s = '3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99'
    x_orig = [int(s2) for s2 in s.split(',')]

    x = x_orig[:]
    run_program(x)
    #print(x)

if __name__ == '__main__':
    main()
