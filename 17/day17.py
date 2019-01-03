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

grid = np.array([['.']*(max_y+1)]*(max_x+1))

for xb, xe, yb, ye in data:
    grid[xb:xe+1,yb:ye+1] = '#'

grid[500,0] = '+'

def ps():
    #s = '\n'.join([''.join([col for col in row[min_x-1:]]) for row in grid])
    s = '\n'.join([''.join([col for col in row[min_x-1:]]) for row in grid.T])
    print(s)

ps()

sources = [(500,0)]
prev = grid.copy() 
prev[:,:] = '.'
drops = 0
while True: 
    drops += 1
    # for each source

        # fill containers starting with the lowest and leftmost/rightmost point
        # below the source


        # move down from source changing . to | until we hit # or ~ or max_y
        # if we hit #, check if we can spread left and right
    x = 500 
    y = 1 
    furthest_found = False
    while not furthest_found:
        # for each location starting from source:
        #   first look down, if open, move down and continue 
        #   otherwise, look left, and if open move left 
        #       if not open, replace current with water and continue
        #   otherwise, look right, and if open move right
        #       if not open, replace current with water, and continue
        #
        # find furthest point water can travel from source
        prev = grid[x,y]
        grid[x,y]='*'
        ps()
        grid[x,y] = prev
        if grid[x, y+1] == '.':
            y += 1
        
        elif grid[x-1, y] == '.':
            x -= 1

        elif (grid[x-1,y] in ['#', '~']) and (grid[x,y] == '.'):
            print("Furthest found")
            furthest_found = True
            grid[x,y] = '~'

        elif grid[x+1,y] == '.':
            x += 1

        elif (grid[x+1,y] in ['#', '~']) and (grid[x,y] == '.'):
            print("Furthest found")
            furthest_found = True
            grid[x,y] = '~'

        input()
