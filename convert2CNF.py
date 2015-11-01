import sys


def parse_file(filepath):
    # read the layout file to the board array
    board = []
    fin = open(filepath)


    fin.close()
    return board


def convert2CNF(board, output):
    # interpret the number constraints


    fout = open(output, 'w')


    fout.close()


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Layout or output file not specified.'
        exit(-1)
    board = parse_file(sys.argv[1])
    convert2CNF(board, sys.argv[2])