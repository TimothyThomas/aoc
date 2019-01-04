import sys
from pathlib import Path
import re
import numpy as np

lines = [l for l in Path(sys.argv[-1]).read_text().split('\n') if l]

grid = []

max_x = 0
min_x = 10000
max_y = 0 
min_y = 10000 


data = []
for line in lines:
    x = re.findall(r'x=([\d.]+)', line)[0]
    y = re.findall(r'y=([\d.]+)', line)[0]

    if '..' in x:
        x_beg, x_end = [int(v) for v in x.split('..')]
    else:
        x_beg, x_end = int(x), int(x)

    if '..' in y:
        y_beg, y_end = [int(v) for v in y.split('..')]
    else:
        y_beg, y_end = int(y), int(y)

    if x_end > max_x:
        max_x = x_end
    if x_beg < min_x:
        min_x = x_beg
    if y_end > max_y:
        max_y = y_end
    if y_beg < min_y:
        min_y = y_beg

    data.append((x_beg, x_end, y_beg, y_end))

grid = np.array([['.']*(max_y+2)]*(max_x+2))

for xb, xe, yb, ye in data:
    grid[xb:xe+1,yb:ye+1] = '#'

grid[500,0] = '+'

def ps(g):
    s = '\n'.join([''.join([col for col in row[min_x-3:]]) for row in g.T])
    print(s)


def find_bottom_from_source(grid, source_x, source_y):
    bottom_found = False
    y = source_y
    x = source_x
    while not bottom_found:
        if y+1 > max_y:
            bottom_found = True
            bottom_y = y
        elif grid[x,y+1] == '.':
            y += 1
        else:
            bottom_found = True
            bottom_y = y
    return bottom_y

def fill_level(g, x, y):
    source_x = x
    left_edge_x = right_edge_x = None  # edge of water (not wall)
    left_contained = right_contained = False
    new_sources = [] 
    while not left_edge_x:
        if g[x-1,y] in ['#']:  # left contained 
            left_contained = True
            left_edge_x = x
            break

        elif g[x-1,y+1] in ['#', '~']:  # floor extends:
            x -= 1  # keep searching left

        else:       # hole in floor
            left_edge_x = x
            g[left_edge_x-1,y] = '|'
            new_sources.append((x-1,y))

    x = source_x
    while not right_edge_x:
        if g[x+1,y] in ['#']:  # right contained 
            right_contained = True
            right_edge_x = x
            break

        elif g[x+1,y+1] in ['#', '~']:  # floor extends:
            x += 1  # keep searching right
        else:       # hole in floor
            right_edge_x = x
            g[right_edge_x+1,y] = '|'
            new_sources.append((x+1,y))

    if left_contained and right_contained:
        g[left_edge_x:right_edge_x+1,y] = '~'
        # we may have converted a level that was partially filled with | to all ~, so check if we should add a new
        # source
        if np.any(g[left_edge_x:right_edge_x+1,y-1] == '|'):
            # find left_most index of source
            new_source_x = int(np.where(g[left_edge_x:right_edge_x+1,y-1]=='|')[0][0]) + left_edge_x
            new_sources.append((new_source_x,y-1))
         
    else:
        g[left_edge_x:right_edge_x+1,y] = '|'

    return g, new_sources



sources = {(500,0)}
prev = grid.copy() 
prev[:,:] = '.'
while sources: 
    source_x,source_y = sources.pop() 
    y_bot = max_y+10
    while source_y != y_bot:
        y_bot = find_bottom_from_source(grid, source_x, source_y)

        if grid[source_x,y_bot+1] == '|':
            grid[source_x,y_bot] = '|'
        elif y_bot == max_y:
            grid[source_x,y_bot] = '|'
        else:
            # find how far left and right y_bot is contained and if water can settle 
            # at this level (~) or not (|)
            grid, new_sources = fill_level(grid, source_x, y_bot)

            if new_sources:
                sources = sources.union(new_sources)

ps(grid)
print(f"Part 1: {np.sum(grid[:,min_y:]=='|') + np.sum(grid[:,min_y:]=='~')}")
print(f"Part 2: {np.sum(grid[:,min_y:]=='~')}")
