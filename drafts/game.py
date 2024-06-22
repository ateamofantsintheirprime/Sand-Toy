import sys
import pygame
from basic import add_sand, draw_sand
from draw import step_simulation, threaded_simulation_step
from screen_partition import screen_partition
from pygame.locals import *
from numpy.random import randint

pygame.init()

fps = 100
fpsClock = pygame.time.Clock()
width, height = 200, 200
screen = pygame.display.set_mode((width, height))
 
# Game loop.
sand = [[0 for x in range(width)] for y in range(height)]

# for x in range(0,width, 5):
#     for y in range(0, height,5):
#         print("ball at: ", x, y)
#         balls.append(ball(x,y))
screen.fill((0, 0, 0))
pixels = pygame.surfarray.pixels3d(screen)
root_partition = screen_partition(0,0,width,height)

while True:
    # draw_sand(screen, sand)
    threaded_simulation_step(pixels)
    # break
    # print_pixels(pixels)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            radius = 10
            add_sand(mouse_pos, radius, pixels)

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

  # Update.
  
  # Draw.
  
    pygame.display.flip()
    print(f"fps: {fpsClock.tick(fps)}")
    
print_pixels(pixels)
