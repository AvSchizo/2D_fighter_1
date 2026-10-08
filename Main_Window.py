import pygame
pygame.init()
clock = pygame.time.Clock()


import json


from decimal import Decimal
decimal = Decimal


from pathlib import Path


# draw line
from drawLine import drawLine
def drawLine(points, inColor=None, specCam=None, inWidth=None):
	
	if inColor == None:
		color = "red"
	else:
		color = inColor

	if specCam == None:
		try:
			cam = globals["objects"]["camera"][0]
		except IndexError:
			cam = cameraClass()
	else:
		cam = specCam
	
	if inWidth == None:
		width = 1
	else:
		width = inWidth

	drawLine(points, cam, color, width, globals["screen"], preferences)


###################
#   preferences   #
###################
from verifyPreferences import verifyPreferences
from savePreferences import savePreferences

# default preferences here
defaultPreferences = {
	"screenSizeScale": .5,
	"playerWithControllerPriority": 1,
	"webMode": False,
	"maxFPS": 75,
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
	# you can get positions bigger than these, this just gives a reference for how to scale things
	"spacetimeSize": [3200, 1800],
	"pygameEvents": [],
	"userEvents": [],
	"mapBounds": {
		"bottom": -600,
		"left": -1800,
		"right": 1800,
		"top": None
	},
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




###################
#      boxes      #
###################
class hurtboxClass():

	def __init__(self, pos, inPoints, inID, inTangibility=0):

		# [topleft, bottomright, topright, bottomleft]
		self.points = [
			list(inPoints[0]),
			list(inPoints[1]),
			[inPoints[1][0], inPoints[0][1]],
			[inPoints[0][0], inPoints[1][1]],
		]
		for e in range(4):
			for i in range(2):
				self.points[e][i] += pos[i]

		self.id = inID

		# 0: regular
		# 1: freeze frames, no damage
		# 2: damage, no freeze frames
		# 3: like it's not event there
		self.tangibility = 0



	def hitboxCollision(self, hitboxes, touched):

		for hitbox in hitboxes:

			if hitbox.id in touched:
				continue

			# colliding?
			collided = False
			for box in hitbox.boxes:
				for p in self.points:
					pointA = box[0]
					pointB = box[1]
					# then it's inside box
					if p[0] > pointA[0] and p[0] < pointB[0] and p[1] > pointA[1] and p[1] < pointB[1]:
						collided = True
			if collided:
				info = [hitbox, self.tangibility]
				return info

		# no hitboxes touched
		return [None]

####################
class hitboxClass():

	def __init__(self, inID, inSus, pos, inBoxes, inType, info, inFollow=False):

		self.id = inID

		# if at -1, won't disappear
		self.sustain = inSus

		self.type = inType

		self.refPos = pos
		self.refBoxes = inBoxes
		self.follow(pos=self.refPos)

		self.following = inFollow

		self.info = info



	def update(self, pos=None):
		if self.sustain > 0:
			self.sustain -= 1

		if self.following:
			self.follow(pos)



	def follow(self, inPos=None, gonnaReturn=False):
		if inPos == None:
			pos = self.refPos
		else:
			pos = inPos
			self.refPos = inPos
		bo = []
		for box in self.refBoxes:
			forBox = []
			for i in range(2):
				forBox.append(box[i]+pos[i])
			bo.append(forBox)
		if gonnaReturn:
			# use gonnaReturn if you just want the updated boxes without actually updating them
			return bo
		else:
			self.boxes = bo

####################
#      /boxes      #
####################



#######################################
#                                     #
#           character class           #
#                                     #
#######################################
defaultCharacterPhysicsDict = {
	"gravity": -1,
	"maxFallSpeed": -50,
	"movementAccel": 5,
	"maxRunSpeed": 25,
	"jumpForce": 25,
}

class characterClass():

	def __init__(self, inID=0, inPhysics={}, inPlacement=0, inPos=[None, None]):

		# ID
		self.id = inID
		self.objID = "Ch"

		# PHYSICS
		self.physics = {}
		for key in defaultCharacterPhysicsDict.keys():
			self.physics[key] = defaultCharacterPhysicsDict[key]
		for key in inPhysics.keys():
			self.physics[key] = inPhysics[key]
		
		self.velocities = {
			"self": [0, 0],
			"dash": [0, 0],
			"push": [0, 0],
			"knockback": [0, 0],
		}
		self.airtime = 0

		# position
		self.direction = 1

		self.pos = [0, 0]
		if inPos[0] != None:
			self.pos[0] = inPos[0]
		if inPos[1] == None:
			self.pos[1] = globals["mapBounds"]["bottom"]
		else:
			self.pos[1] = inPos[1]

		# actions
		self.action = "idle"
		self.progress = 1
		## hitstun counts down
		self.hitstun = 0
		## stun after blocking attack, counts down
		self.blockstun = 0
		## each item in attackBuffer follows [action, time until gets removed from buffer list]
		self.attackBuffer = []

		# boxes
		self.hurtboxes = []
		self.hitboxes = []
		self.hitboxID = 0
		## list of enemy hitboxes touched
		self.othersTouched = []

		# health
		self.health = 144



	def loadSprites(self, characterName, version=1):
		spritePath = Path("characters") / characterName / "sprites" / f"alt{version}"

		returnDict = {}

		spriteList = [sprite for sprite in spritePath.iterdir()]

		for s in spriteList:
			att = str(s).split("_")
			if len(att) == 0:
				continue
			if len(att[-1].split(".")) > 1:
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
			if not ack in returnDict.keys():
				returnDict[ack] = []

			# sheets
			if she:
				for i in chopSprites(pygame.image.load(s).convert_alpha(), dim):
					returnDict[ack].append(i)

			else:
				returnDict[ack].append(pygame.image.load(s).convert_alpha())

		return returnDict
	


	def goToStart(self, placement=0):
		if placement == 0:
			self.pos[0] = -500
		else:
			self.pos[0] = 500
	


	def findOtherChar(self, place):
		self.otherChar = globals["objects"]["character"][place]
		


	def keysIntoInputs(self):
		pass
	


	def findDirection(self, re=False):
		if self.otherChar.pos[0] > self.pos[0]:
			if re:
				return 1
			else:
				self.direction = 1
		elif self.otherChar.pos[0] < self.pos[0]:
			if re:
				return -1
			else:
				self.direction = -1
		elif re:
			return None


	def update(self, segments=[1, 2]):

		if 1 in segments:

			if self.hitstun > 0:
				self.hitstun -= 1
			elif self.blockstun > 0:
				self.blockstun -= 1
			
			else:
				self.updateProgress()
				# player inputs here
				# hitboxes
				## nadda so far, do this later
		
		if 2 in segments:

			self.hurtboxes = self.findHurtboxes()
			for hurtbox in self.hurtboxes:
				info = hurtbox.hitboxCollision(self.otherChar.hitboxes, self.othersTouched)
				if info[0] != None:
					hitbox = info[1]
					self.othersTouched.append(hitbox.id)
					# all the rest of getting hit goes here

			self.doPhysics()




	def doPhysics(self):

		self.updateVelocities()

		# movement
		for key in self.velocities.keys():
			vel = self.velocities[key]

			# vertical movement
			if self.moveForVels(vel[1], 1) == "stopped" and vel[1] < 0:
				self.touchedGround()
				vel[1] = 0

			# horizontal movement
			self.moveForVels(vel[0], 0)
		
		# safety check
		while self.checkMapCollision(t=[0]):
			self.pos[1] += 1
		
		while self.checkMapCollision(t=[1]):
			self.pos[0] += 1
		
		while self.checkMapCollision(t=[2]):
			self.pos[0] -= 1
		
		while self.checkMapCollision(t=[3]):
			self.pos[1] -= 1
	


	def updateVelocities(self):
		for key in self.velocities.keys():
			vel = self.velocities[key]

			if key == "self":
				if vel[1] > self.physics["maxFallSpeed"]:
					distToMax = abs(self.physics["maxFallSpeed"] - vel[1])
					if distToMax < abs(self.physics["gravity"]):
						vel[1] += self.physics["maxFallSpeed"] - vel[1]
					else:
						vel[1] += self.physics["gravity"]



	def moveForVels(self, distance, dir):
		reps = abs(distance)

		for i in range(reps):
			lastPos = self.pos[dir]
			self.pos[dir] += distance/reps
			if self.checkMapCollision():
				self.pos[dir] = lastPos
				return "stopped"
		
		return "allG"



	def checkMapCollision(self, t=[0, 1, 2, 3]):
		# 0: floor collision
		# 1: left wall collision
		# 2: right wall collision
		# 3: ceiling collision

		for box in self.findCollisionbox():

			if globals["mapBounds"]["bottom"] != None:
				if box[1][1] <= globals["mapBounds"]["bottom"]:
					if 0 in t:
						return True
			
			if globals["mapBounds"]["left"] != None:
				if box[0][0] <= globals["mapBounds"]["left"]:
					if 1 in t:
						return True

			if globals["mapBounds"]["right"] != None:
				if box[1][0] >= globals["mapBounds"]["right"]:
					if 2 in t:
						return True

			if globals["mapBounds"]["top"] != None:
				if box[0][1] >= globals["mapBounds"]["top"]:
					if 3 in t:
						return True

		return False



	def touchedGround(self):
		if self.airtime > 0:
			self.action = "idle"
			self.progress = 1
		self.airtime = 0
		self.velocities["self"][1] = 0
	


	def draw(self, specCam=None):

		if specCam == None:
			try:
				cam = globals["objects"]["camera"][0]
			except:
				cam = cameraClass()
		else:
			cam = specCam

		scaling = cam.getScaling(objDist=self.dist)*preferences["screenSizeScale"]
		
		scrn = globals["screen"]

		for pack in self.findYourSprite():

			image, offset = pack
			image = pygame.transform.scale(image, [image.get_width()*scaling, image.get_height()*scaling])

			rect = image.get_rect(midbottom=(scrn.get_width()/2+(self.pos[0]-cam.pos[0]+offset[0])*scaling, scrn.get_height()/2-(self.pos[1]-cam.pos[1]+offset[1])*scaling))

			scrn.blit(image, rect)

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

	def __init__(self, inID=0, inX=None, inY=None, inDist=0, costume=1):
		super().__init__(inID=inID, inPhysics=JaneDoePhysicsDict, inPos=[inX, inY])

		# ID
		self.objID += "_JaDo"

		# sprites
		self.costume = costume
		self.sprites = self.loadSprites("Jane Doe", self.costume)

		# position
		self.dist = inDist

		# character path
		self.characterPath = Path("characters") / "Jane Doe"
	


	def findYourSprite(self):
		# you may have to scale the sprite to the correct size if the actual file is bigger than it should be
		# this is separate from the screen and camera scaling

		packs = []

		if preferences["webMode"]:

			# body
			image = pygame.surface.Surface((100, 200))
			if self.costume == 1:
				image.fill("red")
			elif self.costume == 2:
				image.fill("blue")
			else:
				image.fill("black")
			offset = [0, 0]
			packs.append([image, offset])

			# head
			image = pygame.surface.Surface((50, 50))
			if self.costume == 1:
				image.fill((220, 177, 135))
			elif self.costume == 2:
				image.fill((214, 177, 140))
			else:
				image.fill((214, 177, 135))
			offset = [50*self.direction, 150]
			packs.append([image, offset])
		

		else:
			pass
			# put actual sprites here
			# it's very possible you don't have more than one pack in packs

		
		return packs



	def updateProgress(self):

		self.findDirection()

		if self.action == "idle":
			if self.progress >= 1:
				self.progress = 1
			else:
				self.progress = 1
	


	def findHurtboxes(self):
		if self.action == "idle":
			return [hurtboxClass(self.pos, [(-50, 200), (50, 0)], 0)]
	


	def findCollisionbox(self, inPos=None):

		if inPos == None:
			pos = self.pos
		else:
			pos = inPos

		boxes = []

		# temp, don't use
		toAdd = [
			[pos[0]-50, pos[1]+200],
			[pos[0]+50, pos[1]]
		]
		boxes.append(toAdd)
		#

		return boxes

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



	def updateBorders(self):
		scaling = 1/self.getScaling()
		self.borders = {
			"left": self.pos[0] - self.size[0]/2*scaling,
			"right": self.pos[0] + self.size[0]/2*scaling,
			"top": self.pos[1] - self.size[1]/2*scaling,
			"bottom": self.pos[1] + self.size[1]/2*scaling
		}
		for b in [self.borders[key] for key in self.borders.keys()]:
			b = round(b)

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
			globals["objects"]["character"].append(characterList[characterPointPlace[playerChoices[i+1]]](inID=len(globals["objects"]["character"])))
		except:
			globals["objects"]["character"].append(characterList[characterPointPlace[0]](inID=len(globals["objects"]["character"])))

	for i in range(2):
		globals["objects"]["character"][i].goToStart(placement=i)
	for i in range(2):
		globals["objects"]["character"][i].findOtherChar(place=(-i+1))

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
	globals["currentFrame"] += 1

	# main menu
	if int(globals["gameState"]/100) == 1:

		if globals["gameState"] == 100:
			load_mainMenu()




	# main combat
	if int(globals["gameState"]/100) == 2:

		if globals["gameState"] == 200:
			load_mainFight()


		for i in range(2):
			for player in globals["objects"]["character"]:
				player.update(segments=[i+1])


		for camera in globals["objects"]["camera"]:
			camera.updateBorders()

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

	for ls in globals["objects"].keys():
		for obj in globals["objects"][ls]:
			try:
				obj.draw()
			except AttributeError:
				pass
	
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




	clock.tick(preferences["maxFPS"])
