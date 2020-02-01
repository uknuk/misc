#!/usr/bin/env python3

from os import path, environ
from PyPDF2 import PdfFileMerger, PdfFileReader
import sys
import getopt
import traceback
import argparse
import re

ROOT = path.join(environ['HOME'], 'pr/data/bkm')
PREFIXES = ["Chapter", "Appendix"]


def print_exc(line):
    exc_type, exc_value, exc_traceback = sys.exc_info()
    print(exc_type.__name__, ':', exc_value)
    print('line: ', line)


def flat(output, lines, offset):
    for line in lines:
        *head, tail = line.split()
        title = ' '.join(head)
        page = int(tail) + offset
        try:
            output.addBookmark(title, page, None)
        except (IndexError, ValueError):
            print_exc(line)
            continue


def hier(output, lines, offset):
    marks = {}
    for line in lines:
        try:
            hdr, *tail = line.split()
            if hdr in PREFIXES:
                hdr, *tail = tail

            if '.' not in hdr:
                continue

            hdr = hdr.rstrip('.')
            page = tail.pop()
            title = hdr + ' ' + ' '.join(tail).replace('.', '')
            *head, _ = hdr.split('.')
            parent = marks['.'.join(head)] if len(head) > 0 else None
            page = int(page) + offset
            print(title, page, parent)
            marks[hdr] = output.addBookmark(title, page, parent)
        except (IndexError, ValueError, KeyError):
            print_exc(line)
            continue


def seq(output, lines, offset):
    titles = []
    pages = []
    for line in lines:
        if re.fullmatch(r'\d*', line):
            pages.append(line)
        else:
            titles.append(line)


    for num, title in enumerate(titles):
        page = int(pages[num]) + offset
        print(title, page)
        output.addBookmark(title, page, None)


def main(args):
    bookmarks = args.bookmarks if args.bookmarks else args.input
    with open(path.join(ROOT, bookmarks + '_bkm')) as f:
        lines = [l.rstrip() for l in f.readlines()]

    output = PdfFileMerger()

    with open(path.join(ROOT, args.input + '.pdf'), 'rb') as f:
        reader = PdfFileReader(f)
        # print(reader.trailer["/Root"]["/PageLabels"])
        output.append(reader, import_bookmarks=False)

    globals()[args.fun](output, lines, args.offset)

    with open(path.join(ROOT, args.input + '_bkm.pdf'), 'wb') as outStream:
        output.write(outStream)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('fun')
    parser.add_argument('-b', '--bookmarks')
    parser.add_argument('-o', '--offset', type=int, default=0)

    main(parser.parse_args())
