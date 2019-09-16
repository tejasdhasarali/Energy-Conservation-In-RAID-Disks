
import subprocess
import random
import sys
import shutil

HARDMAXCAPACITY=3303094400


diskBlocks={} #disk=[currentWritingBlock,MaxCapacity]
CURRENTBLOCK=0
MAXCAPACITY=1

command="" #Output
idToBlockDict={} #id=[disk,block,no of blocks]

REQUESTTIME=0
DISK=1
ID=2
BLOCK=2
NOOFBLOCKS=3
TASK=4


DATA=66

READ='R'
WRITE='W'

# Arguments
# 1 Input trace file
# 2 Output trace file
# 3 Retfile
# 4 Enable stat parse

fOut=open(sys.argv[2],'w+')
stack = []

with open(sys.argv[1], 'r') as fIn:
    firstLine = fIn.readline().split()
    for i in range(0,int(firstLine[0])):
        diskBlocks[str(i)]=[0,int(firstLine[1])]
    for line in fIn:
        lineList=line.rstrip().split()
        while(len(stack) and int(stack[0][0])<int(lineList[REQUESTTIME])):
            fOut.write(' '.join(stack.pop(0)))
   
        if lineList[TASK]=='R':
            if lineList[ID] not in idToBlockDict:
                disk=str(random.choice(range(1,len(diskBlocks))))
               
                idToBlockDict[lineList[ID]]=[0, disk,
                                            diskBlocks[disk][CURRENTBLOCK], 0,
                                            lineList[NOOFBLOCKS]] #ADD THE LOCATION OF FILE
               
                diskBlocks[disk][CURRENTBLOCK]+=int(lineList[NOOFBLOCKS]) #INCREMENT THE DISK BLOCK
   
            if idToBlockDict[lineList[ID]][DISK]!=lineList[DISK]: #MOVING THE FILE BETWEEN DISKS
 
                fOut.write(lineList[REQUESTTIME]+' '
                           +str(idToBlockDict[lineList[ID]][DISK])+' '
                           +str(idToBlockDict[lineList[ID]][BLOCK])+' '
                           +str(idToBlockDict[lineList[ID]][NOOFBLOCKS])+' '
                           +READ+'\n')  #READ FROM THE DISK
           
                diskBlocks[idToBlockDict[lineList[ID]][DISK]][MAXCAPACITY]+=int(idToBlockDict[lineList[ID]][NOOFBLOCKS]) #INCREASE MAX CAPACITY
 
                if((diskBlocks[lineList[DISK]][CURRENTBLOCK]+int(lineList[NOOFBLOCKS]))<HARDMAXCAPACITY):
                   
                    stack.append([str(int(lineList[REQUESTTIME])+100),
                               lineList[DISK],
                               str(diskBlocks[lineList[DISK]][CURRENTBLOCK]),
                               lineList[NOOFBLOCKS],
                               WRITE,
                                '\n'])  #Add to stack
 
 
                idToBlockDict[lineList[ID]]=[0, lineList[DISK],
                                             diskBlocks[lineList[DISK]][CURRENTBLOCK], 0,
                                             lineList[NOOFBLOCKS]] #UPDATE THE LOCATION OF FILE
 
                diskBlocks[lineList[DISK]][CURRENTBLOCK]+=int(lineList[NOOFBLOCKS]) #INCREMENT WRITING BLOCK
 
 
            else:     #JUST READ
                fOut.write(lineList[REQUESTTIME]+' '
                           +str(idToBlockDict[lineList[ID]][DISK])+' '
                           +str(idToBlockDict[lineList[ID]][BLOCK])+' '
                           +str(idToBlockDict[lineList[ID]][NOOFBLOCKS])+' '
                           +READ+'\n')  #READ FROM THE DISK
                   
   
        elif lineList[TASK]=='W':
            if((diskBlocks[lineList[DISK]][CURRENTBLOCK]+int(lineList[NOOFBLOCKS]))<HARDMAXCAPACITY):          
                fOut.write(lineList[REQUESTTIME]+' '
                                   +lineList[DISK]+' '
                                   +str(diskBlocks[lineList[DISK]][CURRENTBLOCK])+' '
                                   +lineList[NOOFBLOCKS]+' '
                                   +WRITE+'\n')  #WRITE TO THE DISK
           
            if lineList[ID] in idToBlockDict:
                diskBlocks[idToBlockDict[lineList[ID]][DISK]][MAXCAPACITY]+=int(lineList[NOOFBLOCKS])  #INCREASE MAX CAPACITY
           
            idToBlockDict[lineList[ID]]=[0, lineList[DISK],
                                         diskBlocks[lineList[DISK]][CURRENTBLOCK], 0, 
                                         lineList[NOOFBLOCKS]] #UPDATE THE ID
           
            diskBlocks[lineList[DISK]][CURRENTBLOCK]+=int(lineList[NOOFBLOCKS]) #UPDATE THE WRITING BLOCK
       
               
    while(len(stack)):
            fOut.write(' '.join(stack.pop(0)))          
           
fOut.close()

if int(sys.argv[4]):
	fReturn=open(sys.argv[3],'w')
	fReturn.write('Virtual disk write stats\n')
	with open(sys.argv[1]) as fIn:
		firstLine = fIn.readline().split()
		for i in range(1,int(firstLine[1])+1):
			if(diskBlocks[str(i)][CURRENTBLOCK]):
				percent=(diskBlocks[str(i)][CURRENTBLOCK]/int(firstLine[2]))*100
			else:
				percent=0
			fReturn.write('disk'+','+str(i)+','+str(percent)+'\n')

	fReturn.write('Actual disk write stats\n')
	for i in diskBlocks:
		if(i[CURRENTBLOCK]):
			percent=(diskBlocks[str(i)][CURRENTBLOCK]/HARDMAXCAPACITY)*100
		else:
			percent=0
		fReturn.write('disk'+','+str(i)+','+str(percent)+'\n')
	fReturn.close()

	

if shutil.which("disksim"):
	subprocess.run("disksim parms.1B stdout " + sys.argv[2] + " 0" +
				   " \"disk1 .. disk"+str(len(diskBlocks))
				   +"\" "+"\"Segment size (inblks)\" 64 " + 
				   "\"disk*\" \"Scheduler:Scheduling policy\" 4")
else:
	print("DiskSim not found on system")
