import sys
import itertools
import numpy as np



# PART 1

serial = 42
serial = 5791
GRID_SIZE = 300

grid = np.zeros((GRID_SIZE,GRID_SIZE)) 

for i in range(1, grid.shape[0]+1):
    for j in range(1,grid.shape[1]+1):
        rack_id = j + 10
        power = rack_id * i + serial
        power *= rack_id
        power = int(str(power)[-3]) - 5
        grid[i-1,j-1] = power 

max_power = 0
max_loc = (0,0)
for i in range(grid.shape[0]-2):
    for j in range(grid.shape[1]-2):
        total_power = np.sum(grid[i:i+3, j:j+3])
        if total_power > max_power:
            max_power = total_power
            max_loc = (i+1, j+1)

print(f"Part 1: X={max_loc[1]}, Y={max_loc[0]}")

# PART 2
saved = {}  # keys are (x,y,size) values are total power

# loop through possible sizes
max_power = 0
max_loc = (0,0)
max_size = -1
for size in range(1,GRID_SIZE+1):
    print(size)
    for i in range(GRID_SIZE - size+1):
        for j in range(GRID_SIZE - size+1):
            if size == 1:
                total_power = grid[i,j] 
            else:
                if size % 2 == 0:
                    half_size = size / 2
                    total_power = saved[(i, j, half_size)] + \
                                  saved[(i, j+half_size, half_size)] + \
                                  saved[(i+half_size, j, half_size)] + \
                                  saved[(i+half_size, j+half_size, half_size)]
                else:
                    # add previous block plus bottom row, plus right column
                    total_power = saved[(i, j, size-1)] + \
                            np.sum(grid[i+size-1,j:j+size]) + \
                            np.sum(grid[i:i+size-1,j+size-1])

            saved[(i,j,size)] = total_power
            if total_power > max_power:
                max_size = size
                max_power = total_power
                max_loc = (i+1, j+1)  # swap x,y

# 231,273,16
print(f"Part 2: X={max_loc[1]}, Y={max_loc[0]}, Size={max_size}")
