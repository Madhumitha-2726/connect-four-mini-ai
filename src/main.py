import time
from minimax import (
    ROWS,
    COLS,
    EMPTY,
    HUMAN,
    AI,
    get_next_open_row,
    drop_piece,
    is_winning_move,
    get_valid_columns,
    minimax,
    seed_game
)

STUDENT_REG_NO = "VH15231"
SEARCH_DEPTH = 4


def create_board():
    return [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]


def print_board(board):
    print("\n  1   2   3   4   5   6   7")
    for row in board:
        print(
            "| " +
            " | ".join(
                "." if cell == EMPTY
                else "X" if cell == HUMAN
                else "O"
                for cell in row
            ) +
            " |"
        )
    print("-----------------------------")


def get_human_move(board):
    while True:
        try:
            col = int(input("Choose a column (1-7): ")) - 1
            if col not in range(COLS):
                print("Please enter a number between 1 and 7.")
                continue
            if col not in get_valid_columns(board):
                print("Column is full. Choose another.")
                continue
            return col
        except ValueError:
            print("Invalid input. Enter a number (1-7).")


def play_game():
    seed_game(STUDENT_REG_NO)
    board = create_board()

    print("\n================================")
    print("       CONNECT FOUR MINI AI")
    print("================================")
    print(f"Register No : {STUDENT_REG_NO}")
    print(f"Search Depth: {SEARCH_DEPTH}")
    print("Human = X | AI = O")

    game_over = False

    while not game_over:
        print_board(board)
        human_col = get_human_move(board)
        human_row = get_next_open_row(board, human_col)
        drop_piece(board, human_row, human_col, HUMAN)

        if is_winning_move(board, HUMAN):
            print_board(board)
            print("🎉 Human wins!")
            break

        if not get_valid_columns(board):
            print_board(board)
            print("🤝 Game Draw!")
            break

        print("\n🤖 AI is thinking...")
        start_time = time.time()
        ai_col, ai_score = minimax(board, SEARCH_DEPTH, True)
        elapsed = time.time() - start_time

        ai_row = get_next_open_row(board, ai_col)
        drop_piece(board, ai_row, ai_col, AI)

        print(f"AI selected column: {ai_col + 1}")
        print(f"Evaluation score  : {ai_score}")
        print(f"Thinking time     : {elapsed:.4f}s")

        if is_winning_move(board, AI):
            print_board(board)
            print("🤖 AI wins!")
            break

        if not get_valid_columns(board):
            print_board(board)
            print("🤝 Game Draw!")
            break


if __name__ == "__main__":
    play_game()
