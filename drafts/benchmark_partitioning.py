import sys
import pygame
import cProfile, pstats, io
from pstats import SortKey
from screen_partition import screen_partition
from pygame.locals import *
from math import floor
from basic import sand_count

pygame.init()

def benchmark(resolution:list, frames, depth):
	width, height = [resolution[0], resolution[1]]
	sand_surface = pygame.Surface((width, height))


	pixels = pygame.surfarray.array3d(sand_surface)
	root_partition = screen_partition(0,0,width,height,pixels, None, depth, min_partition_size=1)
	root_partition.add_sand((int(width/2), int(height/2)),50)

	print(f"resolution: {resolution}\ndepth:{depth}\n")
	pr = cProfile.Profile()
	pr.enable()

	for i in range(frames):
		if i % 10 == 0:
			print(f"{i}/{frames}")
		root_partition.recursive_simulation()

	pr.disable()
	with open(f"benchmarks/res{width}-{height}depth{depth}.txt", "w+") as out_file:
		out_file.writelines([f"\n\nresolution: {resolution}\n", f"max_depth:{depth}\n"])
		ps = pstats.Stats(pr, stream=out_file)
		ps.strip_dirs().sort_stats('tottime').print_stats()

basic_resolution_options = [[100,100], [150,150], [200,200]] 
basic_depth_options = [1,5,10,15,20]

advanced_resolution_options = [[400,400], [800,800]]
advanced_depth_options = [25,30,35,40,50]


# Test benchmark
benchmark([1,1],1,1)
# Basic benchmark
# basic_benchmark = [[resolution, 100, depth] for resolution in basic_resolution_options for depth in basic_depth_options]
for resolution in [[100,100], [150,150], [200,200],[400,400]]:
	for depth in [1,3,5,7,10,15,20,25,30,35]:
		benchmark(resolution, 100, depth)

# Advanced benchmark
		
for resolution in [[400,400], [800,800]]:
	for depth in [1,2,3,4,5,6,7,8,9,10,15,20,25,30,35]:
		benchmark(resolution, 100, depth)
