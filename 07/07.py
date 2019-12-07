import itertools

class Amplifier(object):
    def __init__(self, x, phase):
        self.x = x[:]
        self.inputs = [phase]
        self.i = 0

    def get_output(self, input):
        self.inputs.append(input)
        i = self.i
        x = self.x
        while True:
            cmd = str(x[i]).rjust(5, '0')
            op = int(cmd[-2:])

            if op == 99:
                return None
            if op == 3:
                x[x[i+1]] = self.inputs.pop(0)
                i += 2
                continue
            if op == 4:
                output = x[x[i+1]]
                i += 2
                #save state here
                self.i = i
                return output

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

def get_max_output(x, phase_range, do_loop):
    final_outputs = []
    for phases in itertools.permutations(phase_range):
        amps = [Amplifier(x, phase) for phase in phases]
        prev_output = 0
        while True:
            for amp in amps:
                prev_output = amp.get_output(prev_output)
            if prev_output is not None:
                final_output = prev_output
            if not do_loop or prev_output is None:
                break
        final_outputs.append(final_output)
    return max(final_outputs)


def main():
    with open('input.txt', 'r') as f:
        s = f.read()
    #s = '3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0'
    #s = '3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5'
    x = [int(s2) for s2 in s.split(',')]

    print(get_max_output(x, range(5), do_loop=False))
    print(get_max_output(x, range(5,10), do_loop=True))


if __name__ == '__main__':
    main()
