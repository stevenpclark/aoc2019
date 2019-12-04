import numpy as np

SZ = 40000
dtype = np.uint16
start = (SZ//2, SZ//2)
d_map = {'U':np.array((-1,0)),
         'D': np.array((1,0)),
         'L': np.array((0,-1)), 
         'R': np.array((0,1))}


def get_positions(pos, move):
    d = d_map[move[0]]
    n = int(move[1:])
    positions = []
    for i in range(n):
        pos += d
        positions.append(tuple(pos))
    return positions


def solve(fn):
    with open(fn, 'r') as f:
        s = f.read().strip()
    wire1, wire2 = s.split('\n')

    m = np.zeros((SZ,SZ), dtype=dtype)
    tail = start
    n = 0
    for move in wire1.split(','):
        positions = get_positions(tail, move)
        for i, p in enumerate(positions):
            dist = 1 + i + n
            if m[p] == 0:
                m[p] = dist
        tail = positions[-1]
        n += len(positions)

    #print(m)

    part1 = []
    part2 = []
    tail = start
    n = 0
    for move in wire2.split(','):
        positions = get_positions(tail, move)
        for i, p in enumerate(positions):
            dist = 1 + i + n
            if m[p] > 0:
                part1.append(p)
                part2.append(dist+m[p])
        tail = positions[-1]
        n += len(positions)

    part1 = [abs(r-start[0])+abs(c-start[1]) for r,c in part1]
    print(min(part1))
    print(min(part2))


if __name__ == '__main__':
    fn = 'input.txt'
    solve(fn)
