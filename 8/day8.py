import sys
import itertools
from collections import deque
from pathlib import Path
import pprint
import string

class Node:
    def __init__(self, num_children, num_meta):
        self.num_children = num_children
        self.num_meta = num_meta
        self.value = 0
        self.children = []


def main(infile):
    # PART 1

    inputs = [int(s) for s in Path(infile).read_text().split() if s]
    #inputs= [2, 3, 0, 3, 10, 11, 12, 1, 1, 0, 1, 99, 2, 1, 1, 2]
    data = deque(inputs)

    metadata_sums = []

    def process_node(num_children, num_meta):
        if num_children != 0:
            for child in range(num_children):
                process_node(data.popleft(), data.popleft())
        metadata_sums.append(sum([data.popleft() for i in range(num_meta)]))
    process_node(data.popleft(), data.popleft())
    print(f"Part 1: {sum(metadata_sums)}")

    # PART 2
    data = deque(inputs)

    def process(node):
        if node.num_children == 0:
            node.value = sum([data.popleft() for i in range(node.num_meta)])
            print(f"Node has no children and value of {node.value}.")
        else:
            print(f"Node has {node.num_children} children.")
            for _ in range(node.num_children):
                child = Node(data.popleft(), data.popleft())
                node.children.append(child)
                process(child)
            children_indexes = [data.popleft() for _ in range(node.num_meta)]
            print(f"Node values are for children indices {children_indexes}.")
            for i in children_indexes:
                if i < 1:
                    continue
                elif i > len(node.children):
                    continue
                else:
                    node.value += node.children[i-1].value

    root = Node(data.popleft(), data.popleft())
    process(root)
    print(f"Part 2: {root.value}")


if __name__ == '__main__':
    g = main(sys.argv[-1])
