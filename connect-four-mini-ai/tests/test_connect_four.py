import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "../src"
        )
    )
)

from minimax import (
    ROWS,
    COLS,
    EMPTY,
    HUMAN,
    AI,
    get_valid_columns,
    get_next_open_row,
    drop_piece,
    is_winning_move,
    score_position,
    minimax
)


def create_board():
    return [
        [EMPTY for _ in range(COLS)]
        for _ in range(ROWS)
    ]


def test_empty_board():

    board = create_board()

    assert len(get_valid_columns(board)) == 7


def test_drop_piece():

    board = create_board()

    row = get_next_open_row(board, 0)

    drop_piece(board, row, 0, HUMAN)

    assert board[5][0] == HUMAN


def test_horizontal_win():

    board = create_board()

    for col in range(4):
        drop_piece(board, 5, col, HUMAN)

    assert is_winning_move(board, HUMAN)


def test_vertical_win():

    board = create_board()

    for row in range(2, 6):
        drop_piece(board, row, 0, HUMAN)

    assert is_winning_move(board, HUMAN)


def test_ai_evaluation():

    board = create_board()

    drop_piece(board, 5, 3, AI)
    drop_piece(board, 5, 4, AI)

    score = score_position(board, AI)

    assert score > 0


def test_minimax_returns_valid_column():

    board = create_board()

    column, score = minimax(
        board,
        2,
        True
    )

    assert column in range(COLS)