import numpy
import itertools
# Experiment

starting_sand = numpy.random.randint(0,2,(50,50))
result_sand = numpy.zeros((50,50))
updated = numpy.zeros((50,50))

# Perfect simulation, just slow

for (x,y) in itertools.product(list(range(500)),list(range(500))):
	if y +1 <= 499:
		if starting_sand[x][y] and not starting_sand[x][y+1]:
			result_sand[x][y] = 0 # not needed technically
			result_sand[x][y+1] = 1
			updated[x][y] = 1
			updated[x][y+1] = 1
