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
	# if gameSate%100 == 0, that is a loading state, and will trigger the load function for whatever the hundreds place is
	# so please change it to 100 for release
	"gameState": 200,
	"substate": 0,
	"tickRate": 60,
	"FPS": 75,
	"spacetimeSize": [3200, 1800],
	"pygameEvents": [],
	"userEvents": [],
}



def resetObjects():
	globals["objects"] = {
		"camera": [],
		"character": [],
		"pointer": [],
		"background": [],
	}

resetObjects()
globals["ID"] = {}
for key in globals["objects"].keys():
	globals["ID"][key] = 0

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




####################
#  player pointer  #
####################
class playerPointerClass():

	def __init__(self, inID=1, inType="CharSel", inPoint=0):
		
		# ID
		self.objID = "PlPo"
		self.id = inID

		# type
		self.type = inType

		# pointing to
		self.point = inPoint
	


	def movePointer(self, direction):

		# character select
		if self.type == "CharSel":

			if direction == "left":

				if self.point == 0:
					self.point = len(characterList.keys())-1
				
				else:
					self.point -= 1
			
			if direction == "right":

				if self.point == len(characterList.keys())-1:
					self.point = 0
				
				else:
					self.point += 1


		# character select
		if self.type == "MainMenu":

			pass

#####################
#  /player pointer  #
#####################



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

	def __init__(self, inID=0, inPhysics={}, inPos=[0, 0], inDist=0):

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

		# actions
		self.action = "idle"
		self.progress = 1



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
								globals["userEvents"].append(eventClass(inType="error", inName="characterClass, loadSprites()", inInfo=["incorrect sprite sheet dimensions", spritePath]))
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
	


	def draw(self, specCam=None):

		if specCam == None:
			try:
				cam = globals["objects"]["camera"][0]
			except:
				cam = cameraClass()
		else:
			cam = specCam
		
		scrn = globals["screen"]

		scaling = cam.getScaling(objDist=self.distance)*preferences["screenSizeScale"]

		image = self.findYourSprite()

		rect = image.get_rect(center=(scrn.get_width()/2+(self.pos[0]-cam.pos[0])*scaling, scrn.get_height()/2-(self.pos[1]-cam.pos[1])*scaling))
	


	def findYourSprite(self):
		# this is here so no one's confused, replace it when defining the character
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
characterList = {}
characterPointPlace = {}

####################
#     Jane Doe     #
####################
# empty dict here means no changes from default physics
JaneDoePhysicsDict = {}

class JaneDoeClass(characterClass):

	def __init__(self, inID=0, inPos=[0, 0], inDist=0):
		super().__init__(inID=inID, inPhysics=JaneDoePhysicsDict)

		# ID
		self.objID += "_JaDo"

		# sprites
		self.sprites = self.loadSprites("Jane Doe", self.id+1)

		# position
		self.pos = inPos
		self.dist = inDist
	


	def findYourSprite(self):
		# this is a test! don't use this!
		image = pygame.Surface((50, 50))
		image.fill("red")
		return image

characterList["Jane Doe"] = JaneDoeClass
characterPointPlace[0] = "Jane Doe"
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

	def __init__(self, inID=0, inSize=None, inDistance=0, inPos=[0, 0], scalingReference=[1/2, 10]):

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

		# scaling
		self.scalingFactor = scalingReference[0]**(1/scalingReference[1])
	


	def getScaling(self, objDist=0):
		return self.scalingFactor**(self.distance-objDist)

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
		
		if inType == "main combat":
			self.objID += "Mc"
			backgroundPath = "Main Combat"

		else:
			self.objID += "Er"
			backgroundPath = "Error"

		# image
		if backgroundPath == "Error":
			self.image = Path("Error") / "background.png"
		else:
			self.image = Path("backgrounds") / backgroundPath / "background.png"

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




########################################
#                                      #
#             transitions              #
#                                      #
########################################

# main menu
def load_mainMenu():
	globals["gameState"] = 101
	globals["substate"] = 0
	resetObjects()
	globals["objects"]["camera"].append(cameraClass())
	globals["objects"]["pointer"].append(playerPointerClass())
	globals["objects"]["background"].append(backgroundClass(inType="main menu"))


# main combat
def load_mainFight():
	globals["gameState"] = 201
	globals["substate"] = 0

	playerChoices = {1: None, 2: None}
	for p in globals["objects"]["pointer"]:
		playerChoices[p.id] = p.point
	for k in playerChoices.keys():
		if playerChoices[k] == None:
			playerChoices[k] = 0

	resetObjects()
	globals["objects"]["camera"].append(cameraClass())
	for i in range(2):
		try:
			globals["objects"]["character"].append(characterList[characterPointPlace[playerChoices[i+1]]])
		except:
			globals["objects"]["character"].append(characterList[0])
	globals["objects"]["background"].append(backgroundClass(inType="main combat"))

#########################################
#                                       #
#             /transitions              #
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

	# main menu
	if int(globals["gameState"]/100) == 1:

		if globals["gameState"] == 100:
			load_mainMenu()




	# main combat
	if int(globals["gameState"]/100) == 2:

		if globals["gameState"] == 200:
			load_mainFight()

############################################################
#                                                          #
#                                                          #
#                        /MAIN LOOP                        #
#                                                          #
#                                                          #
############################################################




###########################################################
#                                                         #
#                                                         #
#                        RENDERING                        #
#                                                         #
#                                                         #
###########################################################
def renderAll():


	globals["screen"].fill("lavender")

	pygame.display.update()

############################################################
#                                                          #
#                                                          #
#                        /RENDERING                        #
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
	while len(globals["userEvents"]) > 0:
		event = globals["userEvents"][0]

		if event.type == None:
			pass

		else:
			print(f"event, {event.type}: {event.fromWho}")
			event.printInfo()


		# once done with event
		globals["userEvents"].pop(0)



	
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
	renderAll()




	clock.tick(globals["FPS"])
