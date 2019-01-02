import sys
import itertools
from collections import defaultdict
from pathlib import Path
import pprint
import string

def main(infile):
    # PART 1

    lines = [
             'Step C must be finished before step A can begin.',
             'Step C must be finished before step F can begin.',
             'Step A must be finished before step B can begin.',
             'Step A must be finished before step D can begin.',
             'Step B must be finished before step E can begin.',
             'Step D must be finished before step E can begin.',
             'Step F must be finished before step E can begin.',
            ]
    lines = [s for s in Path(infile).read_text().split('\n') if s]

    graph = defaultdict(set) 
    nodes = set()
    for line in lines:
        dependency, node = line.split()[1], line.split()[-3]
        graph[node].add(dependency)
        nodes.add(node)
        nodes.add(dependency)

    ready = nodes - set(graph.keys())
    
    answer = []
    while ready.union(graph.keys()):
        current = sorted(ready)[0]
        ready.remove(current)

        # update dependencies
        for node in graph:
            if current in graph[node]:
                graph[node].remove(current)

            if not graph[node]:
                ready.add(node)

        for node in ready:
            graph.pop(node, None)

        answer.append(current)
    print(f"Part 1: {''.join(answer)}")

    # PART 2
    graph = defaultdict(set) 
    all_nodes = set()
    for line in lines:
        dependency, node = line.split()[1], line.split()[-3]
        graph[node].add(dependency)
        all_nodes.add(node)
        all_nodes.add(dependency)

    durations = {c: i+61 for i,c in enumerate(string.ascii_uppercase)}
    start_times = defaultdict(none) 

    processing = set()  # being worked on now
    completed = set()    # finished tasks
    not_ready = set(graph.keys())  # dependencies not met
    queued = all_nodes - set(graph.keys())      # dependencies met, ready to be worked on
    current_time = -1 

    while processing.union(queued).union(not_ready):
        current_time += 1
        print(f"Current time: {current_time}")

        # check for completed tasks and update dependencies 
        just_finished = set()
        for p in processing:
            if current_time - start_times[p] == durations[p]:
                just_finished.add(p)

                # remove p from all dependency lists
                for node in not_ready:
                    if p in graph[node]:
                        graph[node].remove(p)


        completed = completed.union(just_finished)
        processing = processing - just_finished
        print(f"Completed: {completed}")

        # Queue tasks with dependencies met
        for node in not_ready:
            if not graph[node]:
                queued.add(node)
        not_ready -= queued

        print(f"Queued: {queued}")

        # while we have workers available and tasks ready to be done, start work
        while (len(processing) < 5) and (len(queued) > 0):
            task = sorted(queued)[0]
            processing.add(task)
            queued.remove(task)
            start_times[task] = current_time

        print(f"Processing: {processing}")
        print(f"Not ready: {not_ready}")

    print(f"Part 2: {current_time}")

def none():
    return None


if __name__ == '__main__':
    g = main(sys.argv[-1])
