import pygame
pygame.init()


import json


from verifyPreferences import verifyPreferences

defaultPreferences = {
	"screenSizeScale": 1,
}
verifyPreferences(defaultPreferences)

with open("preferences.json", "r") as f:
	preferences = json.load(f)