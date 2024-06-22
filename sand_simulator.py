from numpy import ndarray, logical_xor, zeros, copy, logical_or
from random import shuffle, getrandbits
import line_profiler, os
from copy import deepcopy

# os.environ["LINE_PROFILE"] = "1"


class sand_simulator():
	def __init__(self, width:int, height:int):
		self.width:int = width
		self.height:int = height
		assert width > 3
		assert height > 3

		self.initial_sand = zeros((width, height), dtype=bool)
		self.resulting_sand = zeros((width, height), dtype=bool)

		self.simple_prompts:list[set] = [set(),set()]
		self.complex_prompts:list[set] = [set(),set()]
		self.wall = zeros((width, height), dtype=bool)

	def count_grains(self):
		return len(self.resulting_sand.nonzero()[0])

		
	def add_grain(self,x:int,y:int):
		self.resulting_sand[x][y] = 1
		# self.add_complex_prompt(x,y)
		self.complex_prompts[1].add((x,y))

	# @line_profiler.profile
	def simulate_sand(self):

		self.initial_sand = deepcopy(self.resulting_sand)
		self.simple_prompts.reverse()
		self.complex_prompts.reverse()
		self.simple_prompts[1].clear()
		self.complex_prompts[1].clear()

		for (x,y) in self.simple_prompts[0]:
			self.simulate_grain(x,y)
		slicing = 17 # This makes the results look random
		for i in range(slicing):
			for (x,y) in list(self.complex_prompts[0])[i::slicing]:
				self.simulate_grain(x,y)

		# for (x,y) in self.complex_prompts[0]:
		# 	self.simulate_grain(x,y)

	def add_complex_prompt(self,x,y):
		if self.initial_sand[x,y] and self.resulting_sand[x,y]:
			# assert self.initial_sand[x][y]==1
			if not (x,y) in self.simple_prompts[1]:
			# 	self.complex_prompts[1].add((x,y))
				self.complex_prompts[1].add((x,y))

	def add_simple_prompt(self,x,y):
		if self.initial_sand[x,y] and self.resulting_sand[x,y]:
			# assert self.initial_sand[x][y]==1
			# try:
			# 	self.complex_prompts[1].remove((x,y))
			# 	self.simple_prompts[1].add((x,y))
			# except KeyError:
			# 	self.simple_prompts[1].add((x,y))
			if not (x,y) in self.complex_prompts[1]:
				self.simple_prompts[1].add((x,y))

	def fall_down(self,x1,y1,x2,y2):
		self.move_grain(x1,y1,x2,y2)

	# @line_profiler.profile
	def move_grain(self,x1:int,y1:int,x2:int,y2:int):
				
		self.initial_sand[x1][y1] = 0
		self.resulting_sand[x1][y1] = 0
		self.resulting_sand[x2][y2] = 1

		if y2+1 < self.height:
			self.complex_prompts[1].add((x2,y2))
		if y1 - 1 >= 0:
			if self.initial_sand[x1,y1-1] and self.resulting_sand[x1,y1-1]:
				self.simple_prompts[1].add((x1,y1-1))
			if x1 - 1 >= 0 and self.initial_sand[x1-1][y1-1] and self.resulting_sand[x1-1,y1-1]:
				self.complex_prompts[1].add((x1-1,y1-1))
			if x1 + 1 < self.width and self.initial_sand[x1+1][y1-1] and self.resulting_sand[x1+1][y1-1]:
				self.complex_prompts[1].add((x1+1,y1-1))

	def print_buffer(self,buff):
		print("\t"+", ".join([str(i) for i in list(range(len(buff[0])))]))
		for y in range(len(buff)):
			print(y,":\t", end='')
			for x in range(len(buff)):
				print(int(buff[x][y])," ", end='')
			print()
		print()

	@line_profiler.profile
	def simulate_grain(self,x:int,y:int):
		if not self.initial_sand[x][y] or self.wall[x][y]:
			# No change needed! already been addressed 
			return
		elif self.resulting_sand[x][y+1]==0 and self.wall[x][y+1]==0:
			self.move_grain(x,y,x,y+1)
		elif x-1 < 0:
			if self.resulting_sand[x+1][y+1] == 0 and self.wall[x+1][y+1]==0:
				self.move_grain(x,y,x+1,y+1)
		elif x+1 >= self.width:
			if self.resulting_sand[x-1][y+1] == 0 and self.wall[x-1][y+1]==0:
				self.move_grain(x,y,x-1,y+1)
		elif self.resulting_sand[x-1][y+1]==1 or self.wall[x-1][y+1]==1:
			if self.resulting_sand[x+1][y+1]==0 and self.wall[x+1][y+1]==0:
				self.move_grain(x,y,x+1,y+1)
			return
		elif self.resulting_sand[x+1][y+1]==1 or self.wall[x+1][y+1]==1:
			self.move_grain(x,y,x-1,y+1)
		elif bool(getrandbits(1)):
			self.move_grain(x,y,x-1,y+1)
		else:
			self.move_grain(x,y,x+1,y+1)

	def remove_wall_cell(self, x:int, y:int):
		self.wall[x][y] = 0
		self.complex_prompts[1].add((x,y))
		if y > 0:
			self.simple_prompts[1].add((x,y-1))
			if x > 0:
				self.complex_prompts[1].add((x-1,y-1))
			if x < self.width-1:
				self.complex_prompts[1].add((x+1,y-1))


	def edit_wall(self,add_remove:int,x:int,y:int,size:int=0):
		if size == 0:
			
			self.wall[x][y] = add_remove
			if add_remove == 0:
				self.remove_wall_cell(x,y)
		else:
			for x_ in range(max(x-size//2, 0), min(x+size//2, self.width)):
				for y_ in range(max(y-size//2, 0), min(y+size//2, self.height)):
					# print(f"changing wall {add_remove}")
					self.wall[x_][y_] = add_remove
					if add_remove == 0:
						self.remove_wall_cell(x_,y_)

	def paint_sand(self,x:int,y:int,radius:int=0):
		if radius == 0:
			self.add_grain(x,y)
		else:
			for y_offset in range(-min(radius,y), radius):
				for x_offset in range(-min(radius,x), radius):
					if pow(y_offset,2) + pow(x_offset,2) > pow(radius,2):
						continue
					try:
						# ###print(f"adding sand to {[x+x_offset,y+y_offset]}")
						# self.buffers[1][x+x_offset][y+y_offset] = 1
						self.add_grain(x+x_offset,y+y_offset)
					except IndexError:
						continue