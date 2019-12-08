import numpy as np

with open('input.txt', 'r') as f:
    s = f.read().strip()

#s = '0222112222120000'
nr = 6
nc = 25

x = [int(c) for c in s]

d = np.array(x)
d = np.reshape(d, (-1, nr, nc))
nb = d.shape[0]


tups = []
for b in range(nb):
    band = d[b,:,:]
    unique, counts = np.unique(band, return_counts=True)
    tups.append(list(counts))

tups.sort()
print(tups[0][1]*tups[0][2])


for r in range(nr):
    for c in range(nc):
        for b in range(nb):
            v = d[b,r,c] 
            if v != 2:
                break
        print({0:' ', 1:'X', 2:'.'}[v], end='')
    print('\n', end='')

