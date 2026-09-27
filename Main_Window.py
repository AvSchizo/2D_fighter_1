import pygame
pygame.init()
clock = pygame.time.Clock()


import json


from decimal import Decimal
decimal = Decimal


###################
#   preferences   #
###################
from verifyPreferences import verifyPreferences
from savePreferences import savePreferences

# default preferences here
defaultPreferences = {
	"screenSizeScale": (9/16),
	"playerWithControllerPriority": 1,
}

#
# please please please turn this off for an official release
#
savePreferencesAsDefault = True
if savePreferencesAsDefault:
	savePreferences(defaultPreferences)


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
	"spacetimeSize": [3200, 1800],
	"events": [],
	"pygameEvents": [],
	"objects": {
		"cameras": [],
		"characters": [],
	},
	"IDs": {
		"event": 0,
		"camera": 0,
		"character": 0,
	},
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
globals["screen"] = pygame.display.set_mode(screenSize)
pygame.display.set_caption("The Watch")

#####################
#      /SCREEN      #
#####################




#######################################
#                                     #
#             event class             #
#                                     #
#######################################
class eventClass():

	def __init__(self, inType=None, inName=None, inInfo=[], inID=0):

		# ID
		self.id = inID
		self.objID = "Ev"

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

	def __init__(self, inPhysics={}, inID=0):

		# ID
		self.id = inID
		self.objID = "Ch"

		# PHYSICS
		self.physics = {}
		for key in defaultCharacterPhysicsDict.keys():
			self.physics[key] = defaultCharacterPhysicsDict[key]
		for key in inPhysics.keys():
			self.physics[key] = inPhysics[key]

		self.velocity = [0, 0]

########################################
#                                      #
#           /character class           #
#                                      #
########################################




########################################
#                                      #
#               Jane Doe               #
#                                      #
########################################
defaultCharacterPhysicsDict = {
	"gravity": -10,
	"maxFallSpeed": -50,
	"movementAccel": 5,
	"maxRunSpeed": 25,
	"jumpForce": 25,
}

class characterClass():

	def __init__(self, inPhysics={}, inID=0):

		# ID
		self.id = inID
		self.objID = "Ch"

		# PHYSICS
		self.physics = {}
		for key in defaultCharacterPhysicsDict.keys():
			self.physics[key] = defaultCharacterPhysicsDict[key]
		for key in inPhysics.keys():
			self.physics[key] = inPhysics[key]

		self.velocity = [0, 0]

#########################################
#                                       #
#               /Jane Doe               #
#                                       #
#########################################




########################################
#                                      #
#             camera class             #
#                                      #
########################################
class cameraClass():

	def __init__(self, inID=0, inSize=None, inDistance=0, inPos=[0, 0]):

		# ID
		self.id = inID
		self.objID = "Ca"

		# size
		if inSize == None:
			self.size = globals["spacetimeSize"]
		else:
			self.size = inSize

		# distance
		self.distance = inDistance

		# pos
		self.pos = inPos

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




	########################################
	#                                      #
	#              MAIN CALCS              #
	#                                      #
	########################################

	# main fighting state
	if int(globals["gameState"]/10) == 1:

		pass




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

	# will count the time since last frame, add it to counter
	# for however many ticks worth of time is in counter:
	# repeat game update that many times

	# this is to keep a non framerate-dependant fighting game "frame" system

	timeGrotched += pygame.time.get_ticks() - lastGrotch

	timeBetweenFrames = 1000/globals["FPS"]

	for i in range(int(timeGrotched/(timeBetweenFrames))):
		timeGrotched -= timeBetweenFrames
		mainLoop()

	clock.tick(globals["FPS"])