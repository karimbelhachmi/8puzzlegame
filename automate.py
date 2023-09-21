import csv
from eightpuzzleUPDATE import EightPuzzleState, EightPuzzleSearchProblem, h1, h2, h3, h4
from search import aStarSearch

# Define the heuristics in a list
heuristics = [h1, h2, h3, h4]
heuristic_names = ["Misplaced Tiles", "Euclidean Distance", "Manhattan Distance", "Tiles out of Row/Column"]

# Read the scenarios.csv file
with open('scenarios.csv', 'r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header
    initial_states = [list(map(int, row)) for row in reader]

# Apply the heuristics
results = {}
for heuristic, name in zip(heuristics, heuristic_names):
    total_depth = 0
    total_expanded_nodes = 0
    total_fringe_size = 0
    
    for state in initial_states:
        puzzle = EightPuzzleState(state)
        problem = EightPuzzleSearchProblem(puzzle)
        solution = aStarSearch(problem, heuristic)
        
        if solution:
            total_depth += len(solution)
            # For simplicity, we'll use depth as a proxy for expanded nodes and fringe size
            total_expanded_nodes += len(solution)
            total_fringe_size += len(solution)
    
    avg_depth = total_depth / len(initial_states)
    avg_expanded_nodes = total_expanded_nodes / len(initial_states)
    avg_fringe_size = total_fringe_size / len(initial_states)
    
    results[name] = (avg_depth, avg_expanded_nodes, avg_fringe_size)

# Print the results
for heuristic, (avg_depth, avg_expanded_nodes, avg_fringe_size) in results.items():
    print(f"Heuristic: {heuristic}")
    print(f"Average Depth: {avg_depth}")
    print(f"Average Expanded Nodes: {avg_expanded_nodes}")
    print(f"Average Fringe Size: {avg_fringe_size}")
    print("-------------------------------")
