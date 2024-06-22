#! /usr/bin/python3

import pygame
from numpy.random import random, randint
from numpy import where

WIDTH, HEIGHT = 800, 800
N_WIDTH, N_HEIGHT = 800,800


def main():

	pygame.init()
	pygame.display.set_caption("video noise")

	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	noise_surface = pygame.Surface((N_WIDTH, N_HEIGHT))
	font = pygame.font.SysFont('Courier New, courier, monospace', 32, bold=True)

	running = True
	clock = pygame.time.Clock()
	dt = 0
	text = font.render('fps: ?', False, (255, 255, 0))

	# main loop
	while running:
		# noise = randint(0, 1, (WIDTH, HEIGHT))
		noise = randint(0, 2, (N_WIDTH, N_HEIGHT))
		# noise = where(noise == 1, 255, 0)
		noise = where(noise == 1, -1, -16777216)
		pygame.surfarray.blit_array(noise_surface, noise)
		pygame.transform.scale(noise_surface, (WIDTH, HEIGHT), dest_surface=screen)

		# pixels = pygame.surfarray.pixels3d(screen)
		# # pixels = pygame.surfarray.pixels2d(screen)
		# print(pixels)
		# print(pixels.shape)
		# print("----")
		# print(pixels[0])
		# print(pixels[0].shape)
		# print("wwwww")
		# print(pixels[0][0])
		# print(pixels[0][0].shape)
		# print("----")
		# # pixels[:] = noise
		# for i in range(3):
		# 	print(pixels[:, :, i])
		# 	print("?????????")
		# 	pixels[:, :, i] = noise
		# del pixels
		# it makes sense to throttle the framerate (which is what the 30 in
		# clock.tick(30) achieves) because it is pointless to have a framerate
		# higher than the screen refresh rate (which is usually 60). To run at
		# full speed, remove the 30
		dt += clock.tick()
		# don't refresh the OSD more than once per sec.
		if dt > 1000:
			dt = 0
			text = font.render(f'fps: {clock.get_fps():.1f}', True, (255, 255, 0))
		screen.blit(text, (10, 10))
		pygame.display.flip()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
		# break

if __name__ == '__main__':
	main()
