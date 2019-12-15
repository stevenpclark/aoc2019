from math import ceil
from collections import Counter

def get_tup(s):
    strs = s.strip().split()
    #returns e.g. ("THQH", 2)
    return (strs[1], int(strs[0]))


class Reaction(object):
    def __init__(self, line):
        s1, s2 = [s.strip() for s in line.split('=>')]
        self.inputs = sorted([get_tup(s) for s in s1.split(',')])
        self.output = get_tup(s2)

    def __repr__(self):
        return '%s => %s'%(', '.join([str(tup) for tup in self.inputs]), self.output)

memo = {}

def get_min_required_ore(desired_tup, reaction_dict, excess_counter=Counter()):
    total = memo.get(desired_tup, None)
    if total is not None:
        return total

    desired_name, desired_amount = desired_tup
    reaction = reaction_dict[desired_name]
    total = 0
    output_amount = reaction.output[1]
    num_cycles = int(ceil(desired_amount/float(output_amount)))
    excess = output_amount*num_cycles - desired_amount

    for i in range(num_cycles):
        for inp_name, inp_amount in reaction.inputs:
            #first subtract from bank, if any
            banked_amount = excess_counter[inp_name]
            if banked_amount:
                withdraw_amount = min(inp_amount, banked_amount)
                #print('withdrawing %d %s from bank'%(withdraw_amount, inp_name))
                inp_amount -= withdraw_amount
                excess_counter[inp_name] -= withdraw_amount

            if inp_amount <= 0:
                continue

            if inp_name == 'ORE':
                total += inp_amount
            else:
                total += get_min_required_ore((inp_name, inp_amount), reaction_dict, excess_counter)

    #print('Need %s, will use %d cycles of %s, with %d excess'%(desired_tup, num_cycles, reaction, excess))
    consume_str = ', '.join(['%d %s'%(num_cycles*tup[1], tup[0]) for tup in reaction.inputs])
    #print('Consume %s to produce %d %s'%(consume_str, num_cycles*output_amount, desired_name))
    excess_counter[desired_name] += excess

    memo[desired_tup] = total

    return total


def main():
    #fn = 'test1.txt'
    fn = 'input.txt'
    reactions = []
    for line in open(fn, 'r'):
        reactions.append(Reaction(line))

    reaction_dict = dict()

    for r in reactions:
        output_name = r.output[0]
        assert output_name not in reaction_dict
        reaction_dict[output_name] = r

    print(get_min_required_ore(('FUEL', 1), reaction_dict))
    


if __name__ == '__main__':
    main()
