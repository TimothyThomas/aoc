import sys
import itertools
from collections import defaultdict
from pathlib import Path
import numpy as np

def main(infile):
    # PART 1
    claim_strings = [s for s in Path(infile).read_text().split('\n') if s]

    #claim_strings = ['#1 @ 1,3: 4x4', '#2 @ 3,1: 4x4', '#3 @ 5,5: 2x2']

    claims = {}
    for s in claim_strings:
        number = s.split()[0][1:]
        x,y = s.split()[2].rstrip(':').split(',')
        width, height = s.split()[-1].split('x')

        claims[number] = (int(x), int(y), int(width), int(height))

    overlap = 0

    # Assume fabric is 2000x2000 based on question info and initialize with 0's
    n = 2000
    fabric = np.array([[0]*n for i in range(n)])

    for num in claims:
        x,y,width,height = claims[num]
        fabric[x:x+width, y:y+height] += 1 
    overlap = np.sum(fabric>1) 
    print(f"Part 1: {overlap}")

    # Part 2
    for claim in claims:
        x,y,w,h = claims[claim]
        if np.all(fabric[x:x+w,y:y+h] == 1):
            break
    print(f"Part 2: {claim}\n{claims[claim]}")


if __name__ == '__main__':
    main(sys.argv[-1])
