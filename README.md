# Uninformed & Informed Search Solver (BFS / UCS / A*)

A command-line tool that solves state-space search problems using **Breadth-First Search**, **Uniform-Cost Search**, and **A\*** search, plus utilities to check whether a given heuristic is **optimistic (admissible)** and/or **consistent (monotonic)**.

## Description

This project implements classic AI search algorithms over an explicit graph representation of a state space. States and their weighted transitions are loaded from a plain-text description file, and (optionally) a heuristic file assigns an estimated cost-to-goal for each state. The tool reports whether a solution was found, how many states were visited, the path length, total path cost, and the resulting path — and can independently verify heuristic properties by comparing them against optimal costs computed via UCS.

## Features

- **BFS** — breadth-first search (unweighted shortest path in terms of number of steps)
- **UCS** — uniform-cost search (optimal path by cumulative cost, via a priority queue)
- **A\*** — best-first search guided by `f = g + h`, using a supplied heuristic
- **Heuristic optimism check** — verifies `h(s) <= h*(s)` for every state with a heuristic value, where `h*` is the true optimal cost computed with UCS
- **Heuristic consistency check** — verifies `h(s) <= h(s') + c(s, s')` for every edge `s -> s'`
- Supports multiple goal states
- Deterministic tie-breaking (neighbors are sorted, and ties in the priority queues resolve lexicographically by state name)

## Requirements

- Python 3.7+
- No external dependencies (only the standard library: `heapq`, `argparse`, `collections`)

## Usage

```bash
python search.py --alg {bfs|ucs|astar} --ss <state_space_file> [--h <heuristic_file>]
python search.py --check-optimistic --ss <state_space_file> --h <heuristic_file>
python search.py --check-consistent --ss <state_space_file> --h <heuristic_file>
```

### Arguments

| Flag                  | Description                                              |
|-----------------------|------------------------------------------------------------|
| `--alg`                | Algorithm to run: `bfs`, `ucs`, or `astar`                |
| `--ss`                 | Path to the state space description file (required)       |
| `--h`                  | Path to the heuristic file (required for `astar` and the checks) |
| `--check-optimistic`   | Instead of searching, check if the heuristic is optimistic |
| `--check-consistent`   | Instead of searching, check if the heuristic is consistent |

### Examples

```bash
python search.py --alg bfs --ss puzzle.txt
python search.py --alg ucs --ss puzzle.txt
python search.py --alg astar --ss puzzle.txt --h puzzle_heuristic.txt
python search.py --check-optimistic --ss puzzle.txt --h puzzle_heuristic.txt
python search.py --check-consistent --ss puzzle.txt --h puzzle_heuristic.txt
```

## Input File Formats

### State space file (`--ss`)

```
# Lines starting with # are comments and are ignored
<start_state>
<goal_state_1> <goal_state_2> ...
<state>: <neighbor_1>,<cost_1> <neighbor_2>,<cost_2> ...
<state>: <neighbor_1>,<cost_1> ...
...
```

- **Line 1**: the start state
- **Line 2**: one or more goal states, separated by spaces
- **Following lines**: one per state, in the form `state: neighbor,cost neighbor,cost ...` (a state with no outgoing edges can be written as `state:`)

### Heuristic file (`--h`)

```
# Lines starting with # are comments and are ignored
<state>: <heuristic_value>
<state>: <heuristic_value>
...
```

## Output

For a search run, the tool prints:

```
[FOUND_SOLUTION]: yes/no
[STATES_VISITED]: <number of states expanded>
[PATH_LENGTH]: <number of states in the path>
[TOTAL_COST]: <total path cost>
[PATH]: state1 => state2 => ... => stateN
```

For heuristic checks, it prints an `OK`/`ERR` verdict per condition and an overall conclusion.

## Algorithm Notes

- **BFS** uses a FIFO queue and marks states as "queued" the moment they're enqueued to avoid re-adding duplicates, which keeps the search efficient on larger state spaces (e.g. sliding-tile puzzles).
- **UCS** uses a min-heap keyed by cumulative path cost and guarantees an optimal-cost path.
- **A\*** uses a min-heap keyed by `f = g + h` and tracks the best known cost per state in a closed set, re-expanding a state only if a cheaper path to it is found.

## License

Feel free to use, modify, and distribute this project. Consider adding an explicit license file (e.g. MIT) if you plan to share it publicly.
