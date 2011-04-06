import os, json

#name	created	released	status	source

data = [];
data.append("name	created	released	status	source")
data.append("string	c	c	string	string")
data.append("meta")

def parseFile(fn, dirFrom):
	f = open(dirFrom + "/" + fn, 'r')
	cont = []
	for i in xrange(5):
		s = f.readline()[0:-1]
		if i == 1 or i == 2: s = s[0:4]
		cont.append(s)		
	f.close()
	data.append("\t".join(cont))
		

def collectAll(dirFrom):
	count = 0
	for i in os.listdir(dirFrom):
		if os.path.isfile(dirFrom + "/" + i) == True:
			cons = json.loads(file("../related/" + i).read())
			if len(cons) > 0:
				print count
				count += 1
				parseFile(i, dirFrom)
			

collectAll("../filtered")

fileObj = open("./leaks.tab", "w")
fileObj.write("\n".join(data).encode('utf8'))
fileObj.close()
