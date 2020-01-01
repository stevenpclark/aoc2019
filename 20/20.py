from queue import Queue
import numpy as np

class Maze(object):
    def __init__(self, f):
        lines = [list(s.strip('\n')) for s in f.readlines()]
        self.m = np.array(lines, dtype=np.chararray)
        self.num_rows, self.num_cols = self.m.shape
        self.m.shape = (self.num_rows, self.num_cols, 1)
        self.m = np.tile(self.m, (1,1,500))
        print(self.m.shape)

        teles = self.get_teles()
        tele_lookup = dict()
        tele_map = dict()
        for s, p1 in teles:
            if s == 'AA':
                self.start = p1
            elif s == 'ZZ':
                self.goal = p1
            else:
                p2 = tele_lookup.get(s, None)
                if p2:
                    tele_map[p2] = p1
                    tele_map[p1] = p2
                else:
                    tele_lookup[s] = p1

        self.tele_map = tele_map


    def get_teles(self):
        m = self.m
        teles = []

        for r in range(self.num_rows-1):
            for c in range(self.num_cols-1):
                p1 = (r,c,0)
                x1 = m[p1]
                if 'A'<=x1<='Z':
                    p2 = (r,c+1,0)
                    if 'A'<=m[p2]<='Z':
                        #horizontal
                        p3 = (r,c-1,0)
                        p4 = (r,c+2,0)
                    else:
                        #vertical
                        p2 = (r+1,c,0)
                        p3 = (r-1,c,0)
                        p4 = (r+2,c,0)
                    s = x1+m[p2]
                    for p in [p3, p4]:
                        if m[p] == '.':
                            teles.append((s, p))
                            break
                    m[p1] = 'x'
                    m[p2] = 'x'
        return teles


    def part1(self):
        m = self.m
        q = Queue()
        q.put((self.start, 0))
        while not q.empty():
            p, dist = q.get()
            if p == self.goal:
                return dist
            m[p] = 'x'
            if p in self.tele_map:
                p2 = self.tele_map[p]
                if m[p2] == '.':
                    q.put((p2, dist+1))
                    continue
            r,c,_ = p
            for p2 in [(r-1,c,0), (r+1,c,0), (r,c-1,0), (r,c+1,0)]:
                if m[p2] == '.':
                    q.put((p2, dist+1))


    def part2(self):
        m = self.m
        q = Queue()
        q.put((self.start, 0))
        while not q.empty():
            p, dist = q.get()
            if p == self.goal:
                return dist
            m[p] = 'x'
            r,c,depth = p
            tele_key = (r,c,0)
            if tele_key in self.tele_map:
                is_outer = r<=2 or c<=2 or r>=self.num_rows-3 or c>=self.num_cols-3
                if is_outer:
                    new_depth = depth-1
                else:
                    new_depth = depth+1
                if new_depth < 0:
                    continue

                r2,c2,_ = self.tele_map[tele_key]
                p2 = (r2,c2,new_depth)
                if m[p2] == '.':
                    q.put((p2, dist+1))
                    continue
            for p2 in [(r-1,c,depth), (r+1,c,depth), (r,c-1,depth), (r,c+1,depth)]:
                if m[p2] == '.':
                    q.put((p2, dist+1))


def main():
    #fn = 'test3.txt'
    fn = 'input.txt'
    with open(fn, 'r') as f:
        maze = Maze(f)

    print(maze.part1())

    with open(fn, 'r') as f:
        maze = Maze(f)
    print(maze.part2())


if __name__ == '__main__':
    main()
