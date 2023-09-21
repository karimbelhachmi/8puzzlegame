import search
import random
import math

class EightPuzzleState:
    """
    The Eight Puzzle is described in the course textbook on
    page 64.

    This class defines the mechanics of the puzzle itself.  The
    task of recasting this puzzle as a search problem is left to
    the EightPuzzleSearchProblem class.
    """

    def __init__( self, numbers ):
        """
          Constructs a new eight puzzle from an ordering of numbers.

        numbers: a list of integers from 0 to 8 representing an
          instance of the eight puzzle.  0 represents the blank
          space.  Thus, the list

            [1, 0, 2, 3, 4, 5, 6, 7, 8]

          represents the eight puzzle:
            -------------
            | 1 |   | 2 |
            -------------
            | 3 | 4 | 5 |
            -------------
            | 6 | 7 | 8 |
            ------------

        The configuration of the puzzle is stored in a 2-dimensional
        list (a list of lists) 'cells'.
        """
        self.cells = []
        numbers = numbers[:] # Make a copy so as not to cause side-effects.
        numbers.reverse()
        for row in range( 3 ):
            self.cells.append( [] )
            for col in range( 3 ):
                self.cells[row].append( numbers.pop() )
                if self.cells[row][col] == 0:
                    self.blankLocation = row, col

    def isGoal( self ):
        """
          Checks to see if the puzzle is in its goal state.

            -------------
            |   | 1 | 2 |
            -------------
            | 3 | 4 | 5 |
            -------------
            | 6 | 7 | 8 |
            -------------

        >>> EightPuzzleState([0, 1, 2, 3, 4, 5, 6, 7, 8]).isGoal()
        True

        >>> EightPuzzleState([1, 0, 2, 3, 4, 5, 6, 7, 8]).isGoal()
        False
        """
        current = 0
        for row in range( 3 ):
            for col in range( 3 ):
                if current != self.cells[row][col]:
                    return False
                current += 1
        return True

    def legalMoves( self ):
        """
          Returns a list of legal moves from the current state.

        Moves consist of moving the blank space up, down, left or right.
        These are encoded as 'up', 'down', 'left' and 'right' respectively.

        >>> EightPuzzleState([0, 1, 2, 3, 4, 5, 6, 7, 8]).legalMoves()
        ['down', 'right']
        """
        moves = []
        row, col = self.blankLocation
        if(row != 0):
            moves.append('up')
        if(row != 2):
            moves.append('down')
        if(col != 0):
            moves.append('left')
        if(col != 2):
            moves.append('right')
        return moves

    def result(self, move):
        """
          Returns a new eightPuzzle with the current state and blankLocation
        updated based on the provided move.

        The move should be a string drawn from a list returned by legalMoves.
        Illegal moves will raise an exception, which may be an array bounds
        exception.

        NOTE: This function *does not* change the current object.  Instead,
        it returns a new object.
        """
        row, col = self.blankLocation
        if(move == 'up'):
            newrow = row - 1
            newcol = col
        elif(move == 'down'):
            newrow = row + 1
            newcol = col
        elif(move == 'left'):
            newrow = row
            newcol = col - 1
        elif(move == 'right'):
            newrow = row
            newcol = col + 1
        else:
            raise "Illegal Move"

        # Create a copy of the current eightPuzzle
        newPuzzle = EightPuzzleState([0, 0, 0, 0, 0, 0, 0, 0, 0])
        newPuzzle.cells = [values[:] for values in self.cells]
        # And update it to reflect the move
        newPuzzle.cells[row][col] = self.cells[newrow][newcol]
        newPuzzle.cells[newrow][newcol] = self.cells[row][col]
        newPuzzle.blankLocation = newrow, newcol

        return newPuzzle

    # Utilities for comparison and display
    def __eq__(self, other):
        """
            Overloads '==' such that two eightPuzzles with the same configuration
          are equal.

          >>> EightPuzzleState([0, 1, 2, 3, 4, 5, 6, 7, 8]) == \
              EightPuzzleState([1, 0, 2, 3, 4, 5, 6, 7, 8]).result('left')
          True
        """
        for row in range( 3 ):
            if self.cells[row] != other.cells[row]:
                return False
        return True

    def __hash__(self):
        return hash(str(self.cells))

    def __getAsciiString(self):
        """
          Returns a display string for the maze
        """
        lines = []
        horizontalLine = ('-' * (13))
        lines.append(horizontalLine)
        for row in self.cells:
            rowLine = '|'
            for col in row:
                if col == 0:
                    col = ' '
                rowLine = rowLine + ' ' + col.__str__() + ' |'
            lines.append(rowLine)
            lines.append(horizontalLine)
        return '\n'.join(lines)

    def __str__(self):
        return self.__getAsciiString()

class EightPuzzleSearchProblem(search.SearchProblem):
    def __init__(self, puzzle):
        self.puzzle = puzzle

    def getStartState(self):
        return self.puzzle

    def isGoalState(self, state):
        return state.isGoal()

    def getSuccessors(self, state):
        succ = []
        for a in state.legalMoves():
            succ.append((state.result(a), a, 1))
        return succ

    def getCostOfActions(self, actions):
        return len(actions)

    # Heuristic Functions
    def h1(self, state, problem=None):
        # Number of misplaced tiles
        goal = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
        misplaced = sum([1 for i in range(3) for j in range(3) if state.cells[i][j] != goal[i][j] and state.cells[i][j] != 0])
        return misplaced

    def h2(self, state, problem=None):
        # Sum of Euclidean distances of the tiles from their goal positions
        goal_positions = {(i * 3 + j): (i, j) for i in range(3) for j in range(3)}
        distance = 0
        for i in range(3):
            for j in range(3):
                if state.cells[i][j] != 0:
                    x_goal, y_goal = goal_positions[state.cells[i][j]]
                    distance += math.sqrt((i - x_goal)**2 + (j - y_goal)**2)
        return distance

    def h3(self, state, problem=None):
        # Sum of Manhattan distances of the tiles from their goal positions
        goal_positions = {(i * 3 + j): (i, j) for i in range(3) for j in range(3)}
        distance = 0
        for i in range(3):
            for j in range(3):
                if state.cells[i][j] != 0:
                    x_goal, y_goal = goal_positions[state.cells[i][j]]
                    distance += abs(i - x_goal) + abs(j - y_goal)
        return distance

    def h4(self, state, problem=None):
        # Number of tiles out of row + Number of tiles out of column
        goal_positions = {(i * 3 + j): (i, j) for i in range(3) for j in range(3)}
        out_of_row = sum([1 for i in range(3) for j in range(3) if state.cells[i][j] != 0 and i != goal_positions[state.cells[i][j]][0]])
        out_of_col = sum([1 for i in range(3) for j in range(3) if state.cells[i][j] != 0 and j != goal_positions[state.cells[i][j]][1]])
        return out_of_row + out_of_col

EIGHT_PUZZLE_DATA = [[1, 0, 2, 3, 4, 5, 6, 7, 8],
                     [1, 7, 8, 2, 3, 4, 5, 6, 0],
                     [4, 3, 2, 7, 0, 5, 1, 6, 8],
                     [5, 1, 3, 4, 0, 2, 6, 7, 8],
                     [1, 2, 5, 7, 6, 8, 0, 4, 3],
                     [0, 3, 1, 6, 8, 2, 7, 5, 4]]

def loadEightPuzzle(puzzleNumber):
    return EightPuzzleState(EIGHT_PUZZLE_DATA[puzzleNumber])

def createRandomEightPuzzle(moves=100):
    puzzle = EightPuzzleState([0,1,2,3,4,5,6,7,8])
    for i in range(moves):
        puzzle = puzzle.result(random.sample(puzzle.legalMoves(), 1)[0])
    return puzzle

HEURISTIC_DESCRIPTIONS = {
    'h1': 'Number of misplaced tiles',
    'h2': 'Sum of Euclidean distances of the tiles from their goal positions',
    'h3': 'Sum of Manhattan distances of the tiles from their goal positions',
    'h4': 'Number of tiles out of row + Number of tiles out of column'
}

def choose_heuristic():
    print("Please choose a heuristic:")
    for key, desc in HEURISTIC_DESCRIPTIONS.items():
        print(f"{key}: {desc}")
    choice = input("Enter your choice (e.g., h1, h2, ...): ")
    while choice not in HEURISTIC_DESCRIPTIONS:
        print("Invalid choice. Please choose again.")
        choice = input("Enter your choice (e.g., h1, h2, ...): ")
    return choice

if __name__ == '__main__':
    puzzle = createRandomEightPuzzle(25)
    print('A random puzzle:')
    print(puzzle)

    problem = EightPuzzleSearchProblem(puzzle)
    
    heuristic_choice = choose_heuristic()
    heuristic_function = getattr(problem, heuristic_choice)
    path = search.aStarSearch(problem, heuristic=heuristic_function)
    
    heuristic_description = HEURISTIC_DESCRIPTIONS.get(heuristic_choice, "this heuristic")

    print('A* found a path of %d moves using %s: %s' % (len(path), heuristic_description, str(path)))
    curr = puzzle
    i = 1
    for a in path:
        curr = curr.result(a)
        print('After %d move%s: %s' % (i, ("", "s")[i>1], a))
        print(curr)
        input("Press return for the next state..")   # Waiting for the user to press Enter
        i += 1
