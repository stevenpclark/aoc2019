from collections import Counter
import itertools
import re
import numpy as np

class Moon(object):
    def __init__(self, line):
        self.pos = np.array([int(s) for s in re.findall(r'[-\d]+', line)])
        self.vel = np.array([0]*len(self.pos))

    def __repr__(self):
        return '%s, %s'%(self.pos, self.vel)

    def apply_gravity(self, other):
        for i, p in enumerate(self.pos):
            p_other = other.pos[i]
            if p < p_other:
                self.vel[i] += 1
            elif p > p_other:
                self.vel[i] -= 1

    def apply_velocity(self):
        self.pos += self.vel

    def potential_energy(self):
        return np.abs(self.pos).sum()

    def kinetic_energy(self):
        return np.abs(self.vel).sum()

    def total_energy(self):
        return self.potential_energy() * self.kinetic_energy()

def step(moons):
    for m1, m2 in itertools.permutations(moons, 2):
        m1.apply_gravity(m2)
    for m in moons:
        m.apply_velocity()

def main():
    moons = []
    for li in open('input.txt', 'r'):
        moons.append(Moon(li))

    for i in range(1000):
        step(moons)
    print(sum([m.total_energy() for m in moons]))

    histories = [dict() for i in range(3)]
    max_intervals = [0]*3
    for i in range(300000):
        step(moons)

        for j in range(3):
            key = tuple(m.pos[j] for m in moons) + tuple(m.vel[j] for m in moons)
            last_i = histories[j].get(key, None)
            if last_i:
                interval = i-last_i
                if interval > max_intervals[j]:
                    max_intervals[j] = interval
            histories[j][key] = i

        i += 1

    print(np.lcm.reduce(max_intervals))


if __name__ == '__main__':
    main()
