import pygame

def drawLine(points, camera, color, width, screen, prefs):

	scaling = prefs["screenSizeScale"]*camera.getScaling()

	reals = [[], []]

	for e in range(2):
		for i in range(2):
			reals[e].append((points[e][i]-camera.pos[i])*scaling)

	pygame.draw.line(screen, color, reals[0], reals[1], width)
