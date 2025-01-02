CSP to solve Sudoku
1 Game Description
Sudoku is a logic-based number-placement game that challenges players to fill a 9x9 grid with
digits from 1 to 9. The objective is to complete the grid in such a way that each row, each
column, and each of the nine 3x3 subgrids (also known as regions or boxes) contains all of the
digits from 1 to 9 without repetition.
2 Requirements
2.1 Game GUI
• Mode 1: You are required to provide a full game with GUI to show the AI agent solving
the game.
• Mode 2 : game with GUI which allow user to input board representation then agent solves
it
2.2 Algorithms
You are required to support Backtracking to be able to validate the input(to check that input
puzzle is solvable) , Backtracking is also needed to generate random puzzle (fill random places
of puzzle) to ensure that the puzzle generated is solvable.
2.3 Arc Consistency
You are required to SHOW Arc consistency for Solution
• Represent Sudoku as a CSP: Variables: Each cell in the Sudoku grid is a variable. Domains: The domain of each variable represents the possible numbers (1 to 9) that can be
placed in the cell. Constraints: The Sudoku rules, which state that no number can be
repeated in a row, column, or 3x3 subgrid.
• Define Arcs: An arc in Sudoku represents a binary constraint between two variables
(cells). Arc consistency is applied to all pairs of connected variables.
For each row, create arcs between all pairs of cells in that row. For each column, create
arcs between all pairs of cells in that column. For each 3x3 subgrid, create arcs between
all pairs of cells in that subgrid.
• Initial Domain Reduction: Before applying arc consistency, initialize the domains of each
variable based on the initial puzzle.
For each pre-filled cell, remove all other values from its domain. For each empty cell,
initialize its domain to [1, 2, 3, 4, 5, 6, 7, 8, 9].
• Apply Arc Consistency: Iteratively enforce arc consistency on all arcs until no further
changes can be made:
For each arc (Xi, Xj): Revise: For each value in the domain of Xi, check if there is a
consistent value in the domain of Xj. If inconsistent: Remove the inconsistent value from
the domain of Xi. Repeat for all arcs: Continue revising all arcs until no further changes
can be made.
• Update Sudoku Grid: After applying arc consistency, update the Sudoku grid based on
the reduced domains:
For each cell with a singleton domain (a domain with only one value), assign that value
to the cell.

•  game was interactive(make user fill board and check if input
correct or violate constraints for each number) and working correctly.
