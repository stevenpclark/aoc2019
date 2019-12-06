def main():
    with open('input.txt', 'r') as f:
        lines = f.readlines()

    d = dict()

    for li in lines:
        s1, s2 = li.strip().split(')')
        d[s2] = s1

    total_links = 0
    for s2,s1 in d.items():
        while s1:
            total_links += 1
            s1 = d.get(s1, None)

    print(total_links)

    santa_distance = dict()
    s1 = d['SAN']
    n = 0
    while s1:
        santa_distance[s1] = n
        n += 1
        s1 = d.get(s1, None)

    s1 = d['YOU']
    n = 0
    while s1:
        if s1 in santa_distance:
            print(n+santa_distance[s1])
            break
        n += 1
        s1 = d.get(s1, None)


if __name__ == '__main__':
    main()
