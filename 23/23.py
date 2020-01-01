import time
from queue import Queue, Empty
from threading import Thread
import numpy as np


NUM_OPERAND_MAP = {1:3, 2:3, 3:1, 4:1, 5:2, 6:2, 7:3, 8:3, 9:1}
class Computer(object):
    def __init__(self, code, address):
        self.x = code[:]
        self.address = address
        self.input_q = Queue()
        self.input_q.put([address])

        self.i = 0
        self.rel_base = 0

        self.computers = []


    def enqueue(self, a, b):
        #print('%d enqueuing %d, %d'%(self.address, a, b))
        self.input_q.put([a,b])


    def run(self):
        #print('starting %d'%self.address)
        x = self.x
        i = self.i
        inputs = []
        outputs = []
        
        while True:
            cmd = str(x[i]).rjust(5, '0')
            op = int(cmd[-2:])

            if op == 99:
                break

            modes = [int(c) for c in reversed(cmd[0:-2])]

            addrs = []
            num_operands = NUM_OPERAND_MAP[op]
            for j, mode in enumerate(modes[:num_operands]):
                if mode == 0: #position mode
                    addrs.append(x[i+j+1])
                elif mode == 1: #immediate mode
                    addrs.append(i+j+1)
                elif mode == 2: #relative mode
                    addrs.append(self.rel_base + x[i+j+1])
                else:
                    raise Exception('bad')

            if op == 1:
                x[addrs[2]] = x[addrs[0]] + x[addrs[1]]
                i += 4
            elif op == 2:
                x[addrs[2]] = x[addrs[0]] * x[addrs[1]]
                i += 4
            elif op == 3:
                if inputs:
                    inp = inputs.pop()
                else:
                    try:
                        inputs = self.input_q.get(block=False)
                        print('%d got: %s' %(self.address, inputs))
                        inp = inputs.pop()
                    except Empty:
                        inp = -1
                x[addrs[0]] = inp
                i += 2
            elif op == 4:
                output = x[addrs[0]]
                outputs.append(output)
                i += 2
                if len(outputs) == 3:
                    addr, a, b = outputs
                    print('%d -> %d: %d %d'%(self.address, addr, a, b))
                    if addr == 255:
                        print(a,b)
                    self.computers[addr].enqueue(a,b)
                    time.sleep(0.1)
            elif op == 5: #jump-if-true
                if x[addrs[0]]:
                    i = x[addrs[1]]
                else:
                    i += 3
            elif op == 6: #jump-if-false
                if not x[addrs[0]]:
                    i = x[addrs[1]]
                else:
                    i += 3
            elif op == 7: #less-than
                x[addrs[2]] = int(x[addrs[0]]<x[addrs[1]])
                i += 4
            elif op == 8: #equals
                x[addrs[2]] = int(x[addrs[0]]==x[addrs[1]])
                i += 4
            elif op == 9:
                self.rel_base += x[addrs[0]]
                i += 2
            else:
                raise Exception('bad2')

        self.i = i

        print('%d exiting'%self.address)


def main():
    with open('input.txt') as f:
        s = f.read()

    code = [int(s2) for s2 in s.split(',')]

    code.extend([0]*10000)

    computers = [Computer(code, addr) for addr in range(50)]

    for c in computers:
        c.computers = computers

    threads = []
    for c in computers:
        threads.append(Thread(target=c.run))

    for t in threads:
        t.start()

    #run_program(code)


if __name__ == '__main__':
    main()
