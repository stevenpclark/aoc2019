from math import atan2, pi, sqrt
from collections import defaultdict
import numpy as np

fn = 'input.txt'
with open(fn, 'r') as f:
    s = f.read().strip()

#print(s.count('#'))
m = np.array([list(row) for row in s.split('\n')], dtype=np.chararray)

count_tups = []

nr, nc = m.shape
#print(nr, nc)

for r1 in range(nr):
    for c1 in range(nc):
        if m[r1, c1] != '#':
            continue
        angles = set()
        for r2 in range(nr):
            for c2 in range(nc):
                if (r2 != r1 or c2 != c1) and m[r2, c2] == '#':
                    a = atan2(r2-r1, c2-c1)
                    angles.add(a)
        count_tups.append((len(angles), r1, c1))

best_count, r_base, c_base = max(count_tups)

print(best_count)
#print(r_base, c_base)

zap_map = defaultdict(list) #{angle1:[(d1, r1, c1), (d2, r2, c2), ...], angle2: [(,,), (,,), ..]}
for r2 in range(nr):
    for c2 in range(nc):
        if (r2 != r_base or c2 != c_base) and m[r2, c2] == '#':
            a = atan2(c2-c_base, -(r2-r_base))%(2*pi)
            d = sqrt((r2-r_base)**2 + (c2-c_base)**2)
            zap_map[a].append((d, r2, c2))

for radial_matches in zap_map.values():
    radial_matches.sort()


num_vaporized = 0
limit = 200
while num_vaporized < limit:
    for a in sorted(zap_map.keys()):
        radial_matches = zap_map[a]
        if radial_matches:
            match = radial_matches.pop(0)
            num_vaporized += 1
            #print(num_vaporized, match)
            if num_vaporized == limit:
                #print(match)
                print(match[2]*100+match[1])
                break


