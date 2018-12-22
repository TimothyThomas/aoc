import sys
from pathlib import Path
from itertools import cycle

def main(infile):
    # PART 1
    data = [int(i) for i in Path(infile).read_text().split('\n') if i]
    ans1 = sum(data)
    print(f"Part 1 answer: {ans1}")

    # PART 2 brute force
    freqs = set()
    cyc = cycle(data)
    current = next(cyc) 
    while current not in freqs:
        freqs.add(current)
        num = next(cyc)
        current += num
    print(f"Part 2 answer: {current}")

if __name__ == '__main__':
    main(sys.argv[-1])
