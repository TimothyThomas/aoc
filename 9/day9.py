import sys
import itertools
from collections import deque
from pathlib import Path
import pprint
import string



def main(infile):
    NUM_PLAYERS = 411
    NUM_MARBLES = 71170   # Part 1
    NUM_MARBLES = 7117000 # Part 2

#    NUM_PLAYERS, NUM_MARBLES = 9, 25

    player_cycle = itertools.cycle(range(1,NUM_PLAYERS+1))
    scores = {p: 0 for p in range(1, NUM_PLAYERS+1)}

    circle = deque([0, 1])

    current_index = 2
    for i in range(2, NUM_MARBLES+1):
        player = next(player_cycle)

        if i%23 == 0:
            circle.rotate(7)
            scores[player] += i + circle.pop()
            circle.rotate(-1)

        else:
            circle.rotate(-1)
            circle.append(i)

    #    marked_circle = circle[:current_index] + [f'*{circle[current_index]}*'] + circle[current_index+1:]
    #    print(f"Player {player}, {marked_circle}")

    print(f"Part 1: {max([scores[p] for p in scores])}")




if __name__ == '__main__':
    g = main(sys.argv[-1])
