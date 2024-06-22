import random
import pygame
from math import floor
from basic import print_pixels

# self.max_depth = 10
# self.min_partition_size = 20

## NOTE TO SELF: if both my children are base simulations, just unpartition and run the base simulation myself
## 

# Make it so that the screen partition takes in a 2d array of booleans
# and when being drawn it has a special function

class screen_partition():
	def __init__(self, x1,y1,x2,y2, pixels, parent, max_depth, min_partition_size, depth=0):
		self.x=x1
		self.y=y1
		self.x1=x1
		self.y1=y1
		self.x2=x2
		self.y2=y2

		self.width=x2-x1
		self.height=y2-y1

		self.parent: screen_partition = parent

		self.pixels = pixels # store a reference, not a copy plz!!

		self.child1: screen_partition = None
		self.child2: screen_partition = None
		self.contains_base_simulation = False
		self.depth = depth
		self.max_depth = max_depth
		self.min_partition_size = min_partition_size

	def unpartition(self):
		self.child1 = None
		self.child2 = None

	def partition(self):
		if self.width > self.height:
			# split horizontally
			half_width = int(floor(self.width/2)) # Notice that it's rounded down. half_width - (self.width - half_width) = 1
			child1_x1 = self.x1
			child1_y1 = self.y1
			child1_x2 = self.x1 + half_width
			child1_y2 = self.y2

			child2_x1 = child1_x2
			child2_y1 = self.y1
			child2_x2 = self.x2
			child2_y2 = self.y2
			# child1_info = [child1_x1, child1_y1, child1_x2, child1_y2, self.pixels, self, self.depth+1]
			# child2_info = [child2_x1, child2_y1, child2_x2, child2_y2, self.pixels, self, self.depth+1]
		else:
			# split vertically
			half_height = int(floor(self.height/2))
			child1_x1 = self.x1
			child1_y1 = self.y1
			child1_x2 = self.x2
			child1_y2 = self.y1 + half_height

			child2_x1 = self.x1
			child2_y1 = child1_y2
			child2_x2 = self.x2
			child2_y2 = self.y2
		
		child1_info = [child1_x1, child1_y1, child1_x2, child1_y2, self.pixels, self, self.max_depth, self.min_partition_size, self.depth+1]
		child2_info = [child2_x1, child2_y1, child2_x2, child2_y2, self.pixels, self, self.max_depth, self.min_partition_size, self.depth+1]
		
		self.child1 = screen_partition(*child1_info)
		self.child2 = screen_partition(*child2_info)

	def base_simulation(self):
		coords = [(x,y) for x in range(self.x, self.x+self.width) for y in range(self.y, self.y+self.height)]
		coords.reverse()
		# random.shuffle(coords)
		self.contains_base_simulation = False
		# self.did_base_simulation = False
		for x,y in coords:
			if any(self.pixels[x][y]):
				self.simulate_grain(x,y)

	def adjacent_to_bounds(self,x,y):
		if x >= self.x -1 and x < self.x + self.width + 1:
			if y>= self.y -1 and y < self.y + self.height + 1:
				return True
		return False
	
	def within_bounds(self,x,y):
		if x >= self.x and x < self.x + self.width:
			if y>= self.y and y < self.y + self.height:
				return True
		return False
	
	def draw(self, screen):
		dims = screen.get_size()
		x = 	int(round(self.x 		* dims[0] / len(self.pixels)))
		width = int(round(self.width 	* dims[0] / len(self.pixels)))
		y = 	int(round(self.y 		* dims[1] / len(self.pixels[1])))
		height= int(round(self.height 	* dims[1] / len(self.pixels[1])))
		

		# colour = (255,0,0)
		# # # # 		# if self.contains_base_simulation:
		# 	intensity = int(round(255*self.depth/MAX_DEPTH))
		# 	colour = (255-intensity,0,255)
		# 	# colour = (255,255,0)
		if self.contains_base_simulation and self.is_leaf():
			colour = (0,255,0)
			pygame.draw.rect(screen, colour, pygame.Rect(x,y,width,height), width=1)
		if not self.is_leaf():
			self.child1.draw(screen)
			self.child2.draw(screen)

	def is_leaf(self):
		return self.child1 == None and self.child2 == None

	def partitionable(self):
		return self.depth < self.max_depth and (self.width > self.min_partition_size or self.height > self.min_partition_size)		

	def prompt(self, x, y):
		try:
			if not any(self.pixels[x][y]):
				return
		except IndexError:
			return
		
		if not self.within_bounds(x,y):
			if self.parent != None:
				self.parent.prompt(x,y)
		else:
			if not self.is_leaf() and self.child1.within_bounds(x,y) and self.child2.within_bounds(x,y):
				raise Exception
			if self.is_leaf():
				if not self.contains_base_simulation:
					self.contains_base_simulation = True
			else:
				if self.child1.within_bounds(x,y):
					self.child1.prompt(x,y)
				if self.child2.within_bounds(x,y):
					self.child2.prompt(x,y)

	def recursive_edit(self, on_off, x, y):
		if not self.within_bounds(x,y):
			if self.parent != None:
				self.parent.recursive_edit(on_off,x,y)
			return
			# This may be dangerous

		self.contains_base_simulation = True
		# If i'm a leaf and i can be partitioned then partition
		if self.is_leaf() and self.partitionable():
			self.partition()

		# I either am a leaf node and am non-partitionable
		# or i'm partitioned
		if self.is_leaf():
			# Do base sim
			self.pixels[x][y]= [255*on_off,255*on_off,255*on_off]
			# self.did_base_simulation = True
			self.contains_base_simulation = True
			self.prompt(x-1,y)
			self.prompt(x+1,y)
			self.prompt(x-1,y-1)
			self.prompt(x,y-1)
			self.prompt(x+1,y-1)
		else:
			# just recurse
			if self.child1.within_bounds(x,y):
				self.child1.recursive_edit(on_off,x,y)
			elif self.child2.within_bounds(x,y):
				self.child2.recursive_edit(on_off, x, y)

	# def clear_did_base_sim(self):
	# 	self.did_base_simulation = False 
	# 	if not self.is_leaf():
	# 		self.child1.clear_did_base_sim()
	# 		self.child2.clear_did_base_sim()

	def recursive_simulation(self):
		if self.contains_base_simulation:
			if self.is_leaf():
				self.base_simulation()
			else:
				# print("ch1")
				# print(self.child1.x1, self.child1.y1, self.child1.x2, self.child1.y2)
				# print("ch2")
				# print(self.child2.x1, self.child2.y1, self.child2.x2, self.child2.y2)
				self.child1.recursive_simulation()
				self.child2.recursive_simulation()
		
		if not self.is_leaf():
			if self.child1.contains_base_simulation or self.child2.contains_base_simulation:
				self.contains_base_simulation = True
			else:
				self.unpartition()
				self.contains_base_simulation = False
				# unpartition

	def move_sand(self, dest, src):
		# print(f"partition: ({self.x1},{self.y1}):({self.x2},{self.y2})")
		# print(f"moving {src} to {dest}")
		# print_pixels(self.pixels)
		self.recursive_edit(0, src[0], src[1])
		self.recursive_edit(1, dest[0], dest[1])
		# print("after move:")
		# print_pixels(self.pixels)

	def add_sand(self, mouse_pos, radius):
		mouse_x = mouse_pos[0]
		mouse_y = mouse_pos[1]
		for y_offset in range(-radius, radius):
			for x_offset in range(-radius, radius):
				x = mouse_x+x_offset
				y = mouse_y+y_offset
				if y < 0 or y >= len(self.pixels[0]):
					continue
				if x < 0 or x >= len(self.pixels):
					continue
				if pow(y_offset,2) + pow(x_offset,2) > pow(radius,2):
					continue
				print("adding sand...")
				self.recursive_edit(1, x,y)


	def simulate_grain(self,x,y):
		if not any(self.pixels[x][y]):
			return
		left, right, below, bottom_right, bottom_left= 0,0,0,0,0

		if y+1 >= len(self.pixels[0]):
			below=1
			bottom_left=1
			bottom_right=1
		else:
			if self.pixels[x][y+1][0]:
				below = 1
			if x+1 >= len(self.pixels) or self.pixels[x+1][y+1][0]:
				bottom_right = 1
			if x-1 < 0 or self.pixels[x-1][y+1][0]:
				bottom_left = 1
		if x+1 >= len(self.pixels) or self.pixels[x+1][y][0]:
			right = 1
		if x-1 < 0 or self.pixels[x-1][y][0]:
			left = 1
		
		if not below:
			self.move_sand((x,y+1), (x,y))
			return
		if (bottom_left or left) and (bottom_right or right):
			#draw_sand(1,x,y,self.pixels)
			return
		if not (left or right or bottom_left or bottom_right):
			# There is no direction of flow we can garner
			left_over_right = y%2
			if left_over_right:
				self.move_sand((x-1,y+1), (x,y))
				# draw_sand(0,x,y,self.pixels)
				# draw_sand(1,x-1,y+1,self.pixels)
			else:
				self.move_sand((x+1,y+1), (x,y))
				# draw_sand(0,x,y,self.pixels)
				# draw_sand(1,x+1,y+1,self.pixels)
			return
		if not bottom_left and not left:
			# nothing on the left => something on the right
			self.move_sand((x-1,y+1), (x,y))
			# draw_sand(0,x,y,self.pixels)
			# draw_sand(1,x-1,y+1,self.pixels)
			return
		else:
			# something on the left => nothing on the right
			self.move_sand((x+1,y+1), (x,y))
			# draw_sand(0,x,y,self.pixels)
			# draw_sand(1,x+1,y+1,self.pixels)
