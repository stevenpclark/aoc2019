import itertools

def run_program(x, inputs):
    i_input = 0
    outputs = []
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
            #x[x[i+1]] = int(input('? '))
            x[x[i+1]] = inputs[i_input]
            i_input += 1
            i += 2
            continue
        if op == 4:
            #print(x[x[i+1]])
            outputs.append(x[x[i+1]])
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

    return outputs


def main():
    with open('input.txt', 'r') as f:
        s = f.read()
    #s = '3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0'
    s = '3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5'
    x_orig = [int(s2) for s2 in s.split(',')]

    if 0:
        final_outputs = []
        for phases in itertools.permutations(range(5)):
            prev_output = 0
            for phase in phases:
                prev_outputs = run_program(x_orig[:], [phase, prev_output])
                assert len(prev_outputs) == 1
                prev_output = prev_outputs[0]
                #print(prev_output)
            final_outputs.append(prev_output)
        print(max(final_outputs))

    final_outputs = []
    for phases in itertools.permutations(range(5,10)):
        prev_output = 0
        for phase in phases:
            prev_outputs = run_program(x_orig[:], [phase, prev_output])
            assert len(prev_outputs) == 1
            prev_output = prev_outputs[0]
            #print(prev_output)
        final_outputs.append(prev_output)
    print(max(final_outputs))

if __name__ == '__main__':
    main()
