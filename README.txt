An Honours Project for the School of Computer Science at Carleton University.
Supervised by Anil Maheshwari.

Simulation of Dynamic Fleet Routing for public transpo busses.

Reference Paper: https://dspace.mit.edu/bitstream/handle/1721.1/112051/1006509328-MIT.pdf

To test your own heuristic:
    1. Add your heuristic handler function in \heuristics
    2. Add the function in \heuristics\Heuristics.py
    3. Change main.py to run `simulate_full_day(HeuristicEnums.YOUR_HEURISTICS)`
    4. Run in tmux session
        - open tmux session `tmux`
        - start simulation `python3 main.py > output/filename.out`