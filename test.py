from tkinter import *
from tkinter import messagebox
import random
import time


class Sudoku:
    def _init_(self, master):
        self.master = master
        master.title("Sudoku")

        self.grid = [[0 for _ in range(9)] for _ in range(9)]
        self.original_grid = [[0 for _ in range(9)] for _ in range(9)]
        self.difficulty_remove_count = 45  # Default difficulty (medium)
        self.start_time = None  # To track the start time of the game
        self.create_widgets()
        self.generate_puzzle()

    def create_widgets(self):
        # Frame for the grid
        self.board_frame = Frame(self.master, bg="#F2F2F2")
        self.board_frame.grid(row=0, column=0, padx=10, pady=10)

        self.entries = [[None for _ in range(9)] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                entry = Entry(
                    self.board_frame,
                    width=3,
                    font=('Arial', 20),
                    justify='center',
                    bg="#E6E6FA",
                    fg="#333333",
                    relief=SOLID,
                    bd=1,
                )
                entry.grid(row=i, column=j, padx=2, pady=2)
                self.entries[i][j] = entry
                entry.bind("<FocusOut>", self.validate_input)

        # Expand rows and columns
        for i in range(9):
            self.board_frame.grid_rowconfigure(i, weight=1)
            self.board_frame.grid_columnconfigure(i, weight=1)

        # Options Frame for buttons
        self.options_frame = Frame(self.master, bg="#F2F2F2")
        self.options_frame.grid(row=1, column=0, pady=10)

        # Game buttons
        self.new_game_button = Button(
            self.options_frame,
            text="New Game",
            command=self.start_new_game,
            bg="#87CEFA",
            fg="white",
            font=('Arial', 12, 'bold'),
            relief=RAISED,
            bd=3,
        )
        self.new_game_button.pack(side=LEFT, padx=10)

        self.hardness_label = Label(
            self.options_frame,
            text="Hardness:",
            bg="#F2F2F2",
            fg="#333333",
            font=('Arial', 12, 'bold'),
        )
        self.hardness_label.pack(side=LEFT, padx=10)

        self.easy_button = Button(
            self.options_frame,
            text="Easy",
            command=lambda: self.set_difficulty("easy"),
            bg="#32CD32",
            fg="white",
            font=('Arial', 12, 'bold'),
            relief=RAISED,
            bd=3,
        )
        self.easy_button.pack(side=LEFT, padx=5)

        self.medium_button = Button(
            self.options_frame,
            text="Medium",
            command=lambda: self.set_difficulty("medium"),
            bg="#FFA500",
            fg="white",
            font=('Arial', 12, 'bold'),
            relief=RAISED,
            bd=3,
        )
        self.medium_button.pack(side=LEFT, padx=5)

        self.hard_button = Button(
            self.options_frame,
            text="Hard",
            command=lambda: self.set_difficulty("hard"),
            bg="#FF4500",
            fg="white",
            font=('Arial', 12, 'bold'),
            relief=RAISED,
            bd=3,
        )
        self.hard_button.pack(side=LEFT, padx=5)

        # Game modes buttons
        self.mode1_button = Button(
            self.master,
            text="Mode 1",
            command=self.mode1_ai_step_by_step,
            bg="#1E90FF",
            fg="white",
            font=('Arial', 12, 'bold'),
            relief=RAISED,
            bd=3,
        )
        self.mode1_button.grid(row=2, column=0, sticky="nsew", pady=5)

        self.mode2_button = Button(
            self.master,
            text="Mode 2",
            command=self.mode2_user_input_board,
            bg="#FFD700",
            fg="black",
            font=('Arial', 12, 'bold'),
            relief=RAISED,
            bd=3,
        )
        self.mode2_button.grid(row=3, column=0, sticky="nsew", pady=5)

        self.solve_button = Button(
            self.master,
            text="Solve",
            command=self.solve_puzzle,
            bg="#4B0082",
            fg="white",
            font=('Arial', 12, 'bold'),
            relief=RAISED,
            bd=3,
        )
        self.solve_button.grid(row=4, column=0, sticky="nsew", pady=10)

        # Timer label to show elapsed time
        self.timer_label = Label(
            self.master,
            text="Time: 0:00",
            font=('Arial', 14, 'bold'),
            fg="#333333",
            bg="#F2F2F2"
        )
        self.timer_label.grid(row=5, column=0, pady=10)

        self.timer_running = False

    def start_new_game(self):
        """Start a new Sudoku game."""
        self.generate_puzzle()
        self.start_time = time.time()  # Start the timer
        self.timer_running = True
        self.update_timer()

    def validate_input(self, event):
        """Validate the user's input to ensure it's a digit between 1 and 9 and check for duplicates."""
        widget = event.widget
        value = widget.get()

        # Check if value is valid (between 1 and 9)
        if not value.isdigit() or not (1 <= int(value) <= 9):
            widget.delete(0, END)
            return

        # Get the row and column of the current widget
        row = widget.grid_info()['row']
        col = widget.grid_info()['column']

        # Check for duplicates in row
        for j in range(9):
            if j != col and self.entries[row][j].get() == value:
                messagebox.showwarning("Duplicate Entry", "This number already exists in the row.")
                widget.delete(0, END)
                self.stop_timer()  # Stop timer when alert comes up
                return

        # Check for duplicates in column
        for i in range(9):
            if i != row and self.entries[i][col].get() == value:
                messagebox.showwarning("Duplicate Entry", "This number already exists in the column.")
                widget.delete(0, END)
                self.stop_timer()  # Stop timer when alert comes up
                return

    def generate_puzzle(self):
        """Generate a new Sudoku puzzle."""
        self.grid = [[(i * 3 + i // 3 + j) % 9 + 1 for j in range(9)] for i in range(9)]
        for _ in range(self.difficulty_remove_count):
            x, y = random.randint(0, 8), random.randint(0, 8)
            self.grid[x][y] = 0

        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, END)
                if self.grid[i][j] != 0:
                    self.entries[i][j].insert(0, str(self.grid[i][j]))
                    self.entries[i][j].config(state='disabled')
                else:
                    self.entries[i][j].config(state='normal')

    def solve_puzzle(self):
        """Solve the current Sudoku puzzle based on user input in Mode 2."""
        for i in range(9):
            for j in range(9):
                user_input = self.entries[i][j].get()
                if user_input:
                    self.grid[i][j] = int(user_input)
                else:
                    self.grid[i][j] = 0

        # Validate the puzzle before solving
        if not self.is_valid_board():
            messagebox.showwarning("Invalid Board", "There are duplicates or invalid entries on the board.")
            self.stop_timer()  # Stop timer when alert comes up
            return

        # Solve the puzzle using a backtracking algorithm
        if self.solve_with_backtracking():
            for i in range(9):
                for j in range(9):
                    self.entries[i][j].delete(0, END)
                    self.entries[i][j].insert(0, str(self.grid[i][j]))
                    self.entries[i][j].config(state='disabled')
            elapsed_time = int(time.time() - self.start_time)
            minutes, seconds = divmod(elapsed_time, 60)
            messagebox.showinfo("Solved", f"The Sudoku puzzle has been solved in {minutes:02}:{seconds:02}!")
            self.stop_timer()  # Stop timer when alert comes up
        else:
            messagebox.showinfo("Error", "No solution exists for this puzzle.")
            self.stop_timer()  # Stop timer when alert comes up

    def solve_with_backtracking(self):
        """Solve the Sudoku puzzle using the backtracking algorithm."""
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    for num in range(1, 10):
                        if self.is_valid_move(i, j, num):
                            self.grid[i][j] = num
                            if self.solve_with_backtracking():
                                return True
                            self.grid[i][j] = 0
                    return False
        return True

    def is_valid_move(self, row, col, num):
        """Check if placing num in (row, col) is valid."""
        # Check the row
        if num in self.grid[row]:
            return False
        # Check the column
        if num in [self.grid[i][col] for i in range(9)]:
            return False
        # Check the 3x3 grid
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if self.grid[i][j] == num:
                    return False
        return True

    def is_valid_board(self):
        """Check if the current board has any duplicate entries."""
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] != 0:
                    # Check row and column for duplicates
                    for k in range(9):
                        if k != j and self.grid[i][k] == self.grid[i][j]:
                            return False
                        if k != i and self.grid[k][j] == self.grid[i][j]:
                            return False
        return True

    def update_timer(self):
        """Update the timer label with the elapsed time."""
        if self.timer_running:
            elapsed_time = int(time.time() - self.start_time)
            minutes, seconds = divmod(elapsed_time, 60)
            self.timer_label.config(text=f"Time: {minutes:02}:{seconds:02}")
            self.master.after(1000, self.update_timer)

    def mode1_ai_step_by_step(self):
        """Solve step by step (simplified example)."""
        self.start_time = time.time()  # Start timer when Mode 1 is clicked
        self.timer_running = True
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    self.grid[i][j] = (i * 3 + i // 3 + j) % 9 + 1
                    self.entries[i][j].delete(0, END)
                    self.entries[i][j].insert(0, str(self.grid[i][j]))
                    self.entries[i][j].update()
                    time.sleep(0.1)

        # Calculate elapsed time
        elapsed_time = int(time.time() - self.start_time)
        minutes, seconds = divmod(elapsed_time, 60)
        # Show the solved alert with elapsed time
        messagebox.showinfo("AI Mode 1", f"Sudoku solved step by step in {minutes:02}:{seconds:02}!")

        self.stop_timer()  # Stop timer when alert comes up

    def mode2_user_input_board(self):
        """Allow user to input their own board."""
        self.grid = [[0 for _ in range(9)] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                self.entries[i][j].config(state='normal')
                self.entries[i][j].delete(0, END)
        self.start_time = time.time()  # Start timer when Mode 2 is clicked
        self.timer_running = True

    def set_difficulty(self, difficulty):
        """Set the difficulty level."""
        if difficulty == "easy":
            self.difficulty_remove_count = 30
        elif difficulty == "medium":
            self.difficulty_remove_count = 45
        elif difficulty == "hard":
            self.difficulty_remove_count = 60
        messagebox.showinfo("Difficulty Changed", f"Difficulty set to {difficulty.capitalize()}")
        self.start_new_game()

    def stop_timer(self):
        """Stop the timer."""
        self.timer_running = False
        self.timer_label.config(text="Time: 0:00")


if __name__ == "__main__":
    root = Tk()
    root.geometry("600x700")
    sudoku_game = Sudoku(root)
    root.mainloop()