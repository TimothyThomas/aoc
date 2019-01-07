import sys
from pathlib import Path
import numpy as np


def ps(g):
    s = '\n'.join([''.join([col for col in row]) for row in g])
    print(f'\n{s}\n')

lines = [l for l in Path(sys.argv[-1]).read_text().split('\n') if l]

# add a border of a different char so we don't have to treat edges/corners separately
top_bot_border = '*' * (len(lines[0])+2)
lines_with_border = [top_bot_border] + ['*' + l + '*' for l in lines] + [top_bot_border]

gi = np.array([[c for c in row] for row in lines_with_border])
gp = gi.copy()

minutes = 0

ps(gp)
while minutes < 10:
    gn = gp.copy() 
    for i,row in enumerate(gp[1:-1], 1):
        for j,col in enumerate(gp[i,1:-1], 1):

            if gp[i,j] == '.':
                tree_count = np.sum(gp[i-1:i+2,j-1:j+2] == '|')
                if tree_count >= 3:
                    gn[i][j] = '|'

            elif gp[i,j] == '|':
                lumber_count = np.sum(gp[i-1:i+2,j-1:j+2] == '#')
                if lumber_count >= 3:
                    gn[i][j] = '#'

            elif gp[i,j] == '#':
                tree_count = np.sum(gp[i-1:i+2,j-1:j+2] == '|')
                lumber_count = np.sum(gp[i-1:i+2,j-1:j+2] == '#') - 1 # subtract 1 for current i,j
                if (lumber_count < 1) or (tree_count < 1):
                    gn[i][j] = '.'
    minutes += 1
    gp = gn
    print(f"After {minutes} minutes.")
    ps(gp)

print(f"Part 1: {np.sum(gp == '|') * np.sum(gp == '#')}")

# Part 2, By inspection a repeating pattern is established after about 600 minutes.
# So find how often the pattern repeats and determine the state after 1e9 minutes.
gp = gi.copy()
ps(gp)

cached = {}
minutes = 0
part2_minutes = int(1e9)
repeats_every = None 
while True:
    gn = gp.copy() 
    for i,row in enumerate(gp[1:-1], 1):
        for j,col in enumerate(gp[i,1:-1], 1):

            if gp[i,j] == '.':
                tree_count = np.sum(gp[i-1:i+2,j-1:j+2] == '|')
                if tree_count >= 3:
                    gn[i][j] = '|'

            elif gp[i,j] == '|':
                lumber_count = np.sum(gp[i-1:i+2,j-1:j+2] == '#')
                if lumber_count >= 3:
                    gn[i][j] = '#'

            elif gp[i,j] == '#':
                tree_count = np.sum(gp[i-1:i+2,j-1:j+2] == '|')
                lumber_count = np.sum(gp[i-1:i+2,j-1:j+2] == '#') - 1 # subtract 1 for current i,j
                if (lumber_count < 1) or (tree_count < 1):
                    gn[i][j] = '.'
    minutes += 1

    if minutes == 700:
        cached[700] = gn

    if minutes > 701:
        if np.all(cached[700] == gn) and not repeats_every:
            repeats_every = minutes - 700

        if repeats_every and ((part2_minutes-minutes) % repeats_every == 0):
            break

    gp = gn
    ps(gp)

print(f"Part 2: {np.sum(gn == '|') * np.sum(gn == '#')}")
