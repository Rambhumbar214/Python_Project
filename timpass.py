import tkinter as tk
import random
import pygame

# Initialize pygame mixer for sound
pygame.mixer.init()

# Load sound effects (ensure you have these files or replace with your own sound files)
move_sound = pygame.mixer.Sound("move_sound.wav")  # Replace with your move sound file
win_sound = pygame.mixer.Sound("win_sound.wav")    # Replace with your win sound file
tie_sound = pygame.mixer.Sound("gameover.wav")    # Replace with your tie sound file

# Initialize the game variables
current_player = "X"
board = [[" " for _ in range(3)] for _ in range(3)]
buttons = [[None for _ in range(3)] for _ in range(3)]
difficulty = "Easy"  # Default difficulty
root = None  # Declare root here to make it accessible globally
game_mode = "AI"  # Default game mode (AI mode)
player_x_score = 0
player_o_score = 0

# Function to set the game mode (AI or 2-Player)
def set_game_mode(mode):
    global game_mode
    game_mode = mode
    if game_mode == "AI":
        set_difficulty_menu()  # Show the difficulty menu if AI is selected
    else:
        restart_game()  # Start the game in 2-player mode

# Function to set the difficulty menu for AI
def set_difficulty_menu():
    for widget in root.winfo_children():
        widget.destroy()

    difficulty_label = tk.Label(root, text="Select Difficulty Level", font=("Helvetica", 20))
    difficulty_label.pack(pady=20)

    easy_button = tk.Button(root, text="Easy", font=("Helvetica", 14), command=lambda: set_difficulty("Easy"))
    easy_button.pack(pady=5)

    medium_button = tk.Button(root, text="Medium", font=("Helvetica", 14), command=lambda: set_difficulty("Medium"))
    medium_button.pack(pady=5)

    hard_button = tk.Button(root, text="Hard", font=("Helvetica", 14), command=lambda: set_difficulty("Hard"))
    hard_button.pack(pady=5)

def set_difficulty(level):
    global difficulty
    difficulty = level
    restart_game()  # After selecting difficulty, start/restart the game

# Function to check for a win and return the winning line (row, column, or diagonal)
def check_win(board, player):
    # Check rows and columns for a win
    for i in range(3):
        if all([board[i][j] == player for j in range(3)]):
            return 'row', i
        if all([board[j][i] == player for j in range(3)]):
            return 'col', i
    
    # Check diagonals for a win
    if all([board[i][i] == player for i in range(3)]):
        return 'diag1', 0
    if all([board[i][2-i] == player for i in range(3)]):
        return 'diag2', 0
    
    return None, None

# Function to handle player moves
def player_move(row, col):
    global current_player
    if board[row][col] == " ":
        board[row][col] = current_player
        buttons[row][col].config(text=current_player)
        move_sound.play()  # Play sound when a move is made
        
        # Check for a winner
        win_type, win_index = check_win(board, current_player)
        if win_type:
            label.config(text=f"Player {current_player} wins!")
            win_sound.play()  # Play sound when a player wins
            highlight_win(win_type, win_index)
            update_score(current_player)
            show_restart_button()
            return
        
        # Check for a tie
        if all(board[i][j] != " " for i in range(3) for j in range(3)):
            label.config(text="It's a tie!")
            tie_sound.play()  # Play sound when it's a tie
            show_restart_button()
            return
        
        # Switch player and make the AI move if AI mode
        current_player = "O" if current_player == "X" else "X"
        label.config(text=f"Player {current_player}'s turn")
        if game_mode == "AI" and current_player == "O":  # AI's turn
            ai_move()

# Function to highlight the winning line
def highlight_win(win_type, win_index):
    if win_type == 'row':
        for j in range(3):
            buttons[win_index][j].config(bg="green")
    elif win_type == 'col':
        for i in range(3):
            buttons[i][win_index].config(bg="green")
    elif win_type == 'diag1':
        for i in range(3):
            buttons[i][i].config(bg="green")
    elif win_type == 'diag2':
        for i in range(3):
            buttons[i][2-i].config(bg="green")

# Function to disable buttons after a win or tie
def disable_buttons():
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(state="disabled")

# Function to update score
def update_score(winner):
    global player_x_score, player_o_score
    if winner == "X":
        player_x_score += 1
    else:
        player_o_score += 1
    update_score_display()

# Function to update the score display
def update_score_display():
    score_label.config(text=f"Player X: {player_x_score}  |  Player O: {player_o_score}")

# Function to show the Restart button
def show_restart_button():
    restart_button.pack(pady=20)  # Show restart button when the game ends

# Function to restart the game
def restart_game():
    global current_player, board, buttons
    current_player = "X"
    board = [[" " for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(text=" ", bg="lightgray", state="normal")
    label.config(text="Player X's turn")
    restart_button.pack_forget()  # Hide restart button after restarting

# AI move (random or optimal depending on the level)
def ai_move():
    if difficulty == "Easy":
        easy_ai_move()
    elif difficulty == "Medium":
        medium_ai_move()
    elif difficulty == "Hard":
        hard_ai_move()

# Easy AI (random move)
def easy_ai_move():
    empty_cells = [(i, j) for i in range(3) for j in range(3) if board[i][j] == " "]
    row, col = random.choice(empty_cells)
    board[row][col] = "O"
    buttons[row][col].config(text="O")
    move_sound.play()  # Play sound when AI makes a move
    
    # Check for winner or tie
    check_game_over()

# Medium AI (blocks winning moves but not optimal)
def medium_ai_move():
    # Check if the AI needs to block a winning move
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                board[i][j] = "O"
                if check_win(board, "O")[0]:  # If AI wins, return
                    buttons[i][j].config(text="O")
                    move_sound.play()
                    check_game_over()
                    return
                board[i][j] = "X"  # Try blocking the player
                if check_win(board, "X")[0]:  # If player wins, block
                    board[i][j] = "O"
                    buttons[i][j].config(text="O")
                    move_sound.play()
                    check_game_over()
                    return
                board[i][j] = " "  # No need to block, continue
    easy_ai_move()  # If no immediate block needed, make a random move

# Hard AI (optimal move using Minimax algorithm)
def hard_ai_move():
    # Implementing the Minimax algorithm for the optimal move
    def minimax(board, depth, is_maximizing):
        winner = check_win(board, "O")[0]
        if winner:
            return 1
        winner = check_win(board, "X")[0]
        if winner:
            return -1
        if all(board[i][j] != " " for i in range(3) for j in range(3)):
            return 0
        
        if is_maximizing:
            best = -float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == " ":
                        board[i][j] = "O"
                        best = max(best, minimax(board, depth + 1, False))
                        board[i][j] = " "
            return best
        else:
            best = float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == " ":
                        board[i][j] = "X"
                        best = min(best, minimax(board, depth + 1, True))
                        board[i][j] = " "
            return best

    # Find the best move for the AI
    best_score = -float('inf')
    best_move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == " ":
                board[i][j] = "O"
                score = minimax(board, 0, False)
                board[i][j] = " "
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    
    row, col = best_move
    board[row][col] = "O"
    buttons[row][col].config(text="O")
    move_sound.play()  # Play sound when AI makes a move
    
    # Check for winner or tie
    check_game_over()

# Function to check if the game is over (win or tie)
def check_game_over():
    win_type, win_index = check_win(board, current_player)
    if win_type:
        label.config(text=f"Player {current_player} wins!")
        win_sound.play()
        highlight_win(win_type, win_index)
        update_score(current_player)
        show_restart_button()
        disable_buttons()
        return

    if all(board[i][j] != " " for i in range(3) for j in range(3)):  # Check for tie
        label.config(text="It's a tie!")
        tie_sound.play()
        show_restart_button()
        return

# Function to initialize the game and create buttons
def init_game():
    global root, buttons, label, restart_button, score_label
    root = tk.Tk()
    root.title("Tic-Tac-Toe")

    label = tk.Label(root, text="Player X's turn", font=("Helvetica", 20))
    label.pack(pady=20)

    # Create the board buttons
    board_frame = tk.Frame(root)
    board_frame.pack()

    buttons = [[None for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            buttons[i][j] = tk.Button(board_frame, text=" ", width=10, height=3, font=("Helvetica", 20),
                                      command=lambda i=i, j=j: player_move(i, j))
            buttons[i][j].grid(row=i, column=j)

    restart_button = tk.Button(root, text="Restart", font=("Helvetica", 14), command=restart_game)
    restart_button.pack_forget()  # Hide restart button initially

    score_label = tk.Label(root, text="Player X: 0  |  Player O: 0", font=("Helvetica", 16))
    score_label.pack(pady=10)

    # Show the main menu
    main_menu()

# Main menu for game mode selection
def main_menu():
    global root
    for widget in root.winfo_children():
        widget.destroy()

    main_menu_frame = tk.Frame(root)
    main_menu_frame.pack()

    label = tk.Label(main_menu_frame, text="Welcome to Tic-Tac-Toe", font=("Helvetica", 20))
    label.pack(pady=20)

    ai_button = tk.Button(main_menu_frame, text="Play with AI", width=20, height=2, font=("Helvetica", 14),
                          command=lambda: set_game_mode("AI"))
    ai_button.pack(pady=5)

    two_player_button = tk.Button(main_menu_frame, text="Play with 2-Player", width=20, height=2, font=("Helvetica", 14),
                                  command=lambda: set_game_mode("2-Player"))
    two_player_button.pack(pady=5)

    root.mainloop()

# Start the game
init_game()
