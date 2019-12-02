def run_program(x):
    i = 0
    while True:
        op, a, b, c = x[i:i+4]
        if op == 99:
            break
        elif op == 1:
            x[c] = x[a]+x[b]
        elif op == 2:
            x[c] = x[a]*x[b]
        i += 4
    return x[0]



def main():
    with open('input.txt') as f:
        s = f.read()
    x_orig = [int(s2) for s2 in s.split(',')]

    x = x_orig[:]
    x[1] = 12
    x[2] = 2
    print(run_program(x))

    target = 19690720
    for noun in range(100):
        for verb in range(100):
            x = x_orig[:]
            x[1] = noun
            x[2] = verb
            if run_program(x) == target:
                print(100*noun + verb)

if __name__ == '__main__':
    main()
