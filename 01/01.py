def calc_fuel(mass, recurse=True):
    n = mass/3-2
    if n <= 0:
        return 0
    elif recurse:
        return n + calc_fuel(n)
    else:
        return n

def solve(recurse=True):
    total = 0
    with open('input.txt') as f:
        for li in f:
            total += calc_fuel(int(li), recurse)
    print(total)


if __name__ == '__main__':
    solve(recurse=False)
    solve(recurse=True)
