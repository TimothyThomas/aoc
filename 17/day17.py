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
while not np.all(grid == prev):
    prev = grid.copy()

    for source_x, source_y in sources:
        # find first y were either water or clay is encountered
        y = source_y + 1
        while y < max_y:
            if grid[source_x, y] == '.':
                if grid[source_x, y+1] == '#':
                    grid[source_x, y] = '~'
                elif grid[source_x, y+1] == '~':
                    grid[source_x, y] = '~'
                else:
                    grid[source_x, y] = '|'

            elif grid[source_x, y] == '|':
                if grid[source_x - 1, y] == '.':
                    grid[source_x - 1,y] = '~'
                y += 1

            elif grid[source_x, y] in ['~', '#']:
                # expand left and then right as far as possible at this y

                x = source_x - 1
                while True: 
                    if grid[x,y] == '.':
                        if grid[x,y+1] in ['#', '~']:
                            grid[x,y] = '~'
                        else:
                            grid[x,y+1] = '|'
                    elif grid[x,y] == '~':
                        x -= 1
                    else:
                        break
                y += 1
            input()
            ps()


