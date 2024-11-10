import sudoku.sudoku_error as skr 

class Sudoku:
    """
    Class representing a sudoku game board. 

    Attributes: 
        matrixOrder (int): The sudoku matrix order
        regionMatrixOrder (int): The sudoku region matrix order. 
        maxCellValue (int) : The maximum cell value.  
    """
    def __init__(self, matrixOrder, regionMatrixOrder, maxCellValue): 
        """
        Initializes the sudoku matrix data

        Args: 
            matrixOrder (int): the sudoku matrix order.
            regionMatrixOrder (int): the region matrix order, should be a divisor of M.
            maxCellValue (int): the maximum cell value, should be greater than the matrix order. 
        """
        if matrixOrder % regionMatrixOrder != 0:
            raise skr.SudokuError("initialization error: the matrix order"
                                  "should be a multiple of the region matrix order."
                                  f"matrixOrder={matrixOrder}\n"
                                  f"regionMatrixOrder={regionMatrixOrder}\n", 
                                  code="INITIALIZATION_ERROR")
        
        if maxCellValue < matrixOrder: 
            raise skr.SudokuError("initialization error: the max cell value should be greater or "
                                  "equal to the matrix order",
                                  f"matrixOrder={matrixOrder}\n"
                                  f"regionMatrixOrder={regionMatrixOrder}",
                                  code="INITIALIZATION_ERROR")
        
        self.matrixOrder = matrixOrder
        self.regionMatrixOrder = regionMatrixOrder
        self.maxCellValue = maxCellValue

        # sets containing values in each lines
        self.lines = [set()] * matrixOrder 
        # sets containing values in each columns
        self.columns = [set()] * matrixOrder 
        # sets containing values in each regions
        self.regions = [set()] * (matrixOrder // regionMatrixOrder) 
        

