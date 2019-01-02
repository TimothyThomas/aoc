import sys
import string
from pathlib import Path
import numpy as np

def main(infile):
    # PART 1
    s  = Path(infile).read_text().strip()
    #s = 'dabAcCaCBAcCcaDA'

    print(f'Part 1: {len(react(s))}')

    min_length = len(s)
    for c in string.ascii_lowercase:
        test = s.replace(c, '').replace(c.upper(), '')
        reacted = react(test) 
        if len(reacted) < min_length:
            min_length = len(reacted)

    print(f'Part 2: {min_length}')



def react(s):
    i = 0
    iters = 0
    while i+1 < len(s):
        if (s[i].lower() == s[i+1].lower()) and (s[i] != s[i+1]):
            # destroyed
            s = s[:i] + s[i+2:]
            if i == 0:
                i = 0
            else:
                i -= 1 
        else:
            i += 1
        iters += 1

    return s


if __name__ == '__main__':
    df = main(sys.argv[-1])
