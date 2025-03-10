import tkinter as tk
from itertools import cycle
from tkinter import font, messagebox
from typing import NamedTuple
import pygame  # Import the pygame module for sound

# Initialize the pygame mixer for sound
pygame.mixer.init()

# Load sounds
move_sound = pygame.mixer.Sound("shoot_sound.wav")  # Make sure you have a 'shoot_sound.wav' file
win_sound = pygame.mixer.Sound("hit_sound.wav")  # Make sure you have a 'hit_sound.wav' file
tie_sound = pygame.mixer.Sound("game_over.wav")  # Make sure you have a 'game_over.wav' file
background_music = "background.mp3"  # Make sure you have a 'background_music.mp3' file for background music

# Player and Move classes remain the same
class Player(NamedTuple):
    label: str
    color: str

class Move(NamedTuple):
    row: int
    col: int
    label: str = ""

BOARD_SIZE = 3
DEFAULT_PLAYERS = (
    Player(label="X", color="blue"),
    Player(label="O", color="green"),
)

class TicTacToeGame:
    def __init__(self, players=DEFAULT_PLAYERS, board_size=BOARD_SIZE):
        self._players = cycle(players)
        self.board_size = board_size
        self.current_player = next(self._players)
        self.winner_combo = []
        self._current_moves = []
        self._has_winner = False
        self._winning_combos = []
        self._setup_board()

    def _setup_board(self):
        self._current_moves = [
            [Move(row, col) for col in range(self.board_size)]
            for row in range(self.board_size)
        ]
        self._winning_combos = self._get_winning_combos()

    def _get_winning_combos(self):
        rows = [
            [(move.row, move.col) for move in row]
            for row in self._current_moves
        ]
        columns = [list(col) for col in zip(*rows)]
        first_diagonal = [row[i] for i, row in enumerate(rows)]
        second_diagonal = [col[j] for j, col in enumerate(reversed(columns))]
        return rows + columns + [first_diagonal, second_diagonal]

    def check_winner(self):
        for combo in self._winning_combos:
            values = [self._current_moves[row][col].label for row, col in combo]
            if values == [self.current_player.label] * self.board_size:
                self.winner_combo = combo
                self._has_winner = True
                return True
        return False

    def check_tie(self):
        for row in self._current_moves:
            for move in row:
                if move.label == "":
                    return False
        return True

class TicTacToeBoard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tic-Tac-Toe Game")
        self._cells = {}
        self.game = None
        self._create_menu_bar()
        self.show_start_page()

    def _create_menu_bar(self):
        menu_bar = tk.Menu(self)
        self.config(menu=menu_bar)

        game_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Game", menu=game_menu)
        game_menu.add_command(label="Start New Game", command=self.start_game)
        game_menu.add_command(label="Exit", command=self.quit)

    def show_start_page(self):
        # Create a frame for the start page with a message and a button to start the game
        frame = tk.Frame(self)
        frame.pack(pady=50)

        title = tk.Label(frame, text="Tic-Tac-Toe Game", font=font.Font(size=24, weight="bold"))
        title.pack(pady=20)

        start_button = tk.Button(frame, text="Start Game", font=font.Font(size=16), command=self.start_game)
        start_button.pack(pady=10)

    def start_game(self):
        self.game = TicTacToeGame()  # Default to 2-player mode
        self.show_game_board()
        pygame.mixer.music.load(background_music)  # Load the background music
        pygame.mixer.music.play(-1)  # Play background music in a loop

    def show_game_board(self):
        # Remove the start page
        for widget in self.winfo_children():
            widget.destroy()

        self._create_board_display()
        self._create_board_grid()

    def _create_board_display(self):
        display_frame = tk.Frame(master=self)
        display_frame.pack(fill=tk.X)
        self.display = tk.Label(
            master=display_frame,
            text="Ready?",
            font=font.Font(size=28, weight="bold"),
        )
        self.display.pack()

    def _create_board_grid(self):
        grid_frame = tk.Frame(master=self)
        grid_frame.pack()
        for row in range(3):
            self.rowconfigure(row, weight=1, minsize=50)
            self.columnconfigure(row, weight=1, minsize=75)
            for col in range(3):
                button = tk.Button(
                    master=grid_frame,
                    text="",
                    font=font.Font(size=36, weight="bold"),
                    fg="black",
                    width=3,
                    height=2,
                    highlightbackground="lightblue",
                    command=lambda r=row, c=col: self.on_cell_click(r, c),
                )
                self._cells[button] = (row, col)
                button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

    def on_cell_click(self, row, col):
        if self.game._current_moves[row][col].label != "":
            return  # Cell already occupied
        self.game._current_moves[row][col] = Move(row, col, self.game.current_player.label)
        button = self.get_button_by_coordinates(row, col)
        button.config(text=self.game.current_player.label, fg=self.game.current_player.color)

        move_sound.play()  # Play move sound

        if self.game.check_winner():
            self.display.config(text=f"Player {self.game.current_player.label} wins!")
            for button in self.get_buttons_by_combo(self.game.winner_combo):
                button.config(bg="yellow")
            win_sound.play()
            self.after(2000, self.restart_game)
        elif self.game.check_tie():
            self.display.config(text="It's a tie!")
            tie_sound.play()
            self.after(2000, self.restart_game)
        else:
            # Switch player turn
            self.game.current_player = next(self.game._players)
            self.display.config(text=f"Player {self.game.current_player.label}'s turn")

    def get_button_by_coordinates(self, row, col):
        for button, (r, c) in self._cells.items():
            if r == row and c == col:
                return button
        return None

    def get_buttons_by_combo(self, combo):
        buttons = []
        for row, col in combo:
            buttons.append(self.get_button_by_coordinates(row, col))
        return buttons

    def restart_game(self):
        for button in self._cells.keys():
            button.config(text="", bg="lightblue")
        self.game = TicTacToeGame()
        self.display.config(text="Ready?")
        pygame.mixer.music.load(background_music)  # Restart the background music after game reset
        pygame.mixer.music.play(-1)  # Play background music in a loop

def main():
    """Create the game's board and run its main loop."""
    board = TicTacToeBoard()
    board.mainloop()

if __name__ == "__main__":
    main()
