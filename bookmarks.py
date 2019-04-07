#!/usr/bin/env python3

from os import path, environ
from PyPDF2 import PdfFileMerger, PdfFileReader
import sys

bkfile = sys.argv[1]
offset = int(sys.argv[2])
infile = sys.argv[3]
outfile = infile + '_out.pdf'


dir = path.join(environ['HOME'], 'pr/data')
lines = []

with open(path.join(dir, bkfile)) as f:
    lines = [l.rstrip() for l in f.readlines()]

output = PdfFileMerger()
infile = path.join(dir, infile + '.pdf')
print(infile)
with open(infile, 'rb') as f:
    output.append(PdfFileReader(f), import_bookmarks=False)

# output.addPage(input.getPage(0))
for line in lines:
    *head, tail = line.split(' ')
    name = ' '.join(head)
    page = int(tail) + offset
    try:
        output.addBookmark(name, page, parent=None)
    except IndexError:
        print(name, page)
        exit(1)

# output.setPageMode("/UseOutlines")
with open(path.join(dir, outfile), 'wb') as outStream:
    output.write(outStream)


