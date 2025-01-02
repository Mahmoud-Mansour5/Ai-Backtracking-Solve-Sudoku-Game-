import sys
import random
import time
from PyQt5.QtWidgets import (
    QApplication, QWidget, QGridLayout, QLineEdit, QPushButton, QLabel, QVBoxLayout, QMessageBox
)
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QFont
from queue import Queue

class Sudoku(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Initializing Sudoku grids and timer
        self.grid = [[0 for _ in range(9)] for _ in range(9)]
        self.solution_grid = [[0 for _ in range(9)] for _ in range(9)]
        self.domains = [[list(range(1, 10)) for _ in range(9)] for _ in range(9)]
        self.difficulty_remove_count = 45  # Default difficulty (medium)
        self.start_time = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.timer_running = False

        # Creating main layout
        self.vbox = QVBoxLayout()
        self.setLayout(self.vbox)

        # Creating Sudoku grid
        self.grid_layout = QGridLayout()
        self.entries = [[None for _ in range(9)] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                entry = QLineEdit(self)
                entry.setMaxLength(1)
                entry.setFixedSize(40, 40)
                entry.setFont(QFont('Arial', 20))
                entry.setStyleSheet(
                    "qproperty-alignment: AlignCenter; background-color: #F0FFF0; border: 1px solid black;"
                )
                entry.textChanged.connect(self.validate_input)
                self.grid_layout.addWidget(entry, i, j)
                self.entries[i][j] = entry

        self.vbox.addLayout(self.grid_layout)

        # Buttons for controls
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

        self.solve_button = QPushButton("Solve", self)
        self.solve_button.setStyleSheet("font-size: 16px; height: 40px; background-color: #4B0082; color: white; border: 2px solid black;")
        self.solve_button.clicked.connect(self.provide_hint)
        self.buttons_layout.addWidget(self.solve_button, 1, 0)

        self.reset_button = QPushButton("Reset", self)
        self.reset_button.setStyleSheet("font-size: 16px; height: 40px; background-color: #FF6347; color: white; border: 2px solid black;")
        self.reset_button.clicked.connect(self.reset_board)
        self.buttons_layout.addWidget(self.reset_button, 1, 1)

        self.ai_button = QPushButton("AI", self)
        self.ai_button.setStyleSheet(button_style)
        self.ai_button.clicked.connect(self.solve_puzzle)
        self.buttons_layout.addWidget(self.ai_button, 1, 2)

        self.user_button = QPushButton("USER", self)
        self.user_button.setStyleSheet(button_style)
        self.user_button.clicked.connect(self.user_mode)
        self.buttons_layout.addWidget(self.user_button, 1, 3)

        self.vbox.addLayout(self.buttons_layout)

        # Timer label
        self.timer_label = QLabel("Time: 0:00", self)
        self.timer_label.setFont(QFont('Arial', 14))
        self.vbox.addWidget(self.timer_label)

        # Window settings
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
                if user_input and int(user_input) != self.solution_grid[i][j]:
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
        self.grid = [[0 for _ in range(9)] for _ in range(9)]
        self.solution_grid = [[0 for _ in range(9)] for _ in range(9)]
        self.fill_grid()
        self.solution_grid = [row[:] for row in self.grid]
        self.remove_numbers_from_grid()
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

    def fill_grid(self):
        numbers = list(range(1, 10))
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    random.shuffle(numbers)
                    for number in numbers:
                        if self.is_valid_move(i, j, number):
                            self.grid[i][j] = number
                            if self.find_empty_cell() is None or self.fill_grid():
                                return True
                            self.grid[i][j] = 0
                    return False

    def remove_numbers_from_grid(self):
        attempts = self.difficulty_remove_count
        while attempts > 0:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            while self.grid[row][col] == 0:
                row = random.randint(0, 8)
                col = random.randint(0, 8)
            backup = self.grid[row][col]
            self.grid[row][col] = 0
            copy_grid = [row[:] for row in self.grid]
            if not self.has_unique_solution(copy_grid):
                self.grid[row][col] = backup
            attempts -= 1

    def has_unique_solution(self, grid):
        count = 0

        def solve(grid):
            nonlocal count
            empty = self.find_empty_cell(grid)
            if not empty:
                count += 1
                return
            row, col = empty
            for num in range(1, 10):
                if self.is_valid_move(row, col, num, grid):
                    grid[row][col] = num
                    solve(grid)
                    grid[row][col] = 0
                    if count > 1:
                        return

        solve(grid)
        return count == 1

    def find_empty_cell(self, grid=None):
        if grid is None:
            grid = self.grid
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    return i, j
        return None

    def is_valid_move(self, row, col, num, grid=None):
        if grid is None:
            grid = self.grid
        if num in grid[row]:
            return False
        if num in [grid[i][col] for i in range(9)]:
            return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if grid[i][j] == num:
                    return False
        return True

    def solve_puzzle(self):
        self.ac3()
        for i in range(9):
            for j in range(9):
                user_input = self.entries[i][j].text()
                if not user_input:
                    self.entries[i][j].setText(str(self.solution_grid[i][j]))

    def provide_hint(self):
        empty_cells = [(i, j) for i in range(9) for j in range(9) if not self.entries[i][j].text()]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.entries[i][j].setText(str(self.solution_grid[i][j]))
            self.entries[i][j].setStyleSheet("background-color: #FFFF99; border: 1px solid black;")
        self.check_user_input()

    def reset_board(self):
        for i in range(9):
            for j in range(9):
                self.entries[i][j].setText('')
                self.entries[i][j].setReadOnly(False)
                self.entries[i][j].setStyleSheet("font-size: 20px; text-align: center; background-color: #FFFFFF; border: 1px solid black;")

    def set_difficulty(self, level):
        if level == "easy":
            self.difficulty_remove_count = 30
        elif level == "medium":
            self.difficulty_remove_count = 45
        elif level == "hard":
            self.difficulty_remove_count = 60
        QMessageBox.information(self, "Difficulty", f"Difficulty set to {level.capitalize()}")

    def stop_timer(self):
        self.timer.stop()
        self.timer_running = False

    def update_timer(self):
        elapsed = int(time.time() - self.start_time)
        minutes = elapsed // 60
        seconds = elapsed % 60
        self.timer_label.setText(f"Time: {minutes}:{seconds:02d}")

    def user_mode(self):
        # Placeholder function to indicate user mode is active
        QMessageBox.information(self, "User Mode", "You are now in USER mode. Solve the puzzle manually.")

    def ac3(self):
        queue = Queue()
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    for k in range(9):
                        if k != j:
                            queue.put(((i, j), (i, k)))
                        if k != i:
                            queue.put(((i, j), (k, j)))
                    start_row, start_col = 3 * (i // 3), 3 * (j // 3)
                    for row in range(start_row, start_row + 3):
                        for col in range(start_col, start_col + 3):
                            if (row, col) != (i, j):
                                queue.put(((i, j), (row, col)))

        while not queue.empty():
            (xi, xj), (yi, yj) = queue.get()
            if self.revise(xi, xj, yi, yj):
                if len(self.domains[xi][xj]) == 0:
                    return False
                for k in range(9):
                    if k != xj:
                        queue.put(((xi, xj), (xi, k)))
                    if k != xi:
                        queue.put(((xi, xj), (k, xj)))
                start_row, start_col = 3 * (xi // 3), 3 * (xj // 3)
                for row in range(start_row, start_row + 3):
                    for col in range(start_col, start_col + 3):
                        if (row, col) != (xi, xj):
                            queue.put(((xi, xj), (row, col)))
        return True

    def revise(self, xi, xj, yi, yj):
        revised = False
        for x in self.domains[xi][xj][:]:
            if not any(self.is_valid_move(xi, xj, x) for y in self.domains[yi][yj]):
                self.domains[xi][xj].remove(x)
                revised = True
        return revised

if __name__ == '__main__':
    app = QApplication(sys.argv)
    sudoku = Sudoku()
    sys.exit(app.exec_())
