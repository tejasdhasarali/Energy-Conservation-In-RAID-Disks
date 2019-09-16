#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  6 15:40:44 2018

@author: tejashasarali
"""

# -*- coding: utf-8 -*-

import os
import sys

intr = (1, 2, 4, 5, 6, 7)
bIntr = ((0, 5*10**13),(3, 5*10**6))

ds = [{} for _ in range(max(intr)+1)]
home = sys.argv[1] + '\\'

for file in list(os.walk(home))[0][2]:
    print(file)
    
    with open(home+file) as ioF:
        for line in ioF:
            data = line.split(' ')
            
            for i in intr:
                if data[i] in ds[i]:
                    ds[i][data[i]] += 1
                else:
                    ds[i][data[i]]  = 1
                    
            for i, s in bIntr:
                tmp = str((int(data[i])//s)*s) + '-' + str(((int(data[i]))//s)*s+s-1)
                if tmp in ds[i]:
                    ds[i][tmp] += 1
                else:
                    ds[i][tmp]  = 1

print()

for dCat in ds:
    sCat = [(dKey, dCat[dKey]) for dKey in sorted(list(dCat.keys()))]
    print(sCat)
    print()
