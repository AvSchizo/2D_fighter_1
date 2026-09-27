# game name: "The Watch"

import pygame
pygame.init()
clock = pygame.time.Clock()


import json


###################
#   preferences   #
###################
from verifyPreferences import verifyPreferences

# default preferences here
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
	"spacetimeSize": [1600, 900],
	"events": [],
	"pygameEvents": [],
}

####################
#     /globals     #
####################




####################
#      SCREEN      #
####################
screenSize = [
	globals["spacetimeSize"][0] * preferences["screenSizeScale"],
	globals["spacetimeSize"][1] * preferences["screenSizeScale"],
]
screen = pygame.display.set_mode(screenSize)

#####################
#      /SCREEN      #
#####################




#######################################
#                                     #
#             event class             #
#                                     #
#######################################
class eventClass():

	def __init__(self, inType=None, inName=None, inInfo=[]):

		# type
		self.type = inType

		# from who
		self.fromWho = inName

		# info
		self.info = inInfo



	def printInfo(self):
		for l in self.info:
			print(l)

########################################
#                                      #
#             /event class             #
#                                      #
########################################




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

	def __init__(self, inPhysics={}):

		# ID
		## regular id is set to 0 as the characterClass is not meant to be used standalone
		self.id = 0
		## Ch for character
		self.objID = "Ch"

		# PHYSICS
		self.physics = {}
		for key in defaultCharacterPhysicsDict.keys():
			self.physics[key] = defaultCharacterPhysicsDict[key]
		for key in inPhysics.keys():
			self.physics[key] = inPhysics[key]

########################################
#                                      #
#           /character class           #
#                                      #
########################################




########################################
#                                      #
#             camera class             #
#                                      #
########################################
class cameraClass():

	def __init__(self, inSize=None, inDistance=0):

		# size
		if inSize == None:
			self.size = globals["spacetimeSize"]
		else:
			self.size = inSize

		# distance
		self.distance = inDistance

#########################################
#                                       #
#             /camera class             #
#                                       #
#########################################





###########################################################
#                                                         #
#                                                         #
#                        MAIN LOOP                        #
#                                                         #
#                                                         #
###########################################################
def mainLoop():

	########################################
	#                                      #
	#             FRAME DUTIES             #
	#                                      #
	########################################
	globals["currentFrame"] += 1

	# pygame events
	globals["pygameEvents"] = pygame.event.get()
	for event in globals["pygameEvents"]:

		if event.type == pygame.QUIT:

			globals["running"] = False
			quit()



	# user events
	while len(globals["events"]) > 0:
		event = globals["events"][0]

		if event.type == None:
			pass

		elif event.type == "report":
			print(f"event, report: {event.fromWho}")
			event.printInfo()

		else:
			print(f"event type: {event.type} is unknown")


		# once done with event
		globals["events"].pop(0)





	# CALC




	# RENDERING



	pygame.display.update()

############################################################
#                                                          #
#                                                          #
#                        /MAIN LOOP                        #
#                                                          #
#                                                          #
############################################################








if __name__ != "__main__":
	quit()



########################################
#                                      #
#              frame loop              #
#                                      #
########################################
timeGrotched = 0
lastGrotch = pygame.time.get_ticks()
while globals["running"]:

	timeGrotched += pygame.time.get_ticks() - lastGrotch

	timeBetweenFrames = 1000/globals["FPS"]

	for i in range(int(timeGrotched/(timeBetweenFrames))):
		timeGrotched -= timeBetweenFrames
		mainLoop()

	clock.tick(globals["FPS"])