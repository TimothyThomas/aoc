import sys
import itertools
from collections import defaultdict
from pathlib import Path
import numpy as np
import pandas as pd
import pprint

def main(infile):
    # PART 1
    lines = [s for s in Path(infile).read_text().split('\n') if s]
#    lines = [
#'[1518-11-01 00:00] Guard #10 begins shift',
#'[1518-11-01 00:05] falls asleep',
#'[1518-11-01 00:25] wakes up',
#'[1518-11-01 00:30] falls asleep',
#'[1518-11-01 00:55] wakes up',
#'[1518-11-01 23:58] Guard #99 begins shift',
#'[1518-11-02 00:40] falls asleep',
#'[1518-11-02 00:50] wakes up',
#'[1518-11-03 00:05] Guard #10 begins shift',
#'[1518-11-03 00:24] falls asleep',
#'[1518-11-03 00:29] wakes up',
#'[1518-11-04 00:02] Guard #99 begins shift',
#'[1518-11-04 00:36] falls asleep',
#'[1518-11-04 00:46] wakes up',
#'[1518-11-05 00:03] Guard #99 begins shift',
#'[1518-11-05 00:45] falls asleep',
#'[1518-11-05 00:55] wakes up',
#]
    records = []
    for line in lines:
        date, time = line.split(']')[0][1:].split()
        # add 200 to year to get around pandas/numpy datetime64 minimum limitation
        date = date[0] + '7' + date[2:]
        action = line.split(']')[1].lstrip()
        records.append((date,time,action))
    records = sorted(records)

    # build dict of Guard IDs and accumulate minutes asleep for each minute
    d = {}
    for record in records:
        hour, minute = (int(x) for x in record[1].split(':'))
        action = record[-1]
        date = record[0]

        if action.startswith('Guard'):
            guard = int(action.split()[1][1:])
            if guard not in d:
                d[guard] = {i: 0 for i in range(60)}

        elif action.endswith('asleep'):
            if hour == 23:
                sleep_start = minute - 60
            else:
                sleep_start = minute

        elif action.endswith('wakes up'):
            sleep_end = minute
            for m in range(sleep_start, sleep_end):
                d[guard][m] += 1 

    max_sleep = -1 
    max_sleep_guard = -1
    for guard in d:
        total_sleep = sum([d[guard][i] for i in d[guard]])
        if total_sleep > max_sleep:
            max_sleep = total_sleep
            max_sleep_guard = guard

    max_sleep_minute = np.argmax([d[max_sleep_guard][i] for i in d[max_sleep_guard]])

    print(f"Part 1: guard {max_sleep_guard},min{max_sleep_minute},guard x min={max_sleep_guard*max_sleep_minute}")

    # part 2
    max_idx = -1
    max_amt = -1
    max_guard = -1
    for guard in d:
        max_idx_this_guard = np.argmax([d[guard][i] for i in d[guard]])
        max_amt_this_guard = d[guard][max_idx_this_guard]
        
        if max_amt_this_guard > max_amt:
            max_amt = max_amt_this_guard
            max_idx = max_idx_this_guard
            max_guard = guard

    print(f"Part 2: guard={max_guard},min={max_idx},amt={max_amt},guard x min={max_guard*max_idx}")
    return d


if __name__ == '__main__':
    df = main(sys.argv[-1])
