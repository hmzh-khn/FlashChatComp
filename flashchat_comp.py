# import cv2 as cv
import pygame
import sys
import random
from pygame.locals import *

FRAME_RATE = 60

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

	size = width, height = 320, 240
	black = 0, 0, 0
	white = 255, 255, 255

	screen = pygame.display.set_mode(size)
	clock = Clock()
	isBlack = True

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: sys.exit()

		time = clock.tick_busy_loop(FRAME_RATE)
		print float(time)

		if isBlack:
			screen.fill(white)
			isBlack = False
		else:
			screen.fill(black)
			isBlack = True

		pygame.display.flip()
