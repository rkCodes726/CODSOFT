import math
import random

EMPTY = '_'

WIN_COMBOS = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),   # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),   # columns
    (0, 4, 8), (2, 4, 6)               # diagonals
]


# ---------- Core board functions ----------

def create_board():
    return [EMPTY] * 9


def print_board(board):
    print()
    for r in range(3):
        row = board[r * 3:(r + 1) * 3]
        print(' | '.join(row))
        if r < 2:
            print('---------')
    print()


def check_winner(board):
    for a, b, c in WIN_COMBOS:
        if board[a] != EMPTY and board[a] == board[b] == board[c]:
            return board[a]
    if EMPTY not in board:
        return 'Draw'
    return None


def empty_cells(board):
    return [i for i in range(9) if board[i] == EMPTY]


# ---------- Minimax ----------

def minimax(board, depth, is_maximizing, alpha, beta, ai_symbol, human_symbol, stats, use_pruning=True):
    stats['nodes'] += 1
    winner = check_winner(board)
    if winner == ai_symbol:
        return 10 - depth
    if winner == human_symbol:
        return depth - 10
    if winner == 'Draw':
        return 0

    if is_maximizing:
        best = -math.inf
        for i in empty_cells(board):
            board[i] = ai_symbol
            score = minimax(board, depth + 1, False, alpha, beta,
                             ai_symbol, human_symbol, stats, use_pruning)
            board[i] = EMPTY
            best = max(best, score)
            if use_pruning:
                alpha = max(alpha, best)
                if beta <= alpha:
                    break
        return best
    else:
        best = math.inf
        for i in empty_cells(board):
            board[i] = human_symbol
            score = minimax(board, depth + 1, True, alpha, beta,
                             ai_symbol, human_symbol, stats, use_pruning)
            board[i] = EMPTY
            best = min(best, score)
            if use_pruning:
                beta = min(beta, best)
                if beta <= alpha:
                    break
        return best


def evaluate_all_moves(board, ai_symbol, human_symbol):
    scores = {}
    for i in empty_cells(board):
        board[i] = ai_symbol
        stats = {'nodes': 0}
        score = minimax(board, 0, False, -math.inf, math.inf, ai_symbol, human_symbol, stats, True)
        board[i] = EMPTY
        scores[i] = score
    return scores


def find_ai_move(board, ai_symbol, human_symbol, difficulty):
    scores = evaluate_all_moves(board, ai_symbol, human_symbol)
    best_score = max(scores.values())
    best_moves = [i for i, s in scores.items() if s == best_score]
    optimal_move = random.choice(best_moves)

    random_chance = {'easy': 0.8, 'medium': 0.4, 'hard': 0.0}[difficulty]
    if random.random() < random_chance:
        chosen = random.choice(list(scores.keys()))
        return chosen, scores, (chosen != optimal_move)
    return optimal_move, scores, False


# ---------- Input helpers ----------

def get_human_move(board, label="Your"):
    while True:
        raw = input(f"{label} move (1-9): ").strip()
        if not raw.isdigit():
            print("Please enter a number between 1 and 9.")
            continue
        move = int(raw) - 1
        if move < 0 or move > 8 or board[move] != EMPTY:
            print("Invalid move (cell taken or out of range). Try again.")
            continue
        return move


def ask_choice(prompt, options):
    """options: dict like {'1': 'easy', '2': 'medium', '3': 'hard'}"""
    while True:
        print(prompt)
        for key, val in options.items():
            print(f"  {key}. {val}")
        choice = input("Enter choice: ").strip()
        if choice in options:
            return options[choice]
        print("Invalid choice, try again.\n")


# ---------- Game modes ----------

def play_vs_ai():
    difficulty = ask_choice("\nSelect difficulty:", {'1': 'easy', '2': 'medium', '3': 'hard'})
    human_symbol = ask_choice("\nChoose your symbol:", {'1': 'X', '2': 'O'})
    ai_symbol = 'O' if human_symbol == 'X' else 'X'
    first = ask_choice("\nWho goes first?", {'1': 'You', '2': 'AI'})

    wins = losses = draws = 0
    keep_playing = True

    while keep_playing:
        board = create_board()
        current = human_symbol if first == 'You' else ai_symbol
        print_board(list('123456789'))

        while True:
            if current == human_symbol:
                move = get_human_move(board)
                board[move] = human_symbol
            else:
                print("AI is thinking...\n")
                move, _, _ = find_ai_move(board, ai_symbol, human_symbol, difficulty)
                board[move] = ai_symbol
                print()

            print_board(board)
            winner = check_winner(board)
            if winner:
                if winner == 'Draw':
                    print("It's a draw!")
                    draws += 1
                elif winner == human_symbol:
                    print("You win!")
                    wins += 1
                else:
                    print("AI wins!")
                    losses += 1
                break

            current = ai_symbol if current == human_symbol else human_symbol

        print(f"\nSession score -> You: {wins}  AI: {losses}  Draws: {draws}")
        keep_playing = input("Play again? (y/n): ").strip().lower() == 'y'

    print("\nThanks for playing!")


if __name__ == "__main__":
    play_vs_ai()