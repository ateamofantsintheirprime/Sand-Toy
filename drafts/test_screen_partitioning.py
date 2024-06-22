import sys
import pygame
import cProfile, pstats, io
from pstats import SortKey
from screen_partition import screen_partition
from pygame.locals import *
from math import floor
from basic import sand_count, print_pixels

pygame.init()

fps = 1
fpsClock = pygame.time.Clock()
width, height = 800, 800
screen = pygame.display.set_mode((width, height))
sand_width, sand_height = 50,50
sand_surface = pygame.Surface((sand_width, sand_height))

pixels = pygame.surfarray.array3d(sand_surface)
root_partition = screen_partition(0,0,sand_width,sand_height,pixels, None,8,5)

i = 0
while True:
	print(f"starting frame {i}")
	# if i > 5:
		# break
	# print("BEGINNING OF FRAME PIXEL STATE:")
	# print_pixels(pixels)
	# root_partition.new_frame_2()
	if any(pygame.mouse.get_pressed()):
		mouse_pos = list(pygame.mouse.get_pos())
		mouse_pos[0] = int(floor(mouse_pos[0] * sand_width/width))
		mouse_pos[1] = int(floor(mouse_pos[1] * sand_height/height))
		print(mouse_pos)
		radius = 1
		root_partition.add_sand(mouse_pos, radius)
	for event in pygame.event.get():

		if event.type == QUIT:
			pygame.quit()
			sys.exit()

  # Update.
  
	# root_partition.clear_did_base_sim()
	root_partition.recursive_simulation()
	print("END OF FRAME PIXEL STATE:")
	# print_pixels(pixels)
	# cProfile.run('root_partition.recursive_simulation()')

  # Draw.
	pygame.pixelcopy.array_to_surface(sand_surface, pixels)
	pygame.transform.scale(sand_surface, (width,height), dest_surface=screen)
	# print(sand_count(pixels))
	# screen.blit(sand_surface, (0,0))
	# root_partition.draw(screen)
	pygame.display.flip()
	i += 1
	fpsClock.tick(fps)

