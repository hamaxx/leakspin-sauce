import os, json, re

#name	created	released	status	source

data = [];
data.append("name	created	released	status	source	title")
data.append("d	c	c	d	d	d")
data.append("meta					meta")

def parseFile(fn, dirFrom):
	f = open(dirFrom + "/" + fn, 'r')
	cont = []
	for i in xrange(5):
		s = f.readline().decode("utf-8")[0:-1]
		if i == 1 or i == 2: s = s[0:4]
		cont.append(s)
	regex = re.compile(r'\nSUBJECT: *(.*?)\n', re.MULTILINE)
	match = re.search(regex, f.read().decode("utf-8"))
	if match: cont.append(match.groups()[0])
	else: cont.append("x")
	
	f.close()
	data.append("\t".join(cont))
		

def collectAll(dirFrom):
	count = 0
	for i in os.listdir(dirFrom):
		if os.path.isfile(dirFrom + "/" + i) == True:
			cons = json.loads(file("../related/" + i).read().decode("utf-8"))
			if len(cons) > 0:
				print count
				count += 1
				parseFile(i, dirFrom)
			

collectAll("../filtered")

fileObj = open("./leaks.tab", "w")
fileObj.write("\n".join(data).encode('ascii', 'replace'))
fileObj.close()
