import pygame, cProfile, pstats, io, os
from sand_simulator import sand_simulator as s_sim
os.environ["LINE_PROFILE"] = "0"

sand_width, sand_height = 200, 200

sand_surface = pygame.Surface((sand_width, sand_height))
sand_simulator = s_sim(sand_width, sand_height)
sand_simulator.paint_sand(100,100, 50)
frames = 300

print("number of grains: ", sand_simulator.count_grains())


pr = cProfile.Profile()
pr.enable()

for i in range(frames):
	if i % 50 == 0:
		print(f"{i}/{frames}")
	sand_simulator.simulate_sand()

pr.disable()
s = io.StringIO()
ps = pstats.Stats(pr, stream=s)
# sortby = SortKey.CUMULATIVE
sortby = 'tottime'
ps = pstats.Stats(pr, stream=s)
ps.strip_dirs().sort_stats(sortby).print_stats()

ps.strip_dirs().sort_stats(sortby).print_callers()

print(s.getvalue())
print("number of grains: ", sand_simulator.count_grains())

