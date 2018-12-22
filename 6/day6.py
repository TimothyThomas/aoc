import sys
import itertools
from collections import defaultdict
from pathlib import Path
import numpy as np

def main(infile):
    # PART 1
    lines = [s for s in Path(infile).read_text().split('\n') if s]
    coords = [tuple(map(int, l.split(','))) for l in lines] 
    #coords = [(1,1), (1,6), (8,3), (3,4), (5,5), (8,9)]

    max_x = max([pair[0] for pair in coords]) + 1
    max_y = max([pair[1] for pair in coords]) + 1
    coords = {i: coord for i, coord in enumerate(coords)}

    arr = np.array(( [[-1]*(max_y)]*(max_x) ))
    
    for x in range(max_x):
        for y in range(max_y):
            arr[x,y] = get_closest_coordinate(x, y, coords)

    max_area = 0
    for coord in coords:
        if (np.any(arr[0,:]==coord) or np.any(arr[:,0]==coord) or
            np.any(arr[max_x-1,:]==coord) or
            np.any(arr[:,max_y-1]==coord)):
            area = 0
            print(f"Coord {coord} located at a boundary.")
        else:
            area = np.sum(arr==coord)
            print(f"Coord {coord} has area: {area}.") 
        if area > max_area:
            max_area = area

    print(f'Part 1: {max_area}')

    # PART 2
    arr = np.zeros((max_x, max_y))

    for x in range(max_x):
        for y in range(max_y):
            arr[x,y] = get_total_dist_to_all(x, y, coords)

    print(f'Part 2: {np.sum(arr<10000)}')

    return arr


def get_closest_coordinate(x, y, coords):
    """Return integer label of nearest coordinate to (x,y) or None if tie."""
    closest = -1 
    min_dist = np.inf
    for coord in coords:
        dist = abs(coords[coord][0] - x) + abs(coords[coord][1] - y)
        if dist < min_dist:
            min_dist = dist
            closest = coord
        elif dist == min_dist:
            closest = -1

    return closest


def get_total_dist_to_all(x, y, coords):
    total_dist = 0
    for coord in coords:
        dist = abs(coords[coord][0] - x) + abs(coords[coord][1] - y)
        total_dist += dist

    return total_dist 



if __name__ == '__main__':
    a = main(sys.argv[-1])
