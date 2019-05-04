#!/usr/bin/env python3

from os import path, environ
from PyPDF2 import PdfFileMerger, PdfFileReader
import sys
import getopt


def add_flat(output, lines, offset):

    for line in lines:
        *head, tail = line.split()
        name = ' '.join(head)
        page = int(tail) + offset
        try:
            output.addBookmark(name, page, parent=None)
        except IndexError:
            print(name, page)
            exit(1)


def add_hier(output, lines, offset):
    parent = None
    for line in lines:
        hdr, *tail = line.split()
        page = tail.pop()
        title = ' '.join(tail).replace('.', '')
        page = int(page) + offset
        print(hdr, title, page)


if __name__ == '__main__':

    struct = 'flat'
    remove = ''
    offset = 0

    opts, args = getopt.getopt(sys.argv[1:], 'b:i:o:s:r:')
    for opt, val in opts:
        if opt == '-b':
            bkfile = val

        if opt == '-i':
            infile = val

        if opt == '-o':
            offset = int(val)

        if opt == '-s':
            struct = val

        if opt == '-r':
            remove = val

    dir = path.join(environ['HOME'], 'pr/data')
    # lines = []

    with open(path.join(dir, bkfile)) as f:
        lines = [l.rstrip().replace(remove, '') for l in f.readlines()]

    output = PdfFileMerger()

    with open(path.join(dir, infile + '.pdf'), 'rb') as f:
        output.append(PdfFileReader(f), import_bookmarks=False)

    if struct == 'flat':
        add_flat(output, lines, offset)
    else:
        add_hier(output, lines, offset)

# output.addPage(input.getPage(0))

# output.setPageMode("/UseOutlines")
    with open(path.join(dir, infile + '_out.pdf'), 'wb') as outStream:
        output.write(outStream)


