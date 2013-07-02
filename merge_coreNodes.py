import sys

def read_kplexOut(kplex_out):
	read=0
	cores=[]
	peripherals=[]
	allCores=set()
	allPeripherals=set()
	for line in kplex_out:
		if line.startswith('-----'):
			read=0
		elif line.startswith('Cores:'):
			read=1
		elif line.startswith('Periph'):
			read=2
		else:
			if read==1:
				line=line.split(' ')
				cores.append(line[:-1])
				allCores |= set(line[:-1])
			elif read==2:
				line=line.split(' ')
				peripherals.append(line[:-1])
				allPeripherals |= set(line[:-1])

	uniquePeripheralNodes=list(allPeripherals - allCores)
	
	return [cores, peripherals, uniquePeripheralNodes]


def merge(cores,peripherals,uniquePeripheralNodes):
	nodeNumber=1
	newCores=[]
	newPeriphery=[]
	edgeList=[]
	for i in range(len(cores)):
		newCores.append(nodeNumber)
		nodeNumber+=1

	for i in range(len(uniquePeripheralNodes)):
		newPeriphery.append(nodeNumber)
		nodeNumber+=1

	nodeIndex=1
	while len(cores)>0:
		currentCore=set(cores.pop(0))
		counter=nodeIndex+1
		for c in cores:
			if len(set(c)&currentCore)>0:
				edgeList.append((nodeIndex,counter))
			counter+=1

		relPeripheral=peripherals[nodeIndex-1]
		commonPeripheries=set(relPeripheral)&set(uniquePeripheralNodes)
		for pheriphery in commonPeripheries:
			idx=uniquePeripheralNodes.index(pheriphery)
			edgeList.append((nodeIndex,newPeriphery[idx]))
		nodeIndex+=1

	return edgeList

kplex_out = open(sys.argv[1],'r')
cores,peripherals,uniquePeripheralNodes = read_kplexOut(kplex_out)
edgeList=merge(cores,peripherals,uniquePeripheralNodes)

f=open('NewGraph.txt','w')
for edge in edgeList:
	f.write(str(edge[0])+'\t'+str(edge[1])+'\n')
