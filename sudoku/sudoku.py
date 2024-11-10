import sudoku.sudoku_error as skr 

class Sudoku:
    """
    Class representing a sudoku game board. 

    Attributes: 
         matrix_order (int): The sudoku matrix order
        region_matrix_order (int): The sudoku region matrix order. 
        max_cell_value (int) : The maximum cell value.  
        lines (list<set>): sets containing values in each lines
        columns (list<set>): sets containing values in each columns
        regions (list<set>): sets containing values in each regions
    """
    def __init__(self, matrix_order, region_matrix_order, max_cell_value): 
        """
        Initializes the sudoku matrix data

        Args: 
            matrix_order (int): the sudoku matrix order.
            region_matrix_order (int): the region matrix order, should be a divisor of M.
            max_cell_value (int): the maximum cell value, should be greater than the matrix order. 
        """
        if matrix_order % region_matrix_order != 0:
            raise skr.SudokuError("initialization error: the matrix order"
                                  "should be a multiple of the region matrix order."
                                  f"matrix_order={matrix_order}\n"
                                  f"region_matrix_order={region_matrix_order}\n", 
                                  code="SKR_INITIALIZATION")
        
        if max_cell_value < matrix_order: 
            raise skr.SudokuError("initialization error: the max cell value should be greater or "
                                  "equal to the matrix order",
                                  f"matrix_order={matrix_order}\n"
                                  f"region_matrix_order={region_matrix_order}",
                                  code="SKR_INITIALIZATION")
        
        self.matrix_order = matrix_order
        self.region_matrix_order = region_matrix_order
        self.max_cell_value = max_cell_value

        # sets containing values in each lines
        self.lines = [set()] * matrix_order 
        # sets containing values in each columns
        self.columns = [set()] * matrix_order 
        # sets containing values in each regions
        self.regions = [set()] * (matrix_order // region_matrix_order) 

        # initialize the game matrix
        self.M = {}
        for i in range(matrix_order):
            for j in range(matrix_order):
                self.M[(i,j)] = 0
        
        self.omega = set(range(1,1+self.max_cell_value))
    
    def play(self, i, j, value):
        """
        Make a game move, e.q: put a value into a cell
        i (int): 0 based line index, should be lower than the matrix order
        j (int): 0 based column index, should be lower than the matrix order
        value (int): the value of the sudoku should be btw [1...max_cell_value]
        """ 
        if i >= self.matrix_order:
            raise skr.SudokuError(f"Can't play at line {i} (>= ${self.matrix_order})",
                                  code="SKR_PLAY")
        if j >= self.matrix_order:
            raise skr.SudokuError(f"Can't play at column {j} (>= ${self.matrix_order})",
                                  code="SKR_PLAY")
        
        if value not in self.omega: 
            raise skr.SudokuError(f"can't play: invalid value {value} for cell ({i},{j}). "
                                  f"not in {self.omega}",
                                  code="SKR_PLAY")
        
        if self.M[(i,j)] != 0: 
            raise skr.SudokuError(f"can't play: "
                                  f"({i}, {j}) have already a value ({self.M[(i,j)]})")
        
        self.M[(i,j)] = value
        self.lines[i].add(value)
        self.columns[j].add(value)
        rg_index = self.region_index(i, j) 
        self.regions[rg_index].add(value)

    def available_moves(self): 
        """
        Return the availables moves
        """
        moves = []
        for value, move in self.M:
            if value == 0:
                moves += move
        return moves 
    

    def region_index(self, i, j):
        """
        Return the index of the region containing the cell (i,j)
        i (int): cell line
        j (int): cell column
        """
        if i >= self.matrix_order or j >= self.matrix_order:
            raise skr.SudokuError(f"can't compute region index "
                                  f"({i}, {j}) is out of range")

        rg_line = i // self.region_matrix_order
        rg_column = j // self.region_matrix_order

        return rg_line * self.matrix_order + rg_column


    def cell_possibilities(self, i, j): 
        """
        Return the available possibilities for the cell (i,j)
        i (int): the cell line
        j (int): the cell column
        """
        if i >= self.matrix_order or j >= self.matrix_order:
            raise skr.SudokuError(f" can't get possibilities : "
                                  f"({i}, {j}) is out of range")
        
        column_poss = self.omega.difference(
            self.columns[i]
        )
        lines_poss = self.omega.difference(
            self.lines[i]
        )
        region_poss = self.omega.difference(
            self.regions[self.region_index(i, j)]
        )

        return lines_poss.intersection(
            column_poss
        ).intersection(
            region_poss
        )