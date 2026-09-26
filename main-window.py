import pygame
pygame.init()


import json


from verifyGamefiles import verifyGamefiles

defaultPreferences = {
	"screenSizeScale": 1,
}
verifyGamefiles(defaultPreferences)

with open("preferences.json", "r") as f:
	preferences = json.load(f)