import random
import math
import json
import argparse

ROWS, COLS = 6, 7
EMPTY = "."


def new_board():
    return tuple(tuple(EMPTY for _ in range(COLS)) for _ in range(ROWS))


def legal_columns(board):
    return [c for c in range(COLS) if board[0][c] == EMPTY]


def drop(board, column, player):
    if column not in legal_columns(board):
        return None
    result = [list(row) for row in board]
    for row in range(ROWS - 1, -1, -1):
        if result[row][column] == EMPTY:
            result[row][column] = player
            return tuple(tuple(r) for r in result)


def winner(board):
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for row in range(ROWS):
        for col in range(COLS):
            player = board[row][col]
            if player == EMPTY:
                continue
            for dr, dc in directions:
                end_r, end_c = row + 3 * dr, col + 3 * dc
                if 0 <= end_r < ROWS and 0 <= end_c < COLS:
                    if all(board[row + i * dr][col + i * dc] == player
                           for i in range(4)):
                        return player
    return None


def all_windows(board):
    for row in range(ROWS):
        for col in range(COLS):
            for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
                end_r, end_c = row + 3 * dr, col + 3 * dc
                if 0 <= end_r < ROWS and 0 <= end_c < COLS:
                    yield [board[row + i * dr][col + i * dc]
                           for i in range(4)]


def evaluate(board, player):
    opponent = "O" if player == "X" else "X"
    score = 0

    for window in all_windows(board):
        mine, theirs = window.count(player), window.count(opponent)
        empty = window.count(EMPTY)

        if theirs == 0:
            score += {1: 2, 2: 12, 3: 65, 4: 100000}.get(mine, 0)
        if mine == 0:
            score -= {1: 2, 2: 12, 3: 75, 4: 100000}.get(theirs, 0)

    score += sum(4 if board[r][3] == player else
                 -4 if board[r][3] == opponent else 0
                 for r in range(ROWS))
    return score


def wins_if_dropped(board, column, player):
    next_board = drop(board, column, player)
    return next_board is not None and winner(next_board) == player


def threat_count(board, player):
    return sum(wins_if_dropped(board, c, player)
               for c in legal_columns(board))


def ordered_columns(board, player, use_rules=True):
    columns = legal_columns(board)
    if not use_rules:
        return columns

    opponent = "O" if player == "X" else "X"

    def priority(column):
        next_board = drop(board, column, player)
        creates_threats = threat_count(next_board, player)
        return (
            wins_if_dropped(board, column, player),       # 1. Win
            wins_if_dropped(board, column, opponent),     # 2. Block
            column == 3,                                  # 3. Centre
            creates_threats,                             # 4. Threats
            -abs(column - 3)
        )

    return sorted(columns, key=priority, reverse=True)


def alpha_beta(board, turn, depth, alpha, beta, player, use_rules, stats):
    stats["nodes"] += 1
    won = winner(board)

    if won == player:
        return 100000 + depth
    if won is not None:
        return -100000 - depth
    if depth == 0 or not legal_columns(board):
        return evaluate(board, player)

    maximizing = (turn == player)
    best = -math.inf if maximizing else math.inf

    for column in ordered_columns(board, turn, use_rules):
        next_board = drop(board, column, turn)
        next_turn = "O" if turn == "X" else "X"
        score = alpha_beta(
            next_board, next_turn, depth - 1, alpha, beta,
            player, use_rules, stats
        )

        if maximizing:
            best = max(best, score)
            alpha = max(alpha, best)
        else:
            best = min(best, score)
            beta = min(beta, best)

        if beta <= alpha:
            break

    return best


def choose_minimax_move(board, player="X", depth=4, use_rules=True):
    stats = {"nodes": 0}
    best_column, best_score = None, -math.inf

    for column in ordered_columns(board, player, use_rules):
        next_board = drop(board, column, player)
        score = alpha_beta(
            next_board, "O" if player == "X" else "X",
            depth - 1, -math.inf, math.inf, player, use_rules, stats
        )
        if score > best_score:
            best_column, best_score = column, score

    return best_column, best_score, stats


def force_win(board, turn, target, moves_left, memo):
    """Check whether target can force a win on exactly its Nth move."""
    won = winner(board)
    if won is not None:
        return won == target and moves_left == 0
    if moves_left == 0:
        return False

    key = (board, turn, target, moves_left)
    if key in memo:
        return memo[key]

    columns = legal_columns(board)
    if not columns:
        return False

    if turn == target:
        # Target needs one move that keeps a forced win possible.
        answer = False
        for column in columns:
            next_board = drop(board, column, turn)
            if force_win(
                next_board, "O" if turn == "X" else "X",
                target, moves_left - 1, memo
            ):
                answer = True
                break
    else:
        # Every opponent reply must still allow the forced win.
        answer = True
        for column in columns:
            next_board = drop(board, column, turn)
            if winner(next_board) == turn or not force_win(
                next_board, "O" if turn == "X" else "X",
                target, moves_left, memo
            ):
                answer = False
                break

    memo[key] = answer
    return answer


def generate_puzzle(moves_to_win=2, seed=17):
    rng = random.Random(seed)

    for _ in range(30000):
        board, turn = new_board(), "X"

        # Make a random legal board without an existing winner.
        for _ in range(rng.randint(8, 18)):
            choices = [
                c for c in legal_columns(board)
                if winner(drop(board, c, turn)) is None
            ]
            if not choices:
                break
            board = drop(board, rng.choice(choices), turn)
            turn = "O" if turn == "X" else "X"

        if winner(board) is not None:
            continue

        x_count = sum(row.count("X") for row in board)
        o_count = sum(row.count("O") for row in board)
        if abs(x_count - o_count) > 1:
            continue

        player = "X" if x_count == o_count else "O"
        if force_win(board, player, player, moves_to_win, {}):
            return board, player, x_count, o_count

    raise RuntimeError("No puzzle found. Run again or reduce moves_to_win.")


def monte_carlo_columns(board, player, samples=250, seed=1):
    rng = random.Random(seed)
    results = {}

    for column in legal_columns(board):
        wins = 0
        for _ in range(samples):
            game = drop(board, column, player)
            turn = "O" if player == "X" else "X"

            while game and winner(game) is None and legal_columns(game):
                move = rng.choice(legal_columns(game))
                game = drop(game, move, turn)
                turn = "O" if turn == "X" else "X"

            wins += int(game is not None and winner(game) == player)

        results[column] = wins / samples

    return results


def board_string(board):
    return "\n".join(" ".join(row) for row in board) + "\n0 1 2 3 4 5 6"


def write_chart(probabilities, scores, filename="column_chart.svg"):
    peak = max((abs(value) for value in scores.values()), default=1) or 1
    svg = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="760" height="360">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<text x="380" y="28" text-anchor="middle" font-family="Arial" '
        'font-size="20">Connect Four: Column Comparison</text>',
        '<text x="55" y="58" font-family="Arial" font-size="12">'
        'Blue: Monte Carlo win probability (%) | Orange: Minimax score (scaled)'
        '</text>'
    ]

    for index, column in enumerate(sorted(probabilities)):
        x = 85 + index * 92
        probability_height = probabilities[column] * 200
        scaled_score = max(0, min(1, (scores[column] / peak + 1) / 2))
        score_height = scaled_score * 200

        svg.extend([
            f'<rect x="{x}" y="{270-probability_height}" width="24" '
            f'height="{probability_height}" fill="#3b82f6"/>',
            f'<rect x="{x+28}" y="{270-score_height}" width="24" '
            f'height="{score_height}" fill="#f59e0b"/>',
            f'<text x="{x+25}" y="295" text-anchor="middle" '
            f'font-family="Arial" font-size="13">{column}</text>',
            f'<text x="{x+12}" y="{260-probability_height}" '
            f'text-anchor="middle" font-family="Arial" font-size="10">'
            f'{probabilities[column]*100:.0f}%</text>'
        ])

    svg.append(
        '<text x="380" y="330" text-anchor="middle" font-family="Arial" '
        'font-size="13">Column (0–6); bar scales differ</text></svg>'
    )
    with open(filename, "w", encoding="utf-8") as file:
        file.write("\n".join(svg))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--samples", type=int, default=250)
    parser.add_argument("--games", type=int, default=8)
    parser.add_argument("--output", default="results.json")
    args = parser.parse_args()

    # Fixed legal board to compare node counts fairly.
    board = new_board()
    setup = [(0, "X"), (1, "O"), (0, "X"), (1, "O"),
             (2, "X"), (1, "O"), (2, "X"), (4, "O")]
    for column, player in setup:
        board = drop(board, column, player)

    _, _, ordered_stats = choose_minimax_move(board, "X", 4, True)
    _, _, plain_stats = choose_minimax_move(board, "X", 4, False)

    probabilities = monte_carlo_columns(
        board, "X", args.samples, args.seed
    )
    scores = {
        c: evaluate(drop(board, c, "X"), "X")
        for c in legal_columns(board)
    }

    # Minimax (X) vs rollout agent (O).
    outcomes = {"minimax_wins": 0, "rollout_wins": 0, "draws": 0}
    for game_number in range(args.games):
        game, turn = new_board(), "X"

        while legal_columns(game) and winner(game) is None:
            if turn == "X":
                move, _, _ = choose_minimax_move(game, "X", 3, True)
            else:
                estimates = monte_carlo_columns(
                    game, "O", max(20, args.samples // 4),
                    args.seed + game_number
                )
                move = max(estimates, key=estimates.get)

            game = drop(game, move, turn)
            turn = "O" if turn == "X" else "X"

        result = winner(game)
        if result == "X":
            outcomes["minimax_wins"] += 1
        elif result == "O":
            outcomes["rollout_wins"] += 1
        else:
            outcomes["draws"] += 1

    puzzles = []
    for number in range(3):
        puzzle, player, x_count, o_count = generate_puzzle(
            2, args.seed + number * 11
        )
        puzzles.append({
            "player": player,
            "win_in": 2,
            "counts": {"X": x_count, "O": o_count},
            "board": [list(row) for row in puzzle]
        })

    results = {
        "node_counts": {
            "with_rule_ordering": ordered_stats["nodes"],
            "without_rule_ordering": plain_stats["nodes"]
        },
        "column_results": {
            str(c): {
                "monte_carlo_win_probability": probabilities[c],
                "minimax_score": scores[c]
            } for c in probabilities
        },
        "agent_win_rates": {
            name: count / args.games
            for name, count in outcomes.items()
        },
        "games_played": args.games,
        "puzzles": puzzles
    }

    with open(args.output, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=2)

    write_chart(probabilities, scores)

    print("Alpha-beta node comparison:")
    print("With rule ordering:", ordered_stats["nodes"])
    print("Without rule ordering:", plain_stats["nodes"])
    print("\nPer-column results:")
    for column in probabilities:
        print(
            f"Column {column}: Monte Carlo win probability "
            f"{probabilities[column]:.1%}; Minimax score {scores[column]}"
        )
    print("\nAgent win rates:")
    for name, rate in results["agent_win_rates"].items():
        print(f"{name}: {rate:.1%}")

    for number, puzzle in enumerate(puzzles, 1):
        print(f"\nPuzzle {number}: Player {puzzle['player']} to win "
              f"in exactly 2 moves")
        for row in puzzle["board"]:
            print(" ".join(row))
        print("0 1 2 3 4 5 6")
        print("Piece counts:", puzzle["counts"])

    print(f"\nSaved results to {args.output}")
    print("Saved chart to column_chart.svg")


if __name__ == "__main__":
    main()