import pygame
pygame.init()


import json


###################
#   preferences   #
###################
from verifyPreferences import verifyPreferences

defaultPreferences = {
	"screenSizeScale": 1,
}
verifyPreferences(defaultPreferences)

with open("preferences.json", "r") as f:
	preferences = json.load(f)
####################
#   /preferences   #
####################




###################
#     globals     #
###################
globals = {
	"currentFrame": 0,
	"gameState": 10,
}
####################
#     /globals     #
####################




#######################################
#                                     #
#           character class           #
#                                     #
#######################################
defaultCharacterPhysicsDict = {
	"gravity": -10,
	"maxFallSpeed": -50,
	"movementAccel": 5,
	"maxRunSpeed": 25,
	"jumpForce": 25,
}

class characterClass():

	def __init__(self, inPhysics=defaultCharacterPhysicsDict):

		# PHYSICS
		self.gravity = inPhysics["gravity"]
		self.maxFallSpeed = inPhysics["maxFallSpeed"]
		self.movementAccel = inPhysics["movementAccel"]
		self.maxRunSpeed = inPhysics["maxRunSpeed"]
		self.jumpForce = inPhysics["jumpForce"]

########################################
#                                      #
#           /character class           #
#                                      #
########################################