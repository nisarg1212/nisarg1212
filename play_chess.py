import os
import re
import random
import chess
import chess.svg

def main():
    # Read the issue title passed from GitHub Actions
    issue_title = os.environ.get("ISSUE_TITLE", "")
    
    # Try to extract a move in UCI format (e.g., "e2e4")
    match = re.search(r'Chess Move:\s*([a-h][1-8][a-h][1-8][qrbn]?)', issue_title, re.IGNORECASE)
    
    # Try to load existing board state, otherwise create a new game
    try:
        with open("chess_board.fen", "r") as f:
            fen = f.read().strip()
        board = chess.Board(fen)
    except Exception:
        board = chess.Board()

    # If the action was triggered by a valid move issue
    if match:
        user_move_str = match.group(1).lower()
        try:
            user_move = chess.Move.from_uci(user_move_str)
            if user_move in board.legal_moves:
                print(f"Applying user move: {user_move_str}")
                board.push(user_move)
                
                # Make AI move (currently plays randomly, but you can plug in Stockfish later!)
                if not board.is_game_over():
                    ai_move = random.choice(list(board.legal_moves))
                    print(f"Applying AI move: {ai_move}")
                    board.push(ai_move)
            else:
                print(f"Illegal move requested: {user_move_str}")
        except ValueError:
            print("Invalid move format.")
    else:
        print("No move found, rendering current/initial state.")
        
    # Reset game if it's over
    if board.is_game_over():
        print("Game over! Resetting board.")
        board.reset()
        
    # Save the updated game state
    with open("chess_board.fen", "w") as f:
        f.write(board.fen())
        
    # Generate the chessboard SVG image
    with open("chess_board.svg", "w") as f:
        f.write(chess.svg.board(board, size=400))

if __name__ == "__main__":
    main()
