import math
import random

ROWS = 6
COLS = 7

EMPTY = 0
HUMAN = 1
AI = 2

nodes_expanded = 0


def seed_game(register_number: str = "VH15231"):
    """Seed randomness using student register number."""
    digits = "".join(filter(str.isdigit, str(register_number)))
    seed_val = int(digits) if digits else 42
    random.seed(seed_val)


def get_valid_columns(board):
    return [col for col in range(COLS) if board[0][col] == EMPTY]


def get_next_open_row(board, col):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == EMPTY:
            return row
    return None


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_winning_move(board, piece):
    # Horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == piece for i in range(4)):
                return True

    # Vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + i][col] == piece for i in range(4)):
                return True

    # Positive diagonal
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == piece for i in range(4)):
                return True

    # Negative diagonal
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == piece for i in range(4)):
                return True

    return False


def evaluate_window(window, piece):
    score = 0
    opponent = HUMAN if piece == AI else AI

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opponent) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score


def score_position(board, piece):
    score = 0

    # Center column preference
    center_column = [board[row][COLS // 2] for row in range(ROWS)]
    center_count = center_column.count(piece)
    score += center_count * 3

    # Horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            window = board[row][col:col + 4]
            score += evaluate_window(window, piece)

    # Vertical
    for col in range(COLS):
        for row in range(ROWS - 3):
            window = [board[row + i][col] for row in range(4)]
            score += evaluate_window(window, piece)

    # Positive diagonals
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            window = [board[row + i][col + i] for i in range(4)]
            score += evaluate_window(window, piece)

    # Negative diagonals
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            window = [board[row - i][col + i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score


def is_terminal_node(board):
    return (
        is_winning_move(board, HUMAN)
        or is_winning_move(board, AI)
        or len(get_valid_columns(board)) == 0
    )


def minimax(board, depth, maximizing_player):
    global nodes_expanded
    nodes_expanded += 1

    valid_columns = get_valid_columns(board)
    terminal = is_terminal_node(board)

    if depth == 0 or terminal:
        if terminal:
            if is_winning_move(board, AI):
                return None, 1_000_000
            if is_winning_move(board, HUMAN):
                return None, -1_000_000
            return None, 0
        return None, score_position(board, AI)

    if maximizing_player:
        best_score = -math.inf
        best_column = valid_columns[0]
        for col in valid_columns:
            row = get_next_open_row(board, col)
            temp_board = [r[:] for r in board]
            drop_piece(temp_board, row, col, AI)
            _, score = minimax(temp_board, depth - 1, False)
            if score > best_score:
                best_score = score
                best_column = col
        return best_column, best_score
    else:
        best_score = math.inf
        best_column = valid_columns[0]
        for col in valid_columns:
            row = get_next_open_row(board, col)
            temp_board = [r[:] for r in board]
            drop_piece(temp_board, row, col, HUMAN)
            _, score = minimax(temp_board, depth - 1, True)
            if score < best_score:
                best_score = score
                best_column = col
        return best_column, best_score
