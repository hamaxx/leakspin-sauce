import re, os,sys, json, operator

alltags = {}
allarticles = {}

def storeData(fn, dirFrom):
	zemanta = json.loads(file(dirFrom + "/" + fn).read())
	tags = zemanta["keywords"]
	allarticles[fn] = tags
	
	for tag in tags:
		if not tag["name"] in alltags:
			alltags[tag["name"]] = []
		alltags[tag["name"]].append({"cable" : fn[0:-4], "confidence" : tag["confidence"]})
	
def collectAll(dirFrom):
	count = 0
	for i in os.listdir(dirFrom):
		if os.path.isfile(dirFrom + "/" + i) == True:
			print count
			count += 1
			storeData(i, dirFrom)
			#if count > 100: break 

def saveTags(folder):
	print "saving tags"
	taglist = []
	for tag in alltags:	
		fn = re.sub(r'[\/\?\*\:\|"<>\\]', "_", tag).encode("utf8");
		fileObj = open(folder + "/" + fn + ".txt", "w")
		tagss = sorted(alltags[tag], key=lambda k: k['confidence'], reverse=True)
		json.dump(tagss, fileObj)
		fileObj.close()
		
		taglist.append({"tag" : tag, "len" : len(alltags[tag])})
	
	taglist = sorted(taglist, key=lambda k: k['tag'])
	fileObj = open(folder + "/list.txt", "w")
	json.dump(taglist, fileObj)
	fileObj.close()
	
def saveRelated(folder):
	print "saving related"
	for article in allarticles:
		related = {}
		for tag in allarticles[article]:
			for rea in alltags[tag["name"]]:
				if rea["cable"] != article[0:-4]:
					if rea["cable"] not in related:
						related[rea["cable"]] = 0
					related[rea["cable"]] += rea["confidence"] + tag["confidence"]
		relateds = sorted(related.iteritems(), key=operator.itemgetter(1), reverse=True)
		selected = []

		for r in relateds:
			if r[1] < 1: break
			selected.append({"cable": r[0], "confidence" : r[1]})
		fileObj = open(folder + "/" + article, "w")
		json.dump(selected, fileObj)
		fileObj.close()
		
collectAll("./zemanta")
saveTags("./tags")
saveRelated("./related")
print



