import numpy as np
sand_buffers = [np.zeros((5,5)), np.zeros((5,5))]
change_buffers = [np.zeros((5,5)), np.zeros((5,5))]

def simulate_sand():
	# Swap buffers
	print("swapping buffers")
	# sand_buffers.reverse() # dont need to do this because they get matched
	change_buffers.reverse()
	change_buffers[1] = np.zeros((5,5))
	print_all()

	print("matching sand_buffers")
	np.logical_xor(sand_buffers[0], change_buffers[0], out=sand_buffers[0])
	print_all()


	print("simulating sand")
	# Do Simulation
	for x in range(len(sand_buffers[1])):
		for y in range(len(sand_buffers[1][0])):
			if change_buffers[0][x][y]:
				change_buffers[0][x][y] = 0
				try:
					if sand_buffers[0][x][y] and not sand_buffers[0][x][y+1]:
						move_sand(x,y,x,y+1)
						# sand_buffers[1][x][y] = 0
						# sand_buffers[1][x][y+1] = 1
						# change_buffers[1][x][y] = 1
						# change_buffers[1][x][y+1] = 1
				except IndexError:
					continue
	print_all()

def move_sand(x1,y1,x2,y2):
	sand_buffers[1][x1][y1] = 0
	sand_buffers[1][x2][y2] = 1
	change_buffers[1][x1][y1] = 1
	change_buffers[1][x2][y2] = 1

def add_sand(x,y):
	print("adding sand")
	sand_buffers[1][x][y] = 1
	change_buffers[1][x][y] = 1
	print_all()
	
def print_all():
	print("SAND:")
	print(sand_buffers[0])
	print(sand_buffers[1])
	print("CHANGES:")
	print(change_buffers[0])
	print(change_buffers[1])
	print()
	print()

## FRAME 1 ===============
print("NEW FRAME ================================")
# NOTHING
simulate_sand()
## FRAME 2 ===============
print("NEW FRAME ================================")

# ADD SAND
add_sand(2,1)

for i in range(3):
	simulate_sand()
	print("NEW FRAME ====================")

# ADD SAND
add_sand(2,1)


for i in range(3):
	simulate_sand()
	print("NEW FRAME ====================")

add_sand(2,1)


for i in range(3):
	simulate_sand()
	print("NEW FRAME ====================")
