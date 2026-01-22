#!/usr/bin/env python

import os
import re
from sys import argv

dir = argv[1]
old = re.compile(argv[2])
new = argv[3]

if len(argv) == 4:
    do = False
else:
    do = True
    
for root, dirs, names in os.walk(dir):
    if len(names) > 0:
        for name in names:
            if old.search(name) != None:
                new_name = os.path.join(root, re.sub(old, new, name))
                print(new_name)
                if do is True:
                    os.rename(os.path.join(root, name), new_name)
 
