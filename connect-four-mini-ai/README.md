# Connect Four Mini AI

## Batch 17

### Students

- VH15231 – Madhumitha N
- VH15159 – Madhumitha R S
- VH15184 – Maheshkumar M

## Project Description

Connect Four Mini AI is a two-player Connect Four game in which a human
player competes against an Artificial Intelligence agent.

The AI uses a depth-limited Minimax algorithm to select its moves.

## AI Technique

The project uses:

- Minimax
- Depth-limited search
- Static evaluation function
- Board-state evaluation

The search depth used in this implementation is:

`Depth = 4`

## How Minimax Works

The AI considers possible future moves.

At the maximizing level, the AI tries to maximize the evaluation score.

At the minimizing level, the AI assumes that the human player will choose
moves that minimize the AI's score.

The search stops when:

1. The selected depth is reached.
2. A player wins.
3. The board is full.

## Evaluation Function

The evaluation function scores non-terminal board positions.

It considers:

- Four connected AI pieces
- Three AI pieces with one empty position
- Two AI pieces with two empty positions
- Blocking opponent opportunities
- Center column preference

Higher scores represent better positions for the AI.

## Project Structure

```text
connect-four-mini-ai/
│
├── src/
│   ├── main.py
│   └── minimax.py
│
├── tests/
│   └── test_connect_four.py
│
├── docs/
│   └── screenshots/
│
├── README.md
├── requirements.txt
├── .gitignore
└── LICENSE