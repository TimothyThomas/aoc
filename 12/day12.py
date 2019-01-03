import sys
from pathlib import Path


state = list('#..#.#..##......###...###')
rules = {
        '...##':'#',
        '..#..':'#',
        '.#...':'#',
        '.#.#.':'#',
        '.#.##':'#',
        '.##..':'#',
        '.####':'#',
        '#.#.#':'#',
        '#.###':'#',
        '##.#.':'#',
        '##.##':'#',
        '###..':'#',
        '###.#':'#',
        '####.':'#',
}

GENERATIONS = 20
lines = [line for line in Path(sys.argv[-1]).read_text().split('\n') if line]
state = list(lines[0].split(':')[-1].strip())
rules = {line.split('=')[0].strip(): line.split('>')[-1].strip() for line in lines[1:]}

state = ['.']*5 + state + ['.']*5
plant_zero_index = 5 
num_plants = len([c for c in state if c == '#'])       
print(f"Initial: {num_plants}")


print(f"Gen 0: {''.join(state)}")
prev_gensum = 0
for generation in range(1, GENERATIONS+1):
    next_state = state[:] 
    for i, _ in enumerate(state[2:-2], 2):
        plants = state[i-2:i+3]
        rule = ''.join(plants)
        result = rules.get(rule, '.')
        #print(f"i: {i}, Plants {plants}, rule: {rule}, result: {result}")

        next_state[i] = result 
    while ''.join(next_state[:5]) != '.....':
        plant_zero_index += 1
        next_state.insert(0, '.')
    while ''.join(next_state[-5:]) != '.....':
        next_state.append('.')
    state = next_state[:]
    #print(f"Gen {generation}: {''.join(state)}")
    
    gensum = 0
    for i, pot in enumerate(state):
        if pot == '#':
            gensum += i - plant_zero_index
    print(f"Gen {generation}, Sum {gensum}, diff {gensum - prev_gensum}")
    prev_gensum = gensum

print(f"Part 1: {gensum}")

# Part 2

GENERATIONS = 50_000_000_000 
# Trial and error reveals the sum increases by 67 for every generation starting
# with Gen 102, whose sum is 6834
print(f"Part 2: {6834+67*(GENERATIONS - 102)}")




