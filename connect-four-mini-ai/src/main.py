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
    minimax
)


SEARCH_DEPTH = 4


def create_board():
    """Create an empty Connect Four board."""
    return [
        [EMPTY for _ in range(COLS)]
        for _ in range(ROWS)
    ]


def print_board(board):
    """Display the board."""

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
    """Read and validate the human player's move."""

    while True:

        try:
            column = int(
                input("Choose a column (1-7): ")
            ) - 1

            if column not in range(COLS):
                print("Please enter a number from 1 to 7.")
                continue

            if column not in get_valid_columns(board):
                print("That column is full.")
                continue

            return column

        except ValueError:
            print("Invalid input. Enter a number from 1 to 7.")


def play_game():
    """Run one complete Connect Four game."""

    board = create_board()

    print("\n================================")
    print("       CONNECT FOUR MINI AI")
    print("================================")
    print("Human = X")
    print("AI    = O")
    print(f"Minimax Search Depth = {SEARCH_DEPTH}")

    game_over = False

    while not game_over:

        # Human turn
        print_board(board)

        human_column = get_human_move(board)
        human_row = get_next_open_row(
            board,
            human_column
        )

        drop_piece(
            board,
            human_row,
            human_column,
            HUMAN
        )

        if is_winning_move(board, HUMAN):

            print_board(board)
            print("🎉 Human wins!")
            game_over = True
            continue

        if not get_valid_columns(board):

            print_board(board)
            print("Game Draw!")
            break

        # AI turn
        print("\nAI is thinking...")

        ai_column, ai_score = minimax(
            board,
            SEARCH_DEPTH,
            True
        )

        ai_row = get_next_open_row(
            board,
            ai_column
        )

        drop_piece(
            board,
            ai_row,
            ai_column,
            AI
        )

        print(
            f"AI selected column: {ai_column + 1}"
        )
        print(
            f"Evaluation score: {ai_score}"
        )

        if is_winning_move(board, AI):

            print_board(board)
            print("🤖 AI wins!")
            game_over = True


if __name__ == "__main__":
    play_game()