import os, json

#def parseFile(fn, dirFrom):

nameToId = {}	

def collectVertices(dirFrom):
	vert = []
	count = 1
	for i in os.listdir(dirFrom):
		if os.path.isfile(dirFrom + "/" + i) == True:
			cons = json.loads(file(dirFrom + "/" + i).read())
			if len(cons) > 0:
				vert.append(str(count) + " " + "\"" + i + "\"")
				nameToId[i[0:-4]] = count
				count += 1
	return vert
	
def collectEdges(dirFrom):
	edg = []
	for i in os.listdir(dirFrom):
		if os.path.isfile(dirFrom + "/" + i) == True:
			cons = json.loads(file(dirFrom + "/" + i).read())
			#print i
			for c in cons:
				edg.append(str(nameToId[i[0:-4]]) + " " + str(nameToId[c["cable"]]) + " " + str(c["confidence"]))
	return edg
			

v = collectVertices("../related")
vertices = "\n\n".join(["*Network \"Wikileaks Cablegate by Ham\" ", "*Description \"bla bla\"", "*Vertices     " + str(len(v))])
vertices += "\n" + "\n".join(v)

e = collectEdges("../related")
edges = "*Edges "
edges += "\n" + "\n".join(e)

fileObj = open("./leaks.net", "w")
fileObj.write("\n".join([vertices, edges]).encode('utf8'))
fileObj.close()


