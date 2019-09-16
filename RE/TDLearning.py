import random
import operator
import json
import sys

# Arguments
# 1 Input Trace
# 2 Prev Reward
# 3 Eval (0) or iter (1)
# 4 Previous Eval
# 5 Output to Inter
# 6 Initilize Policy (0) No (1)

class RL:
    def __init__(self, readPolicies = False, driveNum=8, eps=1/(10**3),
                 weights=[1,1]):
        if readPolicies:
            self.readPolicies()
        else:
            self.policyUID = {}
            self.policyPID = {}
        self.driveNum = driveNum 
        self.eps = eps
        self.weights = weights
        self.uidID = 1
        self.pidID = 2
        self.evalID = 6
    
    def evalUID(self, uid):
        if uid not in self.policyUID:
            self.policyUID[uid] = [[1, 1 + (random.random() * self.eps) ]
						   for _ in range(self.driveNum)]
        if random.random() < self.eps:
            policy = random.randrange(self.driveNum)
        else:
            policy = min(enumerate(self.policyUID[uid]), key=operator.itemgetter(1))[0]
        return [policy, self.policyUID[uid][policy][1]]
    
    def evalPID(self, pid):
        if pid not in self.policyPID:
            self.policyPID[pid] = [[1, 1 + (random.random() * self.eps)]
								    for _ in range(self.driveNum)]
        if random.random() < self.eps:
            policy = random.randrange(self.driveNum)
        else:
            policy = min(enumerate(self.policyPID[pid]), key=operator.itemgetter(1))[0]
        return [policy, self.policyPID[pid][policy][1]]
    
    def evalRequest(self, request):
        evalRet  = [self.evalUID(request[self.uidID])]
        evalRet += [self.evalPID(request[self.pidID])]
        evalRet[0][1] =  evalRet[0][1] * self.weights[0]
        evalRet[1][1] = (evalRet[1][1] * self.weights[1]) + evalRet[0][1]
        evalRand = random.random() * evalRet[1][1]
        return [index for index, prob in evalRet if prob >= evalRand][0]
   
    def updateUID(self, uid, policy, reward):
        frequency, cumReward = self.policyUID[uid][policy]
        self.policyUID[uid][policy][1] = ((cumReward * frequency) + reward) / (frequency + 1)
        self.policyUID[uid][policy][0] = frequency + 1
    
    def updatePID(self, pid, policy, reward):
        frequency, cumReward = self.policyPID[pid][policy]
        self.policyPID[pid][policy][1] = ((cumReward * frequency) + reward) / (frequency + 1)
        self.policyPID[pid][policy][0] = frequency + 1
    
    def updatePolicies(self, request, reward):
        self.updateUID(request[self.uidID], int(request[self.evalID]), reward)
        self.updatePID(request[self.pidID], int(request[self.evalID]), reward)
    
    def readPolicies(self):
        self.policyUID = json.load(open('policyUID.json'))
        self.policyPID = json.load(open('policyPID.json'))
    
    def writePolicies(self):
        with open('policyUID.json', 'w', encoding='utf-8') as outfile:
            json.dump(self.policyUID, outfile, ensure_ascii=False)
        with open('policyPID.json', 'w', encoding='utf-8') as outfile:
            json.dump(self.policyPID, outfile, ensure_ascii=False)


if __name__ == "__main__":
	if int(sys.argv[6]):
		learner = RL()
		learner.writePolicies()
	else:
		learner = RL(readPolicies = True)
	
	with open(sys.argv[1], 'r') as inTrace: 
		with open(sys.argv[5], 'w+') as traceOut:
			if int(sys.argv[3]):
				with open(sys.argv[4], 'w+') as prevTrace:
					fLine = inTrace.readline()
					traceOut.write(fLine)
					for request in inTrace:
						request = request.split()
						request += [str(learner.evalRequest(request))]
						prevTrace.write(' '.join(request) + '\n')
						traceOut.write(str(request[0]) + ' ' + str(request[6]) + ' ' +
									   str(request[3]) + ' ' + str(request[4]) + ' ' +
									   str(request[5]) + '\n')
				if int(sys.argv[6]):
					learner.writePolicies()
			else:
				with open(sys.argv[4], 'r') as prevTrace:
					learner = RL(readPolicies = True)
					reward = float(sys.argv[2])
					for request in prevTrace:
						request = request.split()
						learner.updatePolicies(request, reward)
					learner.writePolicies()
			
