import urllib
import os, sys, json

def getData(fn, dirFrom, dirTo):
	text = file(dirFrom + "/" + fn).read()

	gateway = 'http://api.zemanta.com/services/rest/0.0/'
	args = {'method': 'zemanta.suggest',
		    'api_key': '************************',
		    'text': text,
		    'return_categories': 'dmoz',
		    'return_rdf_links' : 1,
		    'return_images' : 1,
		    'format': 'json'}            
	args_enc = urllib.urlencode(args)
	raw_output = urllib.urlopen(gateway, args_enc).read()
	
	if json.loads(raw_output)["status"] == "ok":
		fileObj = open(dirTo + "/" + fn, "w")
		fileObj.write(raw_output.encode('utf8'))
		fileObj.close()
	else:
		print "error " + fn

def zemifyAll(dirFrom, dirTo):
	count = 0
	for i in os.listdir(dirFrom):
		if os.path.isfile(dirFrom + "/" + i) == True :
			print count
			count += 1
			if os.path.isfile(dirTo + "/" + i) == False :
				getData(i, dirFrom, dirTo)

zemifyAll("./filtered", "./zemanta")
