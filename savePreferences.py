import json

def savePreferences(prefs):

	with open("preferences.json", "w") as f:
		json.dump(prefs, f, indent="\t")