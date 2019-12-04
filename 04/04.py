from collections import Counter
lower = 168630
upper = 718098

part1 = 0
part2 = 0
for i in range(lower, upper+1):
    s = list(str(i))

    if sorted(s) != s:
        continue

    counter = Counter(s)

    counts = counter.values()

    for n in counts:
        if n > 1:
            part1 += 1
            break

    if 2 in counts:
        part2 += 1

print(part1)
print(part2)
