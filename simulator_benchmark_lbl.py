import pygame, line_profiler
from sand_simulator import sand_simulator as s_sim
import os

# @line_profiler.profile
def run_simulation(frames):
	for i in range(frames):
		if i % 50 == 0:
			print(f"{i}/{frames}")
		sand_simulator.simulate_sand()


def count_grains(sand_buffer):
	return len(sand_buffer.nonzero()[0])

os.environ["LINE_PROFILE"] = "1"
sand_width, sand_height = 1000, 1000

sand_surface = pygame.Surface((sand_width, sand_height))
sand_simulator = s_sim(sand_width, sand_height)
sand_simulator.paint_sand(500,700, 50)
frames = 300

print("number of grains: ", count_grains(sand_simulator.resulting_sand))

run_simulation(frames)

print("number of grains: ", count_grains(sand_simulator.resulting_sand))

# print(sorted([((x,y),sand_simulator.impassability_checks[x,y]) for (x,y) in zip(*sand_simulator.impassability_checks.nonzero())], key = lambda x: x[1]))

# print(f"AVERAGE FPS: {frames/}")