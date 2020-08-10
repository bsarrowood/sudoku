# created by:       Brad Arrowood
# created on:       2020.02.17
# last updated:     2020.04.21
# python version:   3.7.6
# run format:       python3 driver.py 00302060090030005001001806400... (and so on)
# file:             driver.py
# addendums:        cls_addendumn.py (contains my class for the script)
# notes:            made for edX ColumbiaX: CSMM.101x - Artificial Intelligence (AI) - week 9, project 4
#                   addendum to driver.py to divide up the class and script, keeping this class separate from the driver.py for ease of use when working on the sudoku solver

# first work with the AC-3 algorithm and if the grid provided needs it, which will most likely be most of the puzzles given, the BTS algorithm will run

# import basics and my class from cls_addendum.py with the class name Puzzle
import argparse
from cls_addendum import Puzzle

def ac_3(grid):
    # func to pull in the values from the grid/Puzzle and place them in a queue to be worked
    queueConstraints = list(grid.constraints)
    while queueConstraints:
        item1, item2 = queueConstraints.pop(0)
        if examine(grid, item1, item2):
            # pulling the func examine to review the values
            if len(grid.domains[item1]) == 0:
                return False
            for item3 in grid.neighbors[item1]:
                if item3 != item1:
                    queueConstraints.append([item3, item1])
    return True

def examine(grid, item1, item2):
    examined = False
    for lat in grid.domains[item1]:
        if not any([grid.constraint(lat, long) for long in grid.domains[item2]]):
            grid.domains[item1].remove(lat)
            examined = True
    return examined

def get_var_0(task, grid):
    # MCV heuristic, picks the cell value which has the fewest options left
    unassigned = [tmp for tmp in grid.variables if tmp not in task]
    # using lambda to sort and return the 
    return min(unassigned, key=lambda var: len(grid.domains[var]))

def backtrack(task, grid):
    # func to use backtrack algorithm
    if len(task) == len(grid.variables):
        return task
    # func to use get_var_0 for using next value and put the returned value into a var
    var = get_var_0(task, grid)
    for value in get_off_neighbor(grid, var):
        if grid.consistent(task, var, value):
            grid.assign(var, value, task)
            result = backtrack(task, grid)
            if result:
                return result
            grid.unassign(var, task)
    return False

def get_off_neighbor(grid, var):
    # LCV heuristic, picks the cell that rules out the fewest options for each of the neighbor var
    if len(grid.domains[var]) == 1:
        return grid.domains[var]
    return sorted(grid.domains[var], key=lambda val: grid.conflicts(grid, var, val))

def main():
    # using argparse to put a name/title to the argument of the cmd line entry of the sudoku puzzle number entry then convert it to a var to be used throughout the script
    parser = argparse.ArgumentParser()
    parser.add_argument('grid')
    arg = parser.parse_args()
    grid = Puzzle(arg.grid)

    if ac_3(grid):
        if grid.success():
        # if the AC3 algorithm solved the puzzle, output using the following
            outputTXT = open("output.txt","a")
            for var in grid.variables:
                outputTXT.write(str(grid.domains[var][0]))
            outputTXT.write(' AC3\n')
            outputTXT.close()
            print('Puzzle Status:    SOLVED\nAlgorithm Used:   AC-3\nWriting to File:  DONE')
        else:
        # if the BTS algorithm solved the puzzle, output using the following
            task = {}
            for lat in grid.variables:
            
                if len(grid.domains[lat]) == 1:
                    task[lat] = grid.domains[lat][0]
            task = backtrack(task, grid)
            for d in grid.domains:
                grid.domains[d] = task[d] if len(d) > 1 else grid.domains[d]

            if task:
                outputTXT = open("output.txt","a")
                for var in grid.variables:
                    outputTXT.write(str(grid.domains[var]))
                outputTXT.write(' BTS\n')
                outputTXT.close()
                print('Puzzle Status:    SOLVED\nAlgorithm Used:   BTS\nWriting to File:  DONE')
            # not adding condition for NO SOLUTION puzzles as the project requirements didn't include requiring this, only that solvable AC3 and BTS puzzles would be tested on my script
            #else:
            #    print("No solution eitem1sts")

if __name__ == '__main__':
    main()
