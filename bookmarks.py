#!/usr/bin/env python3

from os import path, environ
from PyPDF2 import PdfFileMerger, PdfFileReader
import sys
import getopt
import traceback


def add_flat(output, lines, offset):
    for line in lines:
        *head, tail = line.split()
        title = ' '.join(head)
        page = int(tail) + offset
        try:
            output.addBookmark(title, page, None)
        except IndexError:
            print(line)
            traceback.print_exc()
            exit(1)


def add_hier(output, lines, offset):
    marks = {}
    for line in lines:
        try:
            hdr, *tail = line.split()
            hdr = hdr.rstrip('.')
            page = tail.pop()
            title = hdr + ' ' + ' '.join(tail).replace('.', '')
            *head, _ = hdr.split('.')
            parent = marks['.'.join(head)] if len(head) > 0 else None
            page = int(page) + offset
            marks[hdr] = output.addBookmark(title, page, parent)
        except ValueError:
            print(line)
            traceback.print_exc()
            exit(1)


def main(argv):
    struct = 'flat'
    remove = ''
    offset = -1

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

    root = path.join(environ['HOME'], 'pr/data/bkm')

    with open(path.join(root, bkfile)) as f:
        lines = [l.rstrip().replace(remove, '') for l in f.readlines()]

    output = PdfFileMerger()

    with open(path.join(root, infile + '.pdf'), 'rb') as f:
        output.append(PdfFileReader(f), import_bookmarks=False)

    if struct == 'flat':
        add_flat(output, lines, offset)
    else:
        add_hier(output, lines, offset)

    with open(path.join(root, infile + '_bkm.pdf'), 'wb') as outStream:
        output.write(outStream)


if __name__ == '__main__':
    main(sys.argv)
