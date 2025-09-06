import math
import random

ROWS = 6
COLUMNS = 7
PLAYER = 0
AI = 1
PLAYER_PIECE = 1
AI_PIECE = 2
EMPTY = 0
WINDOW_LENGTH = 4

def create_board():
    return [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROWS-1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROWS):
        if board[r][col] == 0:
            return r

def print_board(board):
    for row in reversed(board):
        print(row)

def winning_move(board, piece):
    
    for r in range(ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r][c + i] == piece for i in range(4)):
                return True

    
    for c in range(COLUMNS):
        for r in range(ROWS - 3):
            if all(board[r + i][c] == piece for i in range(4)):
                return True

    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            if all(board[r + i][c + i] == piece for i in range(4)):
                return True

    for r in range(3, ROWS):
        for c in range(COLUMNS - 3):
            if all(board[r - i][c + i] == piece for i in range(4)):
                return True

    return False

def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score

def score_position(board, piece):
    score = 0

    center_array = [board[r][COLUMNS // 2] for r in range(ROWS)]
    score += center_array.count(piece) * 3

    for r in range(ROWS):
        row_array = board[r]
        for c in range(COLUMNS - 3):
            window = row_array[c:c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    for c in range(COLUMNS):
        col_array = [board[r][c] for r in range(ROWS)]
        for r in range(ROWS - 3):
            window = col_array[r:r + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    for r in range(ROWS - 3):
        for c in range(COLUMNS - 3):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    for r in range(3, ROWS):
        for c in range(COLUMNS - 3):
            window = [board[r - i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score

def get_valid_locations(board):
    return [col for col in range(COLUMNS) if is_valid_location(board, col)]

def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

def minimax(board, depth, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)

    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 100000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -100000)
            else:  # Game is over, no moves
                return (None, 0)
        else:  # Depth is zero
            return (None, score_position(board, AI_PIECE))

    if maximizingPlayer:
        value = -math.inf
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = [row[:] for row in board]
            drop_piece(temp_board, row, col, AI_PIECE)
            new_score = minimax(temp_board, depth - 1, False)[1]
            if new_score > value:
                value = new_score
                best_col = col
        return best_col, value

    else:  
        value = math.inf
        best_col = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = [row[:] for row in board]
            drop_piece(temp_board, row, col, PLAYER_PIECE)
            new_score = minimax(temp_board, depth - 1, True)[1]
            if new_score < value:
                value = new_score
                best_col = col
        return best_col, value

def play_game():
    board = create_board()
    print("Welcome to Connect Four!")
    print_board(board)
    game_over = False
    turn = random.randint(PLAYER, AI)

    while not game_over:
        if turn == PLAYER:
            valid_input = False
            while not valid_input:
                user_input = input("Your turn! Choose column (0–6): ")
                if user_input.isdigit():
                    col = int(user_input)
                    if 0 <= col <= 6:
                        if is_valid_location(board, col):
                            valid_input = True
                        else:
                            print("❌ That column is full. Try another one.")
                    else:
                        print("❌ Invalid column. Enter a number from 0 to 6.")
                else:
                    print("❌ Please enter a valid number between 0 and 6.")

            row = get_next_open_row(board, col)
            drop_piece(board, row, col, PLAYER_PIECE)

            if winning_move(board, PLAYER_PIECE):
                print_board(board)
                print("🎉 You win!")
                game_over = True
            else:
                turn = AI
                print_board(board)

        else:  
            print("AI is thinking...")
            col, _ = minimax(board, 4, True)
            if is_valid_location(board, col):
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, AI_PIECE)

                print(f"🤖 AI placed in column {col}, row {row}")

                if winning_move(board, AI_PIECE):
                    print_board(board)
                    print("😞 AI wins!")
                    game_over = True
                else:
                    turn = PLAYER
                    print_board(board)


       
        if not game_over and len(get_valid_locations(board)) == 0:
            print("🤝 It's a draw!")
            game_over = True


play_game()
