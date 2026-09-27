# game name: "The Watch"

import pygame
pygame.init()
clock = pygame.time.Clock()


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
	"running": True,
	"currentFrame": 0,
	"gameState": 10,
	"tickRate": 60,
	"FPS": 75,
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





#######################################
#                                     #
#              MAIN LOOP              #
#                                     #
#######################################
def mainLoop():
	pass

	# CALC




	# RENDERING

########################################
#                                      #
#              /MAIN LOOP              #
#                                      #
########################################


if __name__ != "__main__":
	quit()


timeGrotched = 0
lastGrotch = pygame.time.get_ticks()
while globals["running"]:

	timeGrotched += pygame.time.get_ticks() - lastGrotch

	timeBetweenFrames = 1000/globals["FPS"]

	for i in range(int(timeGrotched/(timeBetweenFrames))):
		timeGrotched -= timeBetweenFrames
		mainLoop()

	clock.tick(globals["FPS"])