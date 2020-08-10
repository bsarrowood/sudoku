# created by:      Brad Arrowood
# last updated:	   2019.12.02
# file:		   cls_addendum.py [addendum to driver.py]
# notes:	   made for edX ColumbiaX: CSMM.101x - Artificial Intelligence (AI) - week 9, project 4
# 		   addendum to driver.py to divide up the class and script, keeping this class separate from the driver.py for ease of use when working on the sudoku solver

# importing basics
import sys

# making the grid into a battleship-style grid to more easily navigate/manage
ROWS = 'ABCDEFGHI'
COLUMNS = '123456789'

class Puzzle:
    def __init__(self, board):
        # setting up multiple
        self.variables, self.domains, self.constraints, self.neighbors, self.pruned = list(), dict(), list(), dict(), dict()
        # then pulling in func create
        self.create(board)

    def create(self, board):
        # creating/combining and then setting var to make the grid
        puzzlegrid = list(board)
        self.variables = self.combine(ROWS, COLUMNS)
        self.domains = {v: list(range(1, 10)) if puzzlegrid[i] == '0'
            else [int(puzzlegrid[i])] for i, v in enumerate(self.variables)}
        self.pruned = {v: list() if puzzlegrid[i] == '0'
            else [int(puzzlegrid[i])] for i, v in enumerate(self.variables)}
        # pulling the func build_cstr and 
        self.build_cstr()
        self.build_nbr()

    def build_cstr(self):
        blocks = (
            # setting the block chunks with the values to nav
            [self.combine(ROWS, number) for number in COLUMNS] +
            [self.combine(char, COLUMNS) for char in ROWS] +
            [self.combine(char, number) for char in ('ABC', 'DEF', 'GHI') for number in ('123', '456', '789')]
        )
        for block in blocks:
            # the blocks within the grid
            combos = self.alter(block)
            for combo in combos:
                if [combo[0], combo[1]] not in self.constraints:
                    self.constraints.append([combo[0], combo[1]])

    def build_nbr(self):
        # putting/piecing together the neighbor variables
        for xx1 in self.variables:
            self.neighbors[xx1] = list()
            for cc1 in self.constraints:
                if xx1 == cc1[0]:
                    self.neighbors[xx1].append(cc1[1])

    def consistent(self, assignment, var, value):
        consistent = True
        for key, val in assignment.items():
            if val == value and key in self.neighbors[var]:
                consistent = False
        return consistent

    def assign(self, var, value, assignment):
        assignment[var] = value
        self.forward_check(var, value, assignment)

    def unassign(self, var, assignment):
        if var in assignment:
            for (D, var3) in self.pruned[var]:
                self.domains[D].append(var3)
            self.pruned[var] = []
            del assignment[var]

    def forward_check(self, var, value, assignment):
        for nbr in self.neighbors[var]:
            if nbr not in assignment:
                if value in self.domains[nbr]:
                    self.domains[nbr].remove(value)
                    self.pruned[var].append((nbr, value))

    # needing to call on the staticmethod to run a check, 1/3
    @staticmethod
    def constraint(lat2, long2): return lat2 != long2

    # needing to call on the staticmethod to run a check, 2/3
    @staticmethod
    def combine(alpha, beta): return [aa1 + bb1 for aa1 in alpha for bb1 in beta]

    # needing to call on the staticmethod to run a check, 3/3
    @staticmethod
    def alter(override):
		# needing to import these tools too
        import itertools
        results = list()
        for Ll2 in range(0, len(override) + 1):
            if Ll2 == 2:
                for subset in itertools.permutations(override, Ll2):
                    results.append(subset)

        return results

    # needing to call on the classmethod just once now
    @staticmethod
    def conflicts(sudoku, var, val):
        count = 0
        for n in sudoku.neighbors[var]:
            if len(sudoku.domains[n]) > 1 and val in sudoku.domains[n]:
                count += 1
        return count

    def out(self, mode):
        if mode == 'console':
            for var in self.variables:
                sys.stdout.write(str(self.domains[var][0]))
        elif mode == 'file':
            return

    def success(self):
        # used in driver.py under the main() > ac_3() to help announce grid was solved followed by determine by with algorithm
        for var2 in self.variables:
            if len(self.domains[var2]) > 1:
                return False
        return True

    #def complete(self, assignment):
    #    for x in self.variables:
    #        if len(self.domains[x]) > 1 and x not in assignment:
    #            return False
    #   return True
