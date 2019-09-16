
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  6 14:44:29 2018

@author: Snigdha
"""

# -*- coding: utf-8 -*-

import os
import sys

#Arguments 
# 1 Home Folder
# 2 File to Parse
# 3 Output file name

home = sys.argv[1] + '\\'
fileOut = sys.argv[3]
maxMerge = 256

with open(fileOut, 'w+') as ioM:
    bMax = 0
    sMax = 0
    for fileIn in list(os.walk(home))[0][2]:
        with open(home+fileIn, 'r') as ioF:
            for line in ioF:
                data = line.split(' ')
                data = [data[x] for x in range(6)]
                bMax = max(bMax, int(data[3]))
                sMax = max(sMax, int(data[4]))
            
    ioM.write('8 ' + str(2 * (bMax + sMax)) + '\n')
    
    for fileIn in list(os.walk(home))[0][2]:
        with open(home+fileIn, 'r') as ioF:
            curr = None
            for line in ioF:
                data = line.split(' ')
                data = [data[x] for x in range(6)]
                
                for i in (0, 3, 4):
                    data[i] = int(data[i])
                    
                if curr == None: 
                    curr = data
                else:
                    match = True
                    for i in (1,2,5):
                        if curr[i] != data[i]:
                            match = False
                            break
                    if match and data[3] != curr[3] + curr[4]:
                        match = False
                    if curr[4] >= maxMerge:
                        match = False
                    
                    if match:
                        curr[4] += data[4]
                    else:
                        for i in (0, 3, 4):
                            curr[i] = str(curr[i])
                        ioM.write(' '.join(curr) + '\n')
                        curr = data