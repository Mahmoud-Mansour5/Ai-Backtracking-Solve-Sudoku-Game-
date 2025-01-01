import sys
import random
import time
from PyQt5.QtWidgets import (
    QApplication, QWidget, QGridLayout, QLineEdit, QPushButton, QLabel, QVBoxLayout, QMessageBox
)
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QFont, QColor, QPalette

class Sudoku(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.grid = [[0 for _ in range(9)] for _ in range(9)]
        self.solution_grid = [[0 for _ in range(9)] for _ in range(9)]
        self.domains = [[list(range(1, 10)) for _ in range(9)] for _ in range(9)]
        self.difficulty_remove_count = 45  # Default difficulty (medium)
        self.start_time = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.timer_running = False

        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)

        self.grid_layout = QGridLayout()
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                entry = QLineEdit(self)
                entry.setMaxLength(1)
                entry.setFixedSize(40, 40)
                entry.setFont(QFont('Arial', 20))
                entry.setStyleSheet("qproperty-alignment: AlignCenter; background-color: #F0FFF0; border: 1px solid black;")
                entry.textChanged.connect(self.validate_input)
                self.grid_layout.addWidget(entry, i, j)
                self.entries[i][j] = entry

        # Add bold lines to divide the 3x3 subgrids
        for i in range(9):
            for j in range(9):
                if i % 3 == 0 and i != 0:
                    self.grid_layout.setRowMinimumHeight(i, 10)
                if j % 3 == 0 and j != 0:
                    self.grid_layout.setColumnMinimumWidth(j, 10)

        self.vbox.addLayout(self.grid_layout)

        self.buttons_layout = QGridLayout()
        button_style = "font-size: 16px; height: 40px; background-color: #87CEFA; color: white; border: 2px solid black;"

        self.new_game_button = QPushButton("New Game", self)
        self.new_game_button.setStyleSheet(button_style)
        self.new_game_button.clicked.connect(self.start_new_game)
        self.buttons_layout.addWidget(self.new_game_button, 0, 0)

        self.easy_button = QPushButton("Easy", self)
        self.easy_button.setStyleSheet("font-size: 16px; height: 40px; background-color: #32CD32; color: white; border: 2px solid black;")
        self.easy_button.clicked.connect(lambda: self.set_difficulty("easy"))
        self.buttons_layout.addWidget(self.easy_button, 0, 1)

        self.medium_button = QPushButton("Medium", self)
        self.medium_button.setStyleSheet("font-size: 16px; height: 40px; background-color: #FFA500; color: white; border: 2px solid black;")
        self.medium_button.clicked.connect(lambda: self.set_difficulty("medium"))
        self.buttons_layout.addWidget(self.medium_button, 0, 2)

        self.hard_button = QPushButton("Hard", self)
        self.hard_button.setStyleSheet("font-size: 16px; height: 40px; background-color: #FF4500; color: white; border: 2px solid black;")
        self.hard_button.clicked.connect(lambda: self.set_difficulty("hard"))
        self.buttons_layout.addWidget(self.hard_button, 0, 3)

        self.ai_button = QPushButton("AI", self)
        self.ai_button.setStyleSheet(button_style)
        self.ai_button.clicked.connect(self.mode1_ai_step_by_step)
        self.buttons_layout.addWidget(self.ai_button, 1, 0)

        self.user_button = QPushButton("USER", self)
        self.user_button.setStyleSheet("font-size: 16px; height: 40px; background-color: #FFD700; color: black; border: 2px solid black;")
        self.user_button.clicked.connect(self.mode2_user_input_board)
        self.buttons_layout.addWidget(self.user_button, 1, 1)

        self.solve_button = QPushButton("Solve", self)
        self.solve_button.setStyleSheet("font-size: 16px; height: 40px; background-color: #4B0082; color: white; border: 2px solid black;")
        self.solve_button.clicked.connect(self.solve_puzzle)
        self.buttons_layout.addWidget(self.solve_button, 1, 2)

        self.reset_button = QPushButton("Reset Board", self)
        self.reset_button.setStyleSheet("font-size: 16px; height: 40px; background-color: #FF6347; color: white; border: 2px solid black;")
        self.reset_button.clicked.connect(self.reset_board)
        self.buttons_layout.addWidget(self.reset_button, 1, 3)

        self.vbox.addLayout(self.buttons_layout)

        self.timer_label = QLabel("Time: 0:00", self)
        self.timer_label.setFont(QFont('Arial', 14))
        self.vbox.addWidget(self.timer_label)

        self.setWindowTitle("Sudoku")
        self.setGeometry(100, 100, 600, 700)
        self.show()

    def validate_input(self):
        sender = self.sender()
        text = sender.text()
        if text and not (text.isdigit() and 1 <= int(text) <= 9):
            sender.setText('')
        else:
            self.check_user_input()

    def check_user_input(self):
        for i in range(9):
            for j in range(9):
                user_input = self.entries[i][j].text()
                if user_input:
                    if int(user_input) != self.solution_grid[i][j]:
                        self.entries[i][j].setStyleSheet("background-color: #FFCCCC; border: 1px solid black;")
                    else:
                        self.entries[i][j].setStyleSheet("background-color: #F0FFF0; border: 1px solid black;")
        if self.is_board_complete():
            QMessageBox.information(self, "Congratulations!", "You have solved the Sudoku puzzle!")
            self.stop_timer()

    def is_board_complete(self):
        for i in range(9):
            for j in range(9):
                if not self.entries[i][j].text():
                    return False
        return True

    def start_new_game(self):
        self.generate_puzzle()
        self.start_time = time.time()
        self.timer_running = True
        self.timer.start(1000)

    def generate_puzzle(self):
        self.grid = [[(i * 3 + i // 3 + j) % 9 + 1 for j in range(9)] for i in range(9)]
        self.solution_grid = [row[:] for row in self.grid]
        self.solve_with_backtracking()  # Ensure we have a solved grid

        # remove numbers to create a puzzle
        for _ in range(self.difficulty_remove_count):
            x, y = random.randint(0, 8), random.randint(0, 8)
            self.grid[x][y] = 0

        # Initialize domains for arc consistency
        self.initialize_domains()
        self.apply_arc_consistency()

        for i in range(9):
            for j in range(9):
                self.entries[i][j].setText('')
                if self.grid[i][j] != 0:
                    self.entries[i][j].setText(str(self.grid[i][j]))
                    self.entries[i][j].setReadOnly(True)
                    self.entries[i][j].setStyleSheet("font-size: 20px; text-align: center; background-color: #D3D3D3; border: 1px solid black;")
                else:
                    self.entries[i][j].setReadOnly(False)
                    self.entries[i][j].setStyleSheet("font-size: 20px; text-align: center; background-color: #FFFFFF; border: 1px solid black;")

    def solve_puzzle(self):
        for i in range(9):
            for j in range(9):
                user_input = self.entries[i][j].text()
                if user_input:
                    self.grid[i][j] = int(user_input)
                else:
                    self.grid[i][j] = 0

        if not self.is_valid_board():
            QMessageBox.warning(self, "Invalid Board", "There are duplicates or invalid entries on the board.")
            self.stop_timer()
            return

        if self.solve_with_backtracking():
            for i in range(9):
                for j in range(9):
                    self.entries[i][j].setText(str(self.grid[i][j]))
                    self.entries[i][j].setReadOnly(True)
                    self.entries[i][j].setStyleSheet("font-size: 20px; text-align: center; background-color: #D3D3D3; border: 1px solid black;")
            elapsed_time = int(time.time() - self.start_time)
            minutes, seconds = divmod(elapsed_time, 60)
            QMessageBox.information(self, "Solved", f"The Sudoku puzzle has been solved in {minutes:02}:{seconds:02}!")
            self.stop_timer()
        else:
            QMessageBox.warning(self, "Error", "No solution exists for this puzzle.")
            self.stop_timer()

    def solve_with_backtracking(self):
        empty = self.find_empty_cell()
        if not empty:
            return True
        row, col = empty
        for num in self.domains[row][col]:
            if self.is_valid_move(row, col, num):
                self.grid[row][col] = num
                if self.solve_with_backtracking():
                    return True
                self.grid[row][col] = 0
        return False

    def find_empty_cell(self):
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    return i, j
        return None

    def is_valid_move(self, row, col, num):
        if num in self.grid[row]:
            return False
        if num in [self.grid[i][col] for i in range(9)]:
            return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if self.grid[i][j] == num:
                    return False
        return True

    def is_valid_board(self):
        for i in range(9):
            row_seen = set()
            col_seen = set()
            for j in range(9):
                if self.grid[i][j] != 0:
                    if self.grid[i][j] in row_seen:
                        return False
                    row_seen.add(self.grid[i][j])
                if self.grid[j][i] != 0:
                    if self.grid[j][i] in col_seen:
                        return False
                    col_seen.add(self.grid[j][i])
        # Check 3x3 subgrids
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                if not self.is_valid_subgrid(i, j):
                    return False
        return True

    def is_valid_subgrid(self, start_row, start_col):
        subgrid_seen = set()
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if self.grid[i][j] != 0:
                    if self.grid[i][j] in subgrid_seen:
                        return False
                    subgrid_seen.add(self.grid[i][j])
        return True

    def update_timer(self):
        if self.timer_running:
            elapsed_time = int(time.time() - self.start_time)
            minutes, seconds = divmod(elapsed_time, 60)
            self.timer_label.setText(f"Time: {minutes:02}:{seconds:02}")

    def mode1_ai_step_by_step(self):
        self.start_time = time.time()
        self.timer_running = True
        self.timer.start(1000)
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    self.grid[i][j] = (i * 3 + i // 3 + j) % 9 + 1
                    self.entries[i][j].setText(str(self.grid[i][j]))
                    QApplication.processEvents()
                    time.sleep(0.1)
        elapsed_time = int(time.time() - self.start_time)
        minutes, seconds = divmod(elapsed_time, 60)
        QMessageBox.information(self, "AI", f"Sudoku solved step by step in {minutes:02}:{seconds:02}!")
        self.stop_timer()

    def mode2_user_input_board(self):
        self.grid = [[0 for _ in range(9)] for _ in range(9)]
        self.solution_grid = [row[:] for row in self.grid]
        self.solve_with_backtracking()  # Ensure we have a solved grid
        for i in range(9):
            for j in range(9):
                self.entries[i][j].setReadOnly(False)
                self.entries[i][j].setText('')
                self.entries[i][j].setStyleSheet("font-size: 20px; text-align: center; background-color: #FFFFFF; border: 1px solid black;")
        self.start_time = time.time()
        self.timer_running = True
        self.timer.start(1000)

    def set_difficulty(self, difficulty):
        if difficulty == "easy":
            self.difficulty_remove_count = 30
        elif difficulty == "medium":
            self.difficulty_remove_count = 45
        elif difficulty == "hard":
            self.difficulty_remove_count = 60
        QMessageBox.information(self, "Difficulty Changed", f"Difficulty set to {difficulty.capitalize()}")
        self.start_new_game()

    def stop_timer(self):
        self.timer_running = False
        self.timer.stop()
        self.timer_label.setText("Time: 0:00")

    def reset_board(self):
        for i in range(9):
            for j in range(9):
                self.entries[i][j].setReadOnly(False)
                self.entries[i][j].setText('')
                self.entries[i][j].setStyleSheet("font-size: 20px; text-align: center; background-color: #FFFFFF; border: 1px solid black;")
        self.grid = [[0 for _ in range(9)] for _ in range(9)]
        self.solution_grid = [[0 for _ in range(9)] for _ in range(9)]
        self.domains = [[list(range(1, 10)) for _ in range(9)] for _ in range(9)]
        self.stop_timer()

    def initialize_domains(self):
        """Initialize domains for arc consistency."""
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] != 0:
                    self.domains[i][j] = [self.grid[i][j]]
                else:
                    self.domains[i][j] = list(range(1, 10))

    def apply_arc_consistency(self):
        """Apply AC-3 algorithm to ensure arc consistency."""
        queue = [(i, j) for i in range(9) for j in range(9)]
        while queue:
            (row, col) = queue.pop(0)
            if self.revise(row, col):
                if len(self.domains[row][col]) == 0:
                    return False
                for k in range(9):
                    if k != col:
                        queue.append((row, k))
                    if k != row:
                        queue.append((k, col))

        for i in range(9):
            for j in range(9):
                if len(self.domains[i][j]) == 1:
                    self.grid[i][j] = self.domains[i][j][0]
        return True

    def revise(self, row, col):
        """Revise the domain of a variable to ensure consistency."""
        revised = False
        for value in self.domains[row][col][:]:
            if not self.is_consistent(row, col, value):
                self.domains[row][col].remove(value)
                revised = True
        return revised

    def is_consistent(self, row, col, value):
        """Check if a value is consistent with the Sudoku constraints."""
        for k in range(9):
            if k != col and value in self.domains[row][k]:
                return False
            if k != row and value in self.domains[k][col]:
                return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if (i != row or j != col) and value in self.domains[i][j]:
                    return False
        return True


if __name__ == "__main__":
    app = QApplication(sys.argv)
    sudoku = Sudoku()
    sys.exit(app.exec_())
