import pygame
from numpy import where

def draw_sand(sand, walls, screen, sand_surface):
	walls = where(walls == 1, 12701133, 0) # 'azure3'
	walls = walls - sand
	pygame.surfarray.blit_array(surface=sand_surface, array=walls)
	pygame.transform.scale(surface=sand_surface, size=screen.get_size(), dest_surface=screen)

