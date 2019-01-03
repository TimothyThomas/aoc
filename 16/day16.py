import sys
from pathlib import Path
from collections import namedtuple

lines = [l for l in Path('input.txt').read_text().split('\n') if l]

Sample = namedtuple('Sample', ['inp', 'op', 'res'])

samples = []


for i, line in enumerate(lines):
    if not i%3 == 0:
        continue
    inp = tuple([int(v) for v in line.split('[')[-1].rstrip(']').split(', ')])
    op = tuple([int(v) for v in lines[i+1].split()])
    res = tuple([int(v) for v in lines[i+2].split('[')[-1].rstrip(']').split(', ')])
    samples.append(Sample(inp, op, res))



def addr(inreg, instruction):
    op, a, b, c = instruction
    outreg = list(inreg)
    outreg[c] = inreg[a] + inreg[b]
    return tuple(outreg)

def addi(inreg, instruction):
    op, a, b, c = instruction
    outreg = list(inreg)
    outreg[c] = inreg[a] + b 
    return tuple(outreg)

def mulr(inreg, instruction):
    op, a, b, c = instruction
    outreg = list(inreg)
    outreg[c] = inreg[a] * inreg[b]
    return tuple(outreg)

def muli(inreg, instruction):
    op, a, b, c = instruction
    outreg = list(inreg)
    outreg[c] = inreg[a] * b 
    return tuple(outreg)

def banr(inreg, instruction):
    op, a, b, c = instruction
    outreg = list(inreg)
    outreg[c] = inreg[a] & inreg[b] 
    return tuple(outreg)

def bani(inreg, instruction):
    op, a, b, c = instruction
    outreg = list(inreg)
    outreg[c] = inreg[a] & b 
    return tuple(outreg)

def borr(inreg, instruction):
    op, a, b, c = instruction
    outreg = list(inreg)
    outreg[c] = inreg[a] | inreg[b] 
    return tuple(outreg)

def bori(inreg, instruction):
    op, a, b, c = instruction
    outreg = list(inreg)
    outreg[c] = inreg[a] | b 
    return tuple(outreg)

def setr(inreg, instruction):
    op, a, b, c = instruction
    outreg = list(inreg)
    outreg[c] = inreg[a]
    return tuple(outreg)

def seti(inreg, instruction):
    op, a, b, c = instruction
    outreg = list(inreg)
    outreg[c] = a 
    return tuple(outreg)

def gtir(inreg, instruction):
    op, a, b, c = instruction
    outreg = list(inreg)
    outreg[c] = 1 if a > inreg[b] else 0 
    return tuple(outreg)

def gtri(inreg, instruction):
    op, a, b, c = instruction
    outreg = list(inreg)
    outreg[c] = 1 if inreg[a] > b else 0 
    return tuple(outreg)

def gtrr(inreg, instruction):
    op, a, b, c = instruction
    outreg = list(inreg)
    outreg[c] = 1 if inreg[a] > inreg[b] else 0 
    return tuple(outreg)

def eqir(inreg, instruction):
    op, a, b, c = instruction
    outreg = list(inreg)
    outreg[c] = 1 if a == inreg[b] else 0 
    return tuple(outreg)

def eqri(inreg, instruction):
    op, a, b, c = instruction
    outreg = list(inreg)
    outreg[c] = 1 if inreg[a] == b else 0 
    return tuple(outreg)

def eqrr(inreg, instruction):
    op, a, b, c = instruction
    outreg = list(inreg)
    outreg[c] = 1 if inreg[a] == inreg[b] else 0 
    return tuple(outreg)

funclist = [addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]

ans1 = 0
for samp in samples:
    matches = 0
    print(samp)
    for func in funclist:
        result = func(samp.inp, samp.op)
        if result == samp.res:
            matches += 1
        if matches >= 3:
            break
    if matches >= 3:
        ans1 += 1
    print(f"Number of matches: {matches}")

#    input()

# Part 1: 640 
print(f"Part 1: {ans1}")


opcodes = {}

# Part 2
undiscovered = set(funclist)
discovered = set()
num_matching = 0
while undiscovered:
    num_matching += 1

    for samp in samples:
        if samp.op[0] in opcodes:
            continue

        matching_funcs = set() 
        for func in funclist:
            result = func(samp.inp, samp.op)
            if (result == samp.res) and (func in undiscovered):
                matching_funcs.add(func)

        if len(matching_funcs) == 1: 
            match = matching_funcs.pop()
            opcodes[samp.op[0]] = match 
            undiscovered.remove(match)
            discovered.add(match)
        else:
            unknowns = matching_funcs.difference(discovered) 
            if len(unknowns) == 1:
                match = matching_funcs.pop()
                opcodes[samp.op[0]] = match 
                undiscovered.remove(match)
                discovered.add(match)

test_lines = [l for l in Path('test.txt').read_text().split('\n') if l]
test = []
for line in test_lines:
    test.append(tuple([int(v) for v in line.split()])) 

reg = (0,0,0,0)

for t in test:
    opcode = t[0]
    reg = opcodes[opcode](reg, t)

print(f"Part 2: {reg[0]}")
