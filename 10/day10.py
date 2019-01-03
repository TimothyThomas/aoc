import sys
import itertools
from collections import deque
from pathlib import Path
import pprint
import string
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import re



infile = sys.argv[1]
# PART 1


lines = [
'position=< 9,  1> velocity=< 0,  2>',
'position=< 7,  0> velocity=<-1,  0>',
'position=< 3, -2> velocity=<-1,  1>',
'position=< 6, 10> velocity=<-2, -1>',
'position=< 2, -4> velocity=< 2,  2>',
'position=<-6, 10> velocity=< 2, -2>',
'position=< 1,  8> velocity=< 1, -1>',
'position=< 1,  7> velocity=< 1,  0>',
'position=<-3, 11> velocity=< 1, -2>',
'position=< 7,  6> velocity=<-1, -1>',
'position=<-2,  3> velocity=< 1,  0>',
'position=<-4,  3> velocity=< 2,  0>',
'position=<10, -3> velocity=<-1,  1>',
'position=< 5, 11> velocity=< 1, -2>',
'position=< 4,  7> velocity=< 0, -1>',
'position=< 8, -2> velocity=< 0,  1>',
'position=<15,  0> velocity=<-2,  0>',
'position=< 1,  6> velocity=< 1,  0>',
'position=< 8,  9> velocity=< 0, -1>',
'position=< 3,  3> velocity=<-1,  1>',
'position=< 0,  5> velocity=< 0, -1>',
'position=<-2,  2> velocity=< 2,  0>',
'position=< 5, -2> velocity=< 1,  2>',
'position=< 1,  4> velocity=< 2,  1>',
'position=<-2,  7> velocity=< 2, -2>',
'position=< 3,  6> velocity=<-1, -1>',
'position=< 5,  0> velocity=< 1,  0>',
'position=<-6,  0> velocity=< 2,  0>',
'position=< 5,  9> velocity=< 1, -2>',
'position=<14,  7> velocity=<-2,  0>',
'position=<-3,  6> velocity=< 2, -1>',
]
lines = [line for line in Path(infile).read_text().split('\n') if line]

x_positions = []
y_positions = []
x_velocities = []
y_velocities = []

for line in lines:
    xpos, ypos, xvel, yvel = map(int, re.findall(r'(-?\d+)', line))
    x_positions.append(xpos)
    y_positions.append(ypos)
    x_velocities.append(xvel)
    y_velocities.append(yvel)

x0 = np.array(x_positions)
y0 = np.array(y_positions)
vx = np.array(x_velocities)
vy = np.array(y_velocities)

y0 = -1.0 * y0
vy = -1.0 * vy


fig, ax = plt.subplots()
line, = ax.plot([], [], 'ro', animated=True)
ax.set_xlim(x0.min(), x0.max())
ax.set_ylim(y0.min(), y0.max())
ax.set_xlim(120, 220)
ax.set_ylim(-70, -150)
#ax.set_aspect('equal')
ax.grid()

def init():
    line.set_data(x0, y0)
    return line, 


def animate(t):
    x = x0 + t*vx 
    y = y0 + t*vy 

   # ax.set_xlim(x.min()-x.min()*0.2, x.max()+x.max()*0.2)
   # ax.set_ylim(y.min()-y.min()*0.2, y.max()+y.max()*0.2)

    line.set_data(x, y)
    return line, 

ani = FuncAnimation(fig, animate, interval=5000, frames=np.arange(10656,100000,1), blit=True)

plt.show()
