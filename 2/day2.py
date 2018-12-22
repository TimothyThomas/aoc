import sys
import itertools
from collections import defaultdict
from pathlib import Path

def main(infile):
    # PART 1
    box_ids = [s for s in Path(infile).read_text().split('\n') if s]
    #box_ids = ['abcdef', 'bababc', 'abbcde', 'abcccd', 'aabcdd', 'abcdee', 'ababab']
    #box_ids = ['abcde', 'fghij', 'klmno', 'pqrst', 'fguij', 'axcye', 'wvxyz']

    #print(box_ids)

    two_count = 0
    three_count = 0
    for box_id in box_ids:
        counts = defaultdict(zero) 
        for c in box_id:
            counts[c] += 1

        exactly_2 = False
        exactly_3 = False

        for c in counts:
            if counts[c] == 2: 
                exactly_2 = True 
            if counts[c] == 3:
                exactly_3 = True 

        if exactly_2:
            two_count += 1

        if exactly_3:
            three_count += 1

    print(f"Part 1: {two_count*three_count}")


    for id1, id2 in itertools.combinations(box_ids, 2):
        #print(id1, id2)
        mismatches = 0
        for c1, c2 in zip(id1, id2):
            #print(c1, c2)
            if c1 != c2:
                mismatches += 1
                
            if mismatches > 1:
                break
        if mismatches == 1:
            ans = ''.join([c1 for c1,c2 in zip(id1, id2) if c1==c2])
            print(f"Part 2: {ans}")


def zero():
    return 0


if __name__ == '__main__':
    main(sys.argv[-1])
