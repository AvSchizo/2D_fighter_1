import json

def verifyGamefiles(default):

	blankDict = {}

	for key in default.keys():
		blankDict[key] = default[key]

	try:
		with open("preferences.json", "r") as f:
			prefDict = json.load(f)
	except:
		prefDict = {}

	for key in prefDict.keys():
		blankDict[key] = prefDict[key]


	with open("preferences.json", "w") as f:
		json.dump(blankDict, f, indent="\t")



if __name__ == "__main__":
	verifyGamefiles({})