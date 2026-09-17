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
├── LICENSE                  # MIT License
└── README.md                # Documentation
