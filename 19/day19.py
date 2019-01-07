import sys
from pathlib import Path

def addr(inreg, instruction):
    a, b, c = instruction
    outreg = list(inreg)
    outreg[c] = inreg[a] + inreg[b]
    return (outreg)

def addi(inreg, instruction):
    a, b, c = instruction
    outreg = list(inreg)
    outreg[c] = inreg[a] + b 
    return (outreg)

def mulr(inreg, instruction):
    a, b, c = instruction
    outreg = list(inreg)
    outreg[c] = inreg[a] * inreg[b]
    return (outreg)

def muli(inreg, instruction):
    a, b, c = instruction
    outreg = list(inreg)
    outreg[c] = inreg[a] * b 
    return (outreg)

def banr(inreg, instruction):
    a, b, c = instruction
    outreg = list(inreg)
    outreg[c] = inreg[a] & inreg[b] 
    return (outreg)

def bani(inreg, instruction):
    a, b, c = instruction
    outreg = list(inreg)
    outreg[c] = inreg[a] & b 
    return (outreg)

def borr(inreg, instruction):
    a, b, c = instruction
    outreg = list(inreg)
    outreg[c] = inreg[a] | inreg[b] 
    return (outreg)

def bori(inreg, instruction):
    a, b, c = instruction
    outreg = list(inreg)
    outreg[c] = inreg[a] | b 
    return (outreg)

def setr(inreg, instruction):
    a, b, c = instruction
    outreg = list(inreg)
    outreg[c] = inreg[a]
    return (outreg)

def seti(inreg, instruction):
    a, b, c = instruction
    outreg = list(inreg)
    outreg[c] = a 
    return (outreg)

def gtir(inreg, instruction):
    a, b, c = instruction
    outreg = list(inreg)
    outreg[c] = 1 if a > inreg[b] else 0 
    return (outreg)

def gtri(inreg, instruction):
    a, b, c = instruction
    outreg = list(inreg)
    outreg[c] = 1 if inreg[a] > b else 0 
    return (outreg)

def gtrr(inreg, instruction):
    a, b, c = instruction
    outreg = list(inreg)
    outreg[c] = 1 if inreg[a] > inreg[b] else 0 
    return (outreg)

def eqir(inreg, instruction):
    a, b, c = instruction
    outreg = list(inreg)
    outreg[c] = 1 if a == inreg[b] else 0 
    return (outreg)

def eqri(inreg, instruction):
    a, b, c = instruction
    outreg = list(inreg)
    outreg[c] = 1 if inreg[a] == b else 0 
    return (outreg)

def eqrr(inreg, instruction):
    a, b, c = instruction
    outreg = list(inreg)
    outreg[c] = 1 if inreg[a] == inreg[b] else 0 
    return (outreg)

funcmap = {'addr': addr, 
           'addi': addi, 
           'mulr': mulr, 
           'muli': muli, 
           'banr': banr, 
           'bani': bani, 
           'borr': borr, 
           'bori': bori, 
           'setr': setr, 
           'seti': seti, 
           'gtir': gtir, 
           'gtri': gtri, 
           'gtrr': gtrr, 
           'eqir': eqir, 
           'eqri': eqri, 
           'eqrr': eqrr}

lines = [l for l in Path(sys.argv[-1]).read_text().split('\n') if l]
ireg = int(lines[0].split()[-1])
instructs = {}
for i, line in enumerate(lines[1:]):
    instructs[i] = [line.split()[0]] + [int(v) for v in line.split()[1:]]
    instructs[i][0] = funcmap[instructs[i][0]]

reg = [0,0,0,0,0,0]
ip = 0
#while True:
#    func,a,b,c = instructs[ip]
#    #print(f'ip={ip} {reg} {func.__name__} {a} {b} {c} ', end='')
#    reg = func(reg, (a,b,c))
#    ip = reg[ireg]
#    #print(reg)
#    ip += 1
#    if not ip in instructs:
#        break
#    reg[ireg] = ip
#    #input()

print(f"Part 1: {reg}")

# PART 2
#reg = [1,0,0,0,0,0]
#reg = [0,10551309,11,10551308,0,1]
#ip = 11
#while True:
#    func,a,b,c = instructs[ip]
#    print(f'ip={ip} {reg} {func.__name__} {a} {b} {c} ', end='')
#    reg = func(reg, (a,b,c))
#    ip = reg[ireg]
#    print(reg, end='')
#    ip += 1
#    if not ip in instructs:
#        break
#    reg[ireg] = ip
#    input()
#
# Use the above output to deduce what the program is doing.

# Label registers 0 thru 5 as follows
#0 1 2 3 4 5 
#A B C D E F
#
# The code is accumulating in register 0 the sum of the factors of register 1.
#
# A = sum(factors of B)
#for F in range(1, B+1):
#    for D in range(1, B+1):
#        if D*F == B::      # if F is a factor of B
#            A += F         # A += F

sum_of_factors = 0
B = 10551309
for i in range(1,B+1):
    if B % i == 0:  # i is a factor of B
        sum_of_factors += i
print(f'Part 2: sum_of_factors')
