import pygame
pygame.init()
clock = pygame.time.Clock()


import json


from decimal import Decimal
decimal = Decimal


from pathlib import Path


###################
#   preferences   #
###################
from verifyPreferences import verifyPreferences
from savePreferences import savePreferences

# default preferences here
defaultPreferences = {
	"screenSizeScale": .5,
	"playerWithControllerPriority": 1,
}

#
# please please please make sure this is off for an official release
#
savePreferencesAsDefault = False
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
	"gameState": 20,
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
		"camera": 0,
		"character": 0,
	},
}

####################
#     /globals     #
####################




###################
#     sprites     #
###################
def chopSprites(sheet, size):
	ref = sheet
	w = ref.get_width()/size[0]
	h = ref.get_height()/size[1]

	rows = []
	for e in range(size[1]):
		print(e*h)
		rows.append(ref.subsurface(pygame.Rect(0, e*h, ref.get_width(), h)))
	print()

	all = []
	for r in rows:
		for a in range(size[0]):
			all.append(r.subsurface(pygame.Rect(a*w, 0, w, h)))

	return all

####################
#     /sprites     #
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

	def __init__(self, inType=None, inName=None, inInfo=[]):

		# ID
		self.objID = "Ev"
		if inType == None:
			self.objID += "_No"
		else:
			self.objID += "_" + str(inType)[:2]

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



	def loadSprites(self, characterName, version=1):
		spritePath = Path("characters") / characterName / "sprites" / "alt" + str(version)

		returnDict = {}

		spriteList = [sprite for sprite in spritePath.iterdir()]

		for s in spriteList:
			att = s.split("_")
			if len(att) == 0:
				continue
			if len(att[-1].split(".") > 1):
				att[-1] = att[-1].split(".").pop(-1)

			# which attack
			ack = att[0]

			# if a sheet
			if len(att) >= 2:
				wa = att[1].split()
				if wa[0] == "sheet":
					if len(wa) > 1:
						dim = []
						for i in range(2):
							try:
								dim.append(int(wa[1].split("-")[i]))
							except ValueError:
								globals["events"].append(eventClass(inType="error", inName="characterClass, loadSprites()", inInfo=["incorrect sprite sheet dimensions", spritePath]))
								dim.append(1)
				else:
					she = False
			else:
				she = False


			# making sure place for it exists
			if not att in returnDict.keys():
				returnDict[att] = []

			# sheets
			if she:
				for i in chopSprites(pygame.image.load(s).convert_alpha(), dim):
					returnDict[ack].append(i)

			else:
				returnDict[ack].append(pygame.image.load(s).convert_alpha())

		return returnDict



	def keysIntoInputs(self):
		pass

########################################
#                                      #
#           /character class           #
#                                      #
########################################




############################################################
#                                                          #
#                                                          #
#                        characters                        #
#                                                          #
#                                                          #
############################################################

####################
#     Jane Doe     #
####################
# empty dict here means no changes from default physics
JaneDoePhysicsDict = {}

class JaneDoeClass(characterClass):

	def __init__(self, inID=0):
		super().__init__(inID=inID, inPhysics=JaneDoePhysicsDict)

		# ID
		self.objID += "_JaDo"

		# sprites
		self.sprites = self.loadSprites("Jane Doe", self.id+1)

#####################
#     /Jane Doe     #
#####################

#############################################################
#                                                           #
#                                                           #
#                        /characters                        #
#                                                           #
#                                                           #
#############################################################




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




########################################
#                                      #
#           background class           #
#                                      #
########################################
class backgroundClass():

	def __init__(self, inType=None, inDistance=0, inPos=[0, 0]):

		# ID
		self.objID = "Ba"

		if inType == "main menu":
			self.objID += "Mm"
			backgroundPath = "Main Menu"

		else:
			self.objID += "Er"
			backgroundPath = "Error"

		self.image = Path(backgroundPath) / "background.png"

		# distance
		self.distance = inDistance

		# pos
		self.pos = inPos

#########################################
#                                       #
#           /background class           #
#                                       #
#########################################




###################
#    main menu    #
###################
mainMenu = {
	"background"
}

####################
#    /main menu    #
####################





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

		else:
			print(f"event, {event.type}: {event.fromWho}")
			event.printInfo()


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




	# main menu
	if int(globals["gameState"]/10) == 2:

		pass





############################################################
#                                                          #
#                                                          #
#                        /MAIN LOOP                        #
#                                                          #
#                                                          #
############################################################








if __name__ != "__main__":
	quit()


#frickin test
scale = 1/1
aaaa = chopSprites(pygame.image.load(Path(Path("characters")/"Jane Doe"/"sprites"/"alt2"/"shutupholup.png")), [3, 3])


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
	lastGrotch = pygame.time.get_ticks()

	timeBetweenFrames = 1000/globals["tickRate"]

	for i in range(int(timeGrotched/(timeBetweenFrames))):
		timeGrotched -= timeBetweenFrames
		mainLoop()


	
	#######################################
	#                                     #
	#              RENDERING              #
	#                                     #
	#######################################
	globals["screen"].fill("blue")
	for i in range(len(aaaa)):
		wa = aaaa[i]
		globals["screen"].blit(wa, (0, wa.get_height()*i))

	pygame.display.update()

	clock.tick(globals["FPS"])