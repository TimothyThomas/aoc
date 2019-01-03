import sys
from pathlib import Path
import numpy as np
from itertools import cycle
import os



def printstate(track, cars):
    state = [[col for col in row] for row in track]
    for car in cars:
        x = car.x
        y = car.y
        state[y][x] = car.dir 
    print('\n'.join([''.join(l) for l in state]))


class Car():
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.dir = direction  # up, down, left, right
        self.isxn_cycle = cycle(['left', 'straight', 'right'])
        self.isxn_turn = next(self.isxn_cycle)
        self.crashed = False

    def __repr__(self):
        return f"Car at {self.x},{self.y} going {self.dir}, turns {self.isxn_turn} at next isxn, crashed={self.crashed}"

    def advance(self):
        if self.dir == '>':
            self.x += 1
        elif self.dir == '<':
            self.x -=1
        elif self.dir == '^':
            self.y -= 1
        elif self.dir == 'v':
            self.y += 1

    def turn_left(self):
        if self.dir == '>':
            self.dir = '^'
        elif self.dir == '<':
            self.dir = 'v'
        elif self.dir == '^':
            self.dir = '<'
        elif self.dir == 'v':
            self.dir = '>'

    def turn_right(self):
        if self.dir == '>':
            self.dir = 'v'
        elif self.dir == '<':
            self.dir = '^'
        elif self.dir == '^':
            self.dir = '>'
        elif self.dir == 'v':
            self.dir = '<'


class Carlist:
    def __init__(self, cars):
        self.cars = cars
        self.sort()

    def sort(self):
        self.cars = sorted(self.cars, key=lambda c: (c.y, c.x))

    def __repr__(self):
        return '\n'.join([str(car) for car in self.cars])

    def is_crash(self):
        locations = [(c.x, c.y) for c in self.cars if not c.crashed]
        if len(locations) != len(set(locations)):
            return True
        else:
            return False

    def flag_crashed(self, x, y):
        for car in self.cars:
            if (car.x == x) and (car.y == y):
                car.crashed=True

    def clear_crashed(self):
        self.cars = [c for c in self.cars if not c.crashed]
        self.sort()


lines = [l for l in Path(sys.argv[-1]).read_text().split('\n') if l]
track = [[c for c in l] for l in lines]

# initialize all cars
cars = [] 
for y, row in enumerate(track):
    for x, col in enumerate(row):
        if col in list('><v^'):
            cars.append(Car(x, y, col))

carlist = Carlist(cars)

track_string = '\n'.join([''.join(l) for l in track])
track_string = track_string.replace('v', '|')
track_string = track_string.replace('^', '|')
track_string = track_string.replace('<', '-')
track_string = track_string.replace('>', '-')
track = [[c for c in l] for l in track_string.split('\n')]


tick = 0
while len(carlist.cars) > 1:
    #os.system('clear')
    carlist.sort()
    #printstate(track, carlist.cars)
    #print(carlist)
    for car in carlist.cars:
        print(f"Moving car {car}")
        x = car.x
        y = car.y

        if track[y][x] == '\\':

            if car.dir in ['>', '<']:
                car.turn_right()
            else:
                car.turn_left()

        elif track[y][x] == '/':

            if car.dir in ['>', '<']:
                car.turn_left()
            else:
                car.turn_right()

        elif track[y][x] == '+':

            if car.isxn_turn == 'left':
                car.turn_left() 
            elif car.isxn_turn == 'right':
                car.turn_right()

            car.isxn_turn = next(car.isxn_cycle)

        car.advance()

        if carlist.is_crash():
            carlist.flag_crashed(car.x, car.y)
            print(f"Crash at {car.x},{car.y}, tick={tick}")
        else:
            print(f"no crash")

    carlist.clear_crashed()

    tick += 1
#    input()

last_car = carlist.cars[0]
print(f"Part 2 ans: {last_car.x}, {last_car.y}") 
