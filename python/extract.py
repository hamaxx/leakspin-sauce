from BeautifulSoup import BeautifulSoup
import re, os,sys

def parseFile(fn):
	html = file(fn)
	soup = BeautifulSoup(html)
	text = ""

	header = soup.find("table", { "class" : "cable" }).findAll("a")
	for a in header:
		text += a.string + "\n"
	text += "\n"

	pre = soup.findAll("pre")
	for t in pre:
		[tag.extract() for tag in t.findAll(True)]
		t = unicode(t.renderContents(), "utf8")
		t = re.sub(r"&#x.{4};", "\n", t)
		text += t + "\n\n"
	
	fileObj = open("filtered/" + os.path.basename(fn)[0:-4] + "txt", "w")
	fileObj.write(text.encode('utf8'))
	fileObj.close()

count = 0
def filterAll(dire):
	global count
	contents=os.listdir(dire)
	for i in contents:
		path = dire + "/" + i
		if os.path.isfile(path) == True :
			print count
			count += 1
			if os.path.isfile("filtered/" + i) == False :
				parseFile(path)
		elif os.path.isdir(path) == True :
			filterAll(path)


filterAll("./cable")

