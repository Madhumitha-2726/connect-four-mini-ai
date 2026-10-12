# Connect Four Mini AI

An intelligent Connect Four game agent implemented in Python using Depth-Limited Minimax Search with a static heuristic evaluation function.

## Student Information
- **Student Name:** Madhumitha N
- **Register Number:** VH15231
- **Course / Topic:** Connect Four Mini AI · Minimax

## Problem Statement
Connect Four is a two-player zero-sum board game on a 6x7 grid. The agent aims to achieve four connected discs (horizontal, vertical, or diagonal) while blocking the human opponent.

## AI Technique & Approach
- **Algorithm:** Depth-Limited Minimax
- **Search Depth:** `4`
- **Evaluation Heuristic:** Scores 4-slot sliding windows:
  - 4-in-a-row (Terminal Win): $+100$
  - 3-in-a-row + 1 empty: $+5$
  - 2-in-a-row + 2 empty: $+2$
  - Opponent 3-in-a-row (Threat Block): $-4$
  - Center column pieces weighted higher ($+3$ per disc).

## Project Structure
```text
connect-four-mini-ai/
├── src/
│   ├── main.py              # Main game loop
│   └── minimax.py           # Minimax algorithm & heuristic function
├── tests/
│   └── test_connect_four.py # Unit tests
├── docs/
│   └── report.pdf           # 2-4 page project report
├── requirements.txt         # Dependencies
├── .gitignore

## Final Project Extension

This project extends the Connect Four Mini AI using explainable decision-making and puzzle generation.

### 1. Features Implemented

- **Depth-Limited Minimax:** Searches possible moves up to a selected depth and evaluates non-terminal board states.
- **Rule-Based Move Ordering:** Prioritizes immediate winning moves, blocking the opponent, centre-column moves, and threat creation.
- **Alpha-Beta Pruning Comparison:** Compares the number of nodes searched with and without rule-based move ordering.
- **CSP Puzzle Generator:** Generates Connect Four win-in-N puzzles using backtracking and constraint propagation.
- **Monte Carlo Rollouts:** Estimates winning probabilities for possible column moves and compares the results with the Minimax agent.
- **Puzzle Verification:** Checks generated puzzles using the Minimax algorithm.

### 2. How to Run

1. Clone or download this repository.
2. Install the dependencies listed in `requirements.txt`, if required.
3. Open a terminal in the project directory.
4. Run the main program:

```bash
python src/main.py
```

5. Run the extension program:

```bash
python src/extension.py
```

### 3. Experiments and Results

The final project evaluates:

- Nodes searched with and without rule-based move ordering.
- Minimax versus Monte Carlo rollout agent win-rates.
- Estimated win probability for each column.
- Three generated win-in-N puzzles and their verification results.

Add actual screenshots, measurements, and outputs from your program here.

### 4. Reflection

This project helped me understand game-tree search, heuristic evaluation, alpha-beta pruning, constraint satisfaction, backtracking, and Monte Carlo simulation. One challenge was combining puzzle generation with reliable move selection and verification.

### 5. Acknowledgement

AI assistance and external references, if used, should be acknowledged here. The implementation and results should be reviewed and understood by the author.

├── LICENSE                  # MIT License
└── README.md                # Documentation
