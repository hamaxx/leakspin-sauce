import os, json

data = [];
tags = []

def parseFile(fn, dirFrom):
	f = open(dirFrom + "/" + fn, 'r')
	cont = []
	for i in xrange(5):
		s = f.readline().decode('utf8')[0:-1]
		if i == 1 or i == 2: s = s[0:4]
		cont.append(s)		
	f.close()
	
	zemanta = json.loads(file("../zemanta/" + fn).read().decode('utf8'))
	zt = zemanta["keywords"]
	ztn = []
	for t in zt: ztn.append(t["name"])
	for t in tags:
		if t in ztn:
			cont.append("1")
		else:	
			cont.append("0")
	
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

def coolTags(dirFrom):
	count = 0;
	for i in os.listdir(dirFrom):
		if os.path.isfile(dirFrom + "/" + i) == True:
			cons = json.loads(file("../tags/" + i).read())
			if len(cons) > 5:	#min n connections
				count += 1;
				i = i.decode('utf8')
				tags.append(i[0:-4])
	print count
	
coolTags("../tags")


data.append("name	created	released	status	source	_" + "\t_".join(tags))
data.append("d	c	c	d	d" + "	d" * len(tags))
data.append("meta")

collectAll("../filtered")

fileObj = open("./leaksWithTags.tab", "w")
fileObj.write("\n".join(data).encode('ascii', 'replace'))
fileObj.close()
