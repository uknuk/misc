#!/usr/bin/env python3

from os import path, environ
from PyPDF2 import PdfFileMerger, PdfFileReader
import sys
import getopt
import traceback
import argparse
import re
import roman

ROOT = path.join(environ['HOME'], 'elib/bkm')


def print_exc(line):
    exc_type, exc_value, exc_traceback = sys.exc_info()
    print(exc_type.__name__, ':', exc_value)
    print('line: ', line)

def parse(line, args):
    *head, tail = line.split()
    try:
        page = int(tail) + args.offset
    except ValueError:
        try:
            tail = tail.rstrip()
            if tail.isupper():
                print (f"Skipping {line} because of non-nummerical {tail}")
                page = None
            else:
                page = roman.fromRoman(tail.upper()) + args.roman_offset
        except:
            print(f"Skipping {line} because of non-nummerical {tail}")
            page = None

    return head,page


def flat(output, lines, args):
    for line in lines:
        # *head, tail = line.split()
        head, page = parse(line, args)
        if not page:
            continue

        title = ' '.join(head)
        try:
            output.addBookmark(title, page, None)
        except (IndexError, ValueError):
            print_exc(line)
            continue


def hier(output, lines, args):
    # hierarchical with numbers
    marks = {}
    for line in lines:
        try:
            head, page = parse(line, args)
            if not page:
                continue

            index = head[0]
            if not '.' in head:
                parent = None
            else:
                head = [item for item in head if item != '.']
                if '.' in index:
                    *pref, _ = index.split('.')
                    parent = marks['.'.join(pref)]
                else:
                    try:
                        int(index)
                        parent = None
                    except ValueError:
                        print(f'Skipping {index}')

            title = ' '.join(head)
            marks[index] = output.addBookmark(title, page, parent)
        except (IndexError, ValueError, KeyError):
            print_exc(line)
            continue


def auto(output, lines, args):
    # auto hierarchical
    for line in lines:
        hdr, page = parse(line, args);

        if not '.' in hdr:
            if hdr:
                parent = output.addBookmark(hdr.pop(), page, None)
            else:
                print(f"Skipping {line}")  # content page number
        else:
            title = ' '.join([item for item in hdr if item != '.'])
            output.addBookmark(title, page, parent)


def seq(output, lines, args):
    titles = []
    pages = []
    for line in lines:
        if re.fullmatch(r'\d*', line):
            pages.append(line)
        else:
            titles.append(line)


    for num, title in enumerate(titles):
        page = int(pages[num]) + args.offset
        print(title, page)
        output.addBookmark(title, page, None)


def main(args):
    with open(path.join(ROOT, "in", args.input + '.txt')) as f:
        lines = [l.rstrip() for l in f.readlines()]

    output = PdfFileMerger()
    pdf_file = args.input + '.pdf'

    with open(path.join(ROOT, "in", pdf_file), 'rb') as f:
        reader = PdfFileReader(f)
        output.append(reader, import_bookmarks=False)

    globals()[args.fun](output, lines, args)

    with open(path.join(ROOT, "out", pdf_file), 'wb') as outStream:
        output.write(outStream)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input')
    parser.add_argument('fun')
    parser.add_argument('offset', type = int)
    parser.add_argument('-r', '--roman_offset', type=int, default=0)

    main(parser.parse_args())
