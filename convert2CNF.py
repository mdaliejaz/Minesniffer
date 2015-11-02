import sys
from itertools import product, combinations

height = 0
width = 0
num_vars = 0


def parse_file(filepath):
    # read the layout file to the board array
    fin = open(filepath)
    h, w = (int(t) for t in fin.readline().split())
    global height, width, num_vars
    height = h
    width = w
    board = [[None for col in range(width)] for row in range(height)]
    for i in xrange(height):
        tokens = fin.readline().strip().split(',')
        for j in xrange(width):
            if tokens[j] == 'X':
                num_vars += 1
                board[i][j] = -num_vars
            else:
                board[i][j] = int(tokens[j])
    fin.close()
    return board


def find_neighbor_mines(board, row, col):
    neighbor_mines = []
    for i in [-1, 0, 1]:
        for j in [1, 0, -1]:
            if 0 <= row - i < height and 0 <= col - j < width:
                if board[row - i][col - j] < 0:
                    neighbor_mines.append(-1 * board[row - i][col - j])
    return neighbor_mines


def tseitin_transform(cnf, no_of_vars):
    # Convert a disjunction of conjunctions to a conjunction of disjunctions
    # by introducing a new Z_i variable to represent each conjunction
    tseitin_no_of_vars = 0
    for i, clause in enumerate(cnf):
        tseitin_no_of_vars = no_of_vars + i
        # Transform 'conjunction implies Z' to CNF
        yield frozenset([tseitin_no_of_vars] + [-v for v in clause])
        # Transform 'Z implies conjunction' to CNF
        for var in clause:
            yield frozenset([-tseitin_no_of_vars, var])
    # Transform disjunction of conjunctions to disjunction of Zs in CNF
    yield frozenset(xrange(no_of_vars, tseitin_no_of_vars + 1))


def convert2CNF(board, output):
    # interpret the number constraints
    fout = open(output, 'w')
    no_of_clauses = set()
    global num_vars
    for row in xrange(height):
        for col in xrange(width):
            if board[row][col] >= 0:
                no_of_mines = board[row][col]
                no_of_vars = find_neighbor_mines(board, row, col)
                cnf = []
                for mines in combinations(no_of_vars, no_of_mines):
                    non_mines = tuple(-var for var in no_of_vars if var not in mines)
                    cnf.append(mines + non_mines)
                if len(no_of_vars) > 2 and 0 < no_of_mines < len(no_of_vars):
                    no_of_clauses.update(tseitin_transform(cnf, num_vars + 1))
                    num_vars += len(cnf)
                else:
                    no_of_clauses.update(frozenset(c) for c in product(*cnf))

    fout.write('p cnf %d %d\n' % (num_vars, len(no_of_clauses)))
    for clause in no_of_clauses:
        fout.write(' '.join(str(v) for v in clause) + ' 0\n')
    fout.close()


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Layout or output file not specified.'
        exit(-1)
    board = parse_file(sys.argv[1])
    convert2CNF(board, sys.argv[2])
