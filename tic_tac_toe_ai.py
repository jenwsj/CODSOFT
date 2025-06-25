import math

# Initialize board
board = [' ' for _ in range(9)]

def print_board():
    print()
    for row in [board[i*3:(i+1)*3] for i in range(3)]:
        print('| ' + ' | '.join(row) + ' |')
    print()

def is_winner(brd, player):
    win_positions = [
        [0,1,2], [3,4,5], [6,7,8],  # rows
        [0,3,6], [1,4,7], [2,5,8],  # columns
        [0,4,8], [2,4,6]            # diagonals
    ]
    return any(all(brd[i] == player for i in line) for line in win_positions)

def is_draw(brd):
    return ' ' not in brd

def get_available_moves(brd):
    return [i for i, x in enumerate(brd) if x == ' ']

def minimax(brd, depth, is_maximizing):
    if is_winner(brd, 'O'):
        return 1
    elif is_winner(brd, 'X'):
        return -1
    elif is_draw(brd):
        return 0

    if is_maximizing:
        best_score = -math.inf
        for move in get_available_moves(brd):
            brd[move] = 'O'
            score = minimax(brd, depth + 1, False)
            brd[move] = ' '
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for move in get_available_moves(brd):
            brd[move] = 'X'
            score = minimax(brd, depth + 1, True)
            brd[move] = ' '
            best_score = min(score, best_score)
        return best_score

def best_move():
    best_score = -math.inf
    move = None
    for i in get_available_moves(board):
        board[i] = 'O'
        score = minimax(board, 0, False)
        board[i] = ' '
        if score > best_score:
            best_score = score
            move = i
    return move

def play():
    print("Welcome to Tic-Tac-Toe!")
    print("You are X, AI is O. Enter moves (1-9):")
    print_board()

    while True:
        # Human move
        try:
            move = int(input("Your move (1-9): ")) - 1
            if board[move] != ' ':
                print("Invalid move. Try again.")
                continue
        except:
            print("Invalid input.")
            continue

        board[move] = 'X'
        print_board()

        if is_winner(board, 'X'):
            print("You win!")
            break
        elif is_draw(board):
            print("It's a draw!")
            break

        # AI move
        ai = best_move()
        board[ai] = 'O'
        print("AI move:")
        print_board()

        if is_winner(board, 'O'):
            print("AI wins!")
            break
        elif is_draw(board):
            print("It's a draw!")
            break

play()
