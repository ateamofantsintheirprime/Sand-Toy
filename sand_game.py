import sys, pygame
# import cProfile, pstats, io
# from pstats import SortKey
from sand_simulator import sand_simulator as s_sim
from draw_sand import draw_sand
from pygame.locals import *
from math import floor

pygame.init()
pygame.display.set_caption("Ants' Sand Toy")

icon_image = pygame.Surface((32,32))
pygame.draw.rect(icon_image, (255,255,255,255), pygame.Rect(10,10,12,12))
# icon_image.draw_rect
# icon_image = pygame.image.load('icon.png')
pygame.display.set_icon(icon_image)

fps = 120
fpsClock = pygame.time.Clock()
width, height = 1200, 800
screen = pygame.display.set_mode((width, height), depth=10)
sand_width, sand_height = 300,200
sand_surface = pygame.Surface((sand_width, sand_height))
sand_simulator = s_sim(sand_width, sand_height)
# pr = cProfile.Profile()
# pr.enable()

i = 0
while True:
	# print(f"starting frame {i}")
	# if i > 300:
	# 	break

	# Process I/O
	if any(pygame.mouse.get_pressed()):
		mouse_pos = list(pygame.mouse.get_pos())
		x = int(floor(mouse_pos[0] * sand_width/width))
		y = int(floor(mouse_pos[1] * sand_height/height))
		size = 3
		if pygame.key.get_pressed()[K_LSHIFT] == True:
			sand_simulator.edit_wall(0,x,y, size)
		elif pygame.key.get_pressed()[K_SPACE] == True:
			sand_simulator.edit_wall(1,x,y, size)
		else:
			sand_simulator.paint_sand(x,y, size)

	for event in pygame.event.get():

		if event.type == QUIT:
			pygame.quit()
			sys.exit()
  
	sand_simulator.simulate_sand()

  # Draw.

	draw_sand(sand_simulator.resulting_sand, sand_simulator.wall, screen, sand_surface)
	pygame.display.flip()
	i += 1
	fpsClock.tick(fps)
	# if i % 10 == 0:
	# 	print(f'fps: {fpsClock.get_fps()}')
# pr.disable()
# s = io.StringIO()
# ps = pstats.Stats(pr, stream=s)
# # sortby = SortKey.CUMULATIVE
# sortby = 'tottime'
# ps = pstats.Stats(pr, stream=s)
# ps.strip_dirs().sort_stats(sortby).print_stats()

# ps.strip_dirs().sort_stats(sortby).print_callers()

# print(s.getvalue())
