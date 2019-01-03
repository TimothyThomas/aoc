

inp = 880751 
#inp = 59414

def print_state(recipes, i, j):
    s = [r for r in recipes]
    s[i] = f'({s[i]})'
    s[j] = f'[{s[j]}]'
    print(' '.join(str(r) for r in s))

print_state(recipes, idx1, idx2)

recipes = [3, 7]
idx1 = 0
idx2 = 1

while len(recipes) < inp + 10:
    recipe1 = recipes[idx1]
    recipe2 = recipes[idx2]
    new_sum = str(recipe1 + recipe2)

    if len(new_sum) == 1:
        recipes.append(int(new_sum))
    else:
        for digit in list(new_sum):
            recipes.append(int(digit))
    
    idx1 = (idx1 + 1 + recipe1) % len(recipes)
    idx2 = (idx2 + 1 + recipe2) % len(recipes)
#    print_state(recipes, idx1, idx2)

ans = ''.join([str(r) for r in recipes])[-10:]
print(f"Part 1: {ans}")



# Part 2
recipes = [3, 7]
idx1 = 0
idx2 = 1
iters = 100000
i = 0
search_string = str(inp)
already_searched_idx = 0

num_recipes = 2

not_seen = list(search_string[::-1])

while not_seen: 
#    print(not_seen)

    recipe1 = recipes[idx1]
    recipe2 = recipes[idx2]
    new_sum = str(recipe1 + recipe2)

    if len(new_sum) == 1:
        num_recipes += 1
        recipes.append(int(new_sum))

        if new_sum == not_seen[-1]:
            not_seen.pop()
        else:
            not_seen = list(search_string[::-1])

    else:
        for digit in list(new_sum):
            recipes.append(int(digit))

            if not not_seen:
                break

            if digit == not_seen[-1]:
                not_seen.pop()
            else:
                not_seen = list(search_string[::-1])

            num_recipes += 1
    
    idx1 = (idx1 + 1 + recipe1) % len(recipes)
    idx2 = (idx2 + 1 + recipe2) % len(recipes)
#    print_state(recipes, idx1, idx2)

print(f"Part 2: {num_recipes - len(search_string)}")
