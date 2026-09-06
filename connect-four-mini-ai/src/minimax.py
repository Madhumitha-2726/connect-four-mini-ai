import math


ROWS = 6
COLS = 7

EMPTY = 0
HUMAN = 1
AI = 2


def get_valid_columns(board):
    """Return columns where another piece can be dropped."""
    return [
        col for col in range(COLS)
        if board[0][col] == EMPTY
    ]


def get_next_open_row(board, col):
    """Return the lowest empty row in a column."""
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == EMPTY:
            return row

    return None


def drop_piece(board, row, col, piece):
    """Place a piece on the board."""
    board[row][col] = piece


def is_winning_move(board, piece):
    """Check whether the given player has four connected pieces."""

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
            if all(
                board[row + i][col + i] == piece
                for i in range(4)
            ):
                return True

    # Negative diagonal
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(
                board[row - i][col + i] == piece
                for i in range(4)
            ):
                return True

    return False


def evaluate_window(window, piece):
    """Evaluate a group of four cells."""

    score = 0

    opponent = HUMAN if piece == AI else AI

    # Four in a row
    if window.count(piece) == 4:
        score += 100

    # Three pieces + empty
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5

    # Two pieces + two empty
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    # Block opponent's winning opportunity
    if window.count(opponent) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score


def score_position(board, piece):
    """
    Static evaluation function for a non-terminal board.
    Higher score means the position is better for the AI.
    """

    score = 0

    # Prefer the center column
    center_column = [
        board[row][COLS // 2]
        for row in range(ROWS)
    ]

    center_count = center_column.count(piece)
    score += center_count * 3

    # Horizontal windows
    for row in range(ROWS):
        for col in range(COLS - 3):
            window = board[row][col:col + 4]
            score += evaluate_window(window, piece)

    # Vertical windows
    for col in range(COLS):
        for row in range(ROWS - 3):
            window = [
                board[row + i][col]
                for i in range(4)
            ]
            score += evaluate_window(window, piece)

    # Positive diagonals
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            window = [
                board[row + i][col + i]
                for i in range(4)
            ]
            score += evaluate_window(window, piece)

    # Negative diagonals
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            window = [
                board[row - i][col + i]
                for i in range(4)
            ]
            score += evaluate_window(window, piece)

    return score


def is_terminal_node(board):
    """Check whether the game has ended."""

    return (
        is_winning_move(board, HUMAN)
        or is_winning_move(board, AI)
        or len(get_valid_columns(board)) == 0
    )


def minimax(board, depth, maximizing_player):
    """
    Depth-limited Minimax algorithm.

    Returns:
        best_column, evaluation_score
    """

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

            _, score = minimax(
                temp_board,
                depth - 1,
                False
            )

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

            _, score = minimax(
                temp_board,
                depth - 1,
                True
            )

            if score < best_score:
                best_score = score
                best_column = col

        return best_column, best_score