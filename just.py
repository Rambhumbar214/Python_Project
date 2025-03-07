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
            disable_buttons()
            return
        
        # Check for a tie
        if all(board[i][j] != " " for i in range(3) for j in range(3)):
            label.config(text="It's a tie!")
            tie_sound.play()  # Play sound when it's a tie
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

    def best_move():
        best_val = -float('inf')
        move = (-1, -1)
        for i in range(3):
            for j in range(3):
                if board[i][j] == " ":
                    board[i][j] = "O"
                    move_val = minimax(board, 0, False)
                    board[i][j] = " "
                    if move_val > best_val:
                        best_val = move_val
                        move = (i, j)
        return move

    row, col = best_move()
    board[row][col] = "O"
    buttons[row][col].config(text="O")
    move_sound.play()
    check_game_over()

# Function to check if the game is over (win or tie)
def check_game_over():
    win_type, win_index = check_win(board, "O")
    if win_type:
        label.config(text="AI wins!")
        win_sound.play()
        highlight_win(win_type, win_index)
        disable_buttons()
        return
    win_type, win_index = check_win(board, "X")
    if win_type:
        label.config(text="Player wins!")
        win_sound.play()
        highlight_win(win_type, win_index)
        disable_buttons()
        return
    if all(board[i][j] != " " for i in range(3) for j in range(3)):
        label.config(text="It's a tie!")
        tie_sound.play()
        return

# Function to set the game difficulty
def set_difficulty(level):
    global difficulty
    difficulty = level
    start_game()

# Function to set the game mode (AI or 2-Player)
def set_game_mode(mode):
    global game_mode
    game_mode = mode
    if game_mode == "AI":
        show_level_menu()
    else:
        start_game()

# Function to show the level menu (after selecting AI)
def show_level_menu():
    # Hide main menu
    main_menu_frame.pack_forget()

    # Show level menu frame
    level_menu_frame = tk.Frame(root, bg="lightblue")
    level_menu_frame.pack(expand=True)

    level_label = tk.Label(level_menu_frame, text="Select Difficulty", font=("Helvetica", 24), bg="lightblue")
    level_label.pack(pady=20)

    easy_button = tk.Button(level_menu_frame, text="Easy", width=20, height=2, font=("Helvetica", 14),
                            command=lambda: set_difficulty("Easy"))
    easy_button.pack(pady=5)

    medium_button = tk.Button(level_menu_frame, text="Medium", width=20, height=2, font=("Helvetica", 14),
                              command=lambda: set_difficulty("Medium"))
    medium_button.pack(pady=5)

    hard_button = tk.Button(level_menu_frame, text="Hard", width=20, height=2, font=("Helvetica", 14),
                            command=lambda: set_difficulty("Hard"))
    hard_button.pack(pady=5)

# Function to initialize the game interface
def init_game():
    global current_player, board, buttons, label, start_button, restart_button, main_menu_frame
    global root  # Make root global
    root = tk.Tk()  # Initialize the root window
    current_player = "X"
    board = [[" " for _ in range(3)] for _ in range(3)]
    buttons = [[None for _ in range(3)] for _ in range(3)]

    # Create the main window
    root.title("Tic Tac Toe")
    root.configure(bg="lightblue")

    # Main Menu Frame
    main_menu_frame = tk.Frame(root, bg="lightblue")
    main_menu_frame.pack(expand=True)

    welcome_label = tk.Label(main_menu_frame, text="Welcome to Tic Tac Toe!", font=("Helvetica", 24), bg="lightblue")
    welcome_label.pack(pady=20)

    # Mode selection (AI or 2-Player)
    ai_button = tk.Button(main_menu_frame, text="Play with AI", width=20, height=2, font=("Helvetica", 14),
                          command=lambda: set_game_mode("AI"))
    ai_button.pack(pady=5)

    two_player_button = tk.Button(main_menu_frame, text="2-Player Game", width=20, height=2, font=("Helvetica", 14),
                                  command=lambda: set_game_mode("2-Player"))
    two_player_button.pack(pady=5)

    root.mainloop()

# Function to start a new game
def start_game():
    global current_player, board, buttons, label, start_button, restart_button, main_menu_frame
    # Hide level menu and show the game board
    main_menu_frame.pack_forget()

    # Create a new frame for the game
    game_frame = tk.Frame(root, bg="lightblue")
    game_frame.pack(expand=True)

    # Create a label to show the current player
    label = tk.Label(game_frame, text="Player X's turn", font=("Helvetica", 20), bg="lightblue")
    label.grid(row=0, column=0, columnspan=3)

    # Create the buttons for the grid
    for i in range(3):
        for j in range(3):
            buttons[i][j] = tk.Button(game_frame, text=" ", width=10, height=3, font=("Helvetica", 24, "bold"),
                                      state="normal", bg="lightgray", command=lambda row=i, col=j: player_move(row, col))
            buttons[i][j].grid(row=i+1, column=j, padx=5, pady=5)

# Start the game
if __name__ == "__main__":
    init_game()
