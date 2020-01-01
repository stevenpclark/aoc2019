def main():
    pattern = [0, 1, 0, -1]
    with open('input.txt', 'r') as f:
        s = f.read().strip()
    #s = '12345678'
    #s = '80871224585914546619083218645595'

    if 0:
        offset = 0
        s_in = [int(c) for c in s]
        for phase in range(100):
            s_out = []
            for row in range(len(s)):
                total = 0
                for i, x in enumerate(s_in):
                    p_ind = ((i+1)//(row+1))%4
                    #print(x, pattern[p_ind])
                    total += x*pattern[p_ind]
                s_out.append(int(str(total)[-1]))
                #print()
            s_in = s_out
        print(''.join([str(x) for x in s_out[offset:offset+8]]))

    s = '03036732577212944063491565474664'
    s = s*10000
    offset = int(s[:7])
    print(offset)
    s_in = [int(c) for c in s]
    for phase in range(100):
        s_out = []
        for row in range(len(s)):
            total = 0
            for i, x in enumerate(s_in):
                p_ind = ((i+1)//(row+1))%4
                #print(x, pattern[p_ind])
                total += x*pattern[p_ind]
            s_out.append(int(str(total)[-1]))
            #print()
        s_in = s_out
    print(''.join([str(x) for x in s_out[offset:offset+8]]))

if __name__ == '__main__':
    main()
