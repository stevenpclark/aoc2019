from math import ceil
import numpy as np

def to_ind(r, c):
    return c + 5*r

def is_bug(x, ind):
    return x & (1<<ind)

def display(x, nr, nc):
    print('\n')
    for r in range(nr):
        for c in range(nc):
            ind = to_ind(r,c)
            if is_bug(x, ind):
                print('#', end='')
            else:
                print('.', end='')
        print()


def part1():
    fn = 'input.txt'
    #fn = 'test.txt'
    with open(fn, 'r') as f:
        s = f.read().strip().replace('\n', '')
    x = 0
    nr, nc = 5,5
    for i, c in enumerate(s):
        if c == '#':
            x |= (1<<i)
    neighbor_map = dict()
    for r in range(nr):
        for c in range(nc):
            neighbor_inds = []
            if r > 0:
                neighbor_inds.append(to_ind(r-1,c))
            if r < nr-1:
                neighbor_inds.append(to_ind(r+1,c))
            if c > 0:
                neighbor_inds.append(to_ind(r,c-1))
            if c < nc-1:
                neighbor_inds.append(to_ind(r,c+1))
            neighbor_map[(r,c)] = neighbor_inds

    seen = set()
    while x not in seen:
        display(x, nr, nc)
        seen.add(x)
        x2 = x
        for r in range(nr):
            for c in range(nc):
                neighbor_inds = neighbor_map[(r,c)]
                num_adjacent_bugs = len([neighbor_ind for neighbor_ind in neighbor_inds if is_bug(x, neighbor_ind)])
                ind = to_ind(r,c)
                if is_bug(x, ind):
                    if num_adjacent_bugs != 1:
                        x2 &= (~(1<<ind))
                else:
                    if num_adjacent_bugs in [1,2]:
                        x2 |= (1<<ind)
        x = x2
    print(x)



def get_neighbors(r, c, d, max_d):
    neighbors = []
    #North section
    if r == 0:
        if d > 0:
            neighbors.append((1,2,d-1))
    elif (r,c) == (3,2):
        if d < max_d-1:
            for i in range(5):
                neighbors.append((4,i,d+1))
    else:
        neighbors.append((r-1,c,d))

    #West section
    if c == 0:
        if d > 0:
            neighbors.append((2,1,d-1))
    elif (r,c) == (2,3):
        if d < max_d-1:
            for i in range(5):
                neighbors.append((i,4,d+1))
    else:
        neighbors.append((r,c-1,d))

    #South section
    if r == 4:
        if d > 0:
            neighbors.append((3,2,d-1))
    elif (r,c) == (1,2):
        if d < max_d-1:
            for i in range(5):
                neighbors.append((0,i,d+1))
    else:
        neighbors.append((r+1,c,d))

    #East section
    if c == 4:
        if d > 0:
            neighbors.append((2,3,d-1))
    elif (r,c) == (2,1):
        if d < max_d-1:
            for i in range(5):
                neighbors.append((i,0,d+1))
    else:
        neighbors.append((r,c+1,d))

    return neighbors


def get_num_adjacent_bugs(r, c, d, m, max_d):
    neighbors = get_neighbors(r,c,d, max_d)

    num_adjacent_bugs = 0
    for p in neighbors:
        #print(p)
        if m[p]:
            num_adjacent_bugs += 1
    return num_adjacent_bugs
            

def part2():
    fn = 'input.txt'
    #fn = 'test.txt'
    with open(fn, 'r') as f:
        lines = [li.strip() for li in f.readlines()]

    nr, nc, nd = 5,5,20
    nd = 220
    mid_depth = nd//2
    m = np.zeros((nr,nc,nd), dtype=np.bool)

    for r in range(nr):
        for c in range(nc):
            if lines[r][c] == '#':
                m[r,c,mid_depth] = True

    for turn in range(200):
        m2 = np.copy(m)
        for d in range(nd): #TODO optimize
            for r in range(nr):
                for c in range(nc):
                    if (r,c) == (2,2):
                        continue
                    num_adjacent_bugs = get_num_adjacent_bugs(r,c,d,m, nd)
                    if m[r,c,d]:
                        if num_adjacent_bugs != 1:
                            m2[r,c,d] = False
                    else:
                        if num_adjacent_bugs in [1,2]:
                            m2[r,c,d] = True
        m = m2


    if 0:
        for d in range(max_turns+1):
            print('Depth: %d'%(d-mid_depth))
            for r in range(nr):
                for c in range(nc):
                    print({True:'#', False:'.'}[m[r,c,d]], end='')
                print()
            print()

    print(m.sum())

    if 0:
        for r in range(nr):
            for c in range(nc):
                print(r, c, len(get_neighbors(r, c, mid_depth, max_turns+1)))


if __name__ == '__main__':
    #part1()
    part2()
