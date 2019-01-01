import sys
from pathlib import Path
from math import inf
import os
import time



def ps():
    state = [[col for col in row] for row in area]
    for elf in elves.units:
        x = elf.x
        y = elf.y
        state[y][x] = 'E' 
    for goblin in goblins.units:
        x = goblin.x
        y = goblin.y
        state[y][x] = 'G' 
    print('\n'.join([''.join(l) for l in state]))


class Unit():
    def __init__(self, x, y, ap=3):
        self.x = x
        self.y = y
        self.hp = 200
        self.ap = ap
        self.alive = True

    def in_range(self, enemies):
        enemies = {(enemy.x, enemy.y) for enemy in enemies} 
        ux, uy = self.x, self.y
        neighbors = {n for n in [(ux, uy+1), (ux+1, uy), (ux-1, uy), (ux, uy-1)]}
        if enemies.intersection(neighbors):
            return True
        else:
            return False

    def get_attack_target(self, enemies):
        ux, uy = self.x, self.y
        neighbors = {n for n in [(ux, uy+1), (ux+1, uy), (ux-1, uy), (ux, uy-1)]}
        all_enemy_locs = {(enemy.x, enemy.y) for enemy in enemies} 
        enemy_locs_in_range = all_enemy_locs.intersection(neighbors)

        possible_targets = [enemy for enemy in enemies 
                if ((enemy.x, enemy.y) in enemy_locs_in_range) and (enemy.alive)]

        if not possible_targets:
            return None

        min_hp = inf
        min_hp_targets = []
        for t in possible_targets:
            if t.hp < min_hp:
                min_hp_targets = [t]
                min_hp = t.hp
            elif t.hp == min_hp:
                min_hp_targets.append(t)

        if len(min_hp_targets) == 1:
            return min_hp_targets.pop()
        else:
            # return based on reading order
            return sorted(min_hp_targets, key=lambda t: (t.y, t.x))[0]


    def attack(self, enemies):
        target = self.get_attack_target(enemies)
        if target:
            target.hp -= self.ap
            if target.hp <= 0:
                target.alive = False

    def get_next_move(self, enemies):
	#https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm
        
        # find shortest paths to all enemies 
        paths_to_enemies = {(enemy.x, enemy.y): [] for enemy in enemies} 

        nearest_enemy_dist = inf
        nearest_candidates = set()
        for enemy in paths_to_enemies:
            paths_to_enemies[enemy] = []
            unvisited = {(x, y) for x,y in graph}.difference({(unit.x,unit.y) for unit in all_units if unit.alive})

            # add source and target to unvisited
            unvisited.add((self.x, self.y))
            unvisited.add(enemy)

            dist = {(x,y): inf for x,y in unvisited} 
            dist[(self.x, self.y)] = 0
            prev = {(x,y): [] for x,y in unvisited}

            while unvisited:
                #breakpoint()
                ux, uy = min_distance(dist, unvisited) # min distance from source to unvisited nodes
                unvisited.remove((ux,uy))

                # process neighbors in reading order
                neighbors = [n for n in [(ux, uy+1), (ux+1, uy), (ux-1, uy), (ux, uy-1)] 
                            if (n in graph) and 
                            (n not in {(unit.x, unit.y) for unit in all_units if unit.alive}.difference({enemy}))]

                for neighbor in neighbors: 
                    alt = dist[(ux,uy)] + 1
                    if alt <= dist[neighbor]:
                        dist[neighbor] = alt
                        prev[neighbor].append((ux,uy))

            # if enemy is unreachable continue:
            if dist[enemy] == inf:
                continue
            path = []
            u = enemy
            while u:
                path.append(u)
                prev_choices = prev.get(u, None)
                if prev_choices: 
                    u = sorted(prev_choices, key=lambda c: (c[1], c[0]))[0]
                else:
                    u = None 
            if path[-1] != (self.x,self.y):  # no path was found  
                return (self.x, self.y)

            paths_to_enemies[enemy] = path

            shortest_path_this_enemy = len(path)
            if shortest_path_this_enemy == nearest_enemy_dist:
                nearest_candidates.add(enemy)
            elif shortest_path_this_enemy < nearest_enemy_dist:
                nearest_enemy_dist = shortest_path_this_enemy
                nearest_candidates = {enemy}

        if not nearest_candidates:  # no paths found
            return (self.x, self.y)

        elif len(nearest_candidates) == 1:
            return paths_to_enemies[nearest_candidates.pop()][-2]

        else:
            # sort by in reading order by location prior to target, not target itself
            # index 1 in path is location just prior to target
            nearest = sorted(nearest_candidates, key=lambda c:
                    (paths_to_enemies[c][1][1], paths_to_enemies[c][1][0]))[0]
            return paths_to_enemies[nearest][-2]
                        

def min_distance(dist, Q):
    """Return x,y coordinates of node in set Q with min value in dist."""
    min_dist = inf
    min_xy = None
    for x,y in Q:
        if dist[(x,y)] < min_dist:
            min_dist = dist[(x,y)]
            min_xy = (x,y)
    if min_xy:
        return min_xy
    else:
        return list(Q)[0]  # all have dist of inf so return arbitrary


class Elf(Unit):
    def __repr__(self):
        return f"Elf at {self.x},{self.y}, {self.hp} HP"


class Goblin(Unit):
    def __repr__(self):
        return f"Goblin at {self.x},{self.y}, {self.hp} HP"


class UnitList:
    def __init__(self, units):
        self.units = units

    def reading_sort(self):
        self.units = sorted(self.units, key=lambda c: (c.y, c.x))

    def __repr__(self):
        return '\n'.join([str(unit) for unit in self.units])

    def __len__(self):
        return len(self.units)

    def __getitem__(self, key):
        return self.units[key]


lines = [l for l in Path(sys.argv[-1]).read_text().split('\n') if l]
area = [[c for c in l] for l in lines]

graph = {}
# all input maps have #### around all borders so we don't need to check those
for y, row in enumerate(area[1:-1], 1):
    for x, col in enumerate(row[1:-1], 1):
        cur = (x,y)
        adj = [(x+1,y), (x-1,y), (x,y+1), (x,y-1)]
        if area[y][x] == '#':
            continue
        graph[(x,y)] = [n for n in adj if area[n[1]][n[0]] != '#']

# initialize elves and goblins 
elves = UnitList([])
goblins = UnitList([])
for y, row in enumerate(area):
    for x, col in enumerate(row):
        if col == 'E': 
            elves.units.append(Elf(x, y, ap=17))  # ap=16 for Part 2 (trial and error)
        elif col == 'G':
            goblins.units.append(Goblin(x, y))

all_units = UnitList(elves.units + goblins.units)

area_string = '\n'.join([''.join(l) for l in area])
area_string = area_string.replace('E', '.')
area_string = area_string.replace('G', '.')
area = [[c for c in l] for l in area_string.split('\n')]


num_elves = len(elves.units)
round = 0
ps()
combat_ends = False
#BREAK_ROUND = 8
BREAK_ROUND = 100
while not combat_ends:
    os.system('clear')
    all_units.reading_sort()
    ps() 
    print(f'\nStart of round: {round+1}\n')
    print(all_units)
#    input()

    for i, unit in enumerate(all_units.units):
        os.system('clear')
        ps() 
        print(f'Round: {round+1}')
        if not any([u.alive for u in all_units.units[i:]]):
            round += 1
            break

        if unit is all_units.units[-1]:  # a full round has completed
            round += 1

        if not unit.alive:
            continue
        print(f'Unit turn: {unit}')
        print('\n'.join([str(su) for su in sorted(all_units.units, key=lambda u: u.hp)]))
        #time.sleep(.01)
        #if round + 1 >=BREAK_ROUND:
        #    input()
        x = unit.x
        y = unit.y

        if type(unit) == Goblin:
            if not unit.in_range(elves):
                next_move = unit.get_next_move(elves)
                unit.x, unit.y = next_move

            if unit.in_range(elves):
                unit.attack(elves)

        elif type(unit) == Elf:
            if not unit.in_range(goblins):
                next_move = unit.get_next_move(goblins)
                unit.x, unit.y = next_move

            if unit.in_range(goblins):
                unit.attack(goblins)

        elves.units = [elf for elf in elves.units if elf.alive]
        goblins.units = [goblin for goblin in goblins.units if goblin.alive]

        if (len(elves) > 0) and (len(goblins) > 0):
            continue
        else:
            combat_ends = True
            break


    all_units = UnitList(elves.units + goblins.units)


os.system('clear')
ps()
print(f'\nCombat ended after {round} rounds.\n')
print(all_units)

hp_sum = sum([u.hp for u in all_units.units])
print(f"Part 1 ans: {round*hp_sum}") 

# Part 1 wrong guesses:
# 180498 (67 rounds)
# 183192 (68 rounds)
# 177804 (66 rounds)
# CORRECT ANSWER:  182376

if len(elves) == num_elves:
    print(f"Part 2 ans: {round*hp_sum}") 

