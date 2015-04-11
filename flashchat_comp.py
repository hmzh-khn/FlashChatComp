# import cv2 as cv
import pygame
import sys
import random
from pygame.locals import *
import convert

FRAME_RATE = 1000./180 #1000./80

Clock = pygame.time.Clock

# print "Using OpenCV v" + cv.__version__
print "Using pygame v" + pygame.__version__

# # currently broken on OS X
# def toggle_fullscreen():
#     screen = pygame.display.get_surface()
#     tmp = screen.convert()
#     caption = pygame.display.get_caption()
#     cursor = pygame.mouse.get_cursor()  # Duoas 16-04-2007 
    
#     w,h = screen.get_width(),screen.get_height()
#     flags = screen.get_flags()
#     bits = screen.get_bitsize()
    
#     #pygame.display.quit()
#     pygame.display.init()
    
#     screen = pygame.display.set_mode((w,h),flags^FULLSCREEN,bits)
#     screen.blit(tmp,(0,0))
#     pygame.display.set_caption(*caption)
 
#     pygame.key.set_mods(0) #HACK: work-a-round for a SDL bug??
 
#     pygame.mouse.set_cursor( *cursor )  # Duoas 16-04-2007
    
#     return screen

if __name__ == "__main__":
	pygame.init()

	size = width, height = 1000, 600
	upZero = 255, 0,0
	downZero = 0, 200,0
	upOne  = 255, 0,255
	downOne  = 0, 0,255

	black = 0, 0, 0
	white = 255, 255, 255

	screen = pygame.display.set_mode(size)
	clock = Clock()
	# isBlack = True
	isUp = False
	bits = convert.makeMessage("m","Testing")

	while True:
		for bit in bits:
			for event in pygame.event.get():
				if event.type == pygame.QUIT: sys.exit()

			time = clock.tick_busy_loop(FRAME_RATE)
			print float(time)

			if isUp:
				if bit == '1':
					screen.fill(upOne)
				else:
					screen.fill(upZero)
			else:
				if bit == '1':
					screen.fill(downOne)
				else:
					screen.fill(downZero)
			isUp = not isUp

			pygame.display.flip()
