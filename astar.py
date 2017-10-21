import math
import random
from constants import *

import pyglet

class Model:
	def __init__(self):
		self.x = INIT[0]
		self.y = INIT[1]
		self.location = (0,0)
		self.speed = SPEED
		self.pressed_keys = set()
		self.quit_key = pyglet.window.key.Q
		self.world = [[GRASS for row in range(WORLD_DIMENSIONS[0])] for col in range(WORLD_DIMENSIONS[1])]
		self.world[1][0] = WALL
		self.update_path()
		self.previous_location=(0,0)

	def update_map_cell(self, x, y):
		current_tile = self.world[y][x]
		self.world[y][x] = (current_tile+1) % NUM_TILETYPES
		self.update_path()

	def update(self, dt):
		pks = self.pressed_keys
		if self.quit_key in pks:
			exit(0)
		if pyglet.window.key.UP in pks:
			self.y = self.y + self.speed * dt
		if pyglet.window.key.DOWN in pks:
			self.y = self.y - self.speed * dt
		if pyglet.window.key.RIGHT in pks:
			self.x = self.x + self.speed * dt
		if pyglet.window.key.LEFT in pks:
			self.x = self.x - self.speed * dt

		self.location = (math.trunc(self.x / TILE_DIMENSIONS[0]), math.trunc(self.y / TILE_DIMENSIONS[1]))
		if self.location != self.previous_location:
			self.update_path()
			self.previous_location = self.location

	def manhattan_distance(self, point, goal):
		distance = abs(point[0] - goal.x) + abs(point[1]-goal.y)
		return distance

	def neighbours(self, x, y):
		result = []

		n = y-1
		s = y+1
		e = x+1
		w = x-1

		if n > -1 and self.can_walk_here(x, n):
			result.append((x,n))
		if s < len(self.world) and self.can_walk_here(x, s):
			result.append((x,s))
		if e < len(self.world[0]) and self.can_walk_here(e,y):
			result.append((e,y))
		if w > -1 and self.can_walk_here(w,y):
			result.append((w,y))

		return result


	def can_walk_here(self, x, y):
		return self.world[y][x] <=  MAX_WALKABLE_TILE

	# Update the vertices used to draw our shortest path line
	def update_vertices(self):
		previous_vertex = self.location

		vertices = []

		for vertex in self.goal_path:
			vertices.append(previous_vertex[0])
			vertices.append(previous_vertex[1])
			
			vertices.append(vertex[0])
			vertices.append(vertex[1])

			previous_vertex = vertex

		for i in range(len(vertices)):
			vertices[i] = vertices[i]*TILE_DIMENSIONS[0]+int(TILE_DIMENSIONS[0]/2)

		self.vertex_list = pyglet.graphics.vertex_list(int(len(vertices)/2), 
			('v2i', vertices),
			("c3B",(255,0,0)*int(len(vertices)/2)))	

	def update_path(self):
		self.find_path()
		self.update_vertices()

	# Pretty sweet A-star implementation using linked lists
	def find_path(self):
		world_width = WORLD_DIMENSIONS[0]
		world_height = WORLD_DIMENSIONS[1]
		world_size = world_width * world_height

		distance_function = self.manhattan_distance

		# Nodes are stored in the form g, f, x, y, parent
		path_start = MapNode(None, self.location)
		path_end = MapNode(None, GOAL)
		astar = [False for x in range(world_size)]
		open_list = [path_start]
		closed_list = []
		result = []
		current_neighbours = []
		current_node = None
		path_start = None

		length = len(open_list)

		while len(open_list) > 0:
			max_f = world_size
			min_f = -1

			for i in range(length):
				if open_list[i].f < max_f:
					max_f = open_list[i].f
					min_f = i

			# Remove the next node from the list
			current_node = open_list.pop(i)


			# Did we find the destination node?
			if current_node.value == path_end.value:
				closed_list.append(current_node)
				path_start = closed_list[len(closed_list)-1]

				keep_adding = True

				while keep_adding:
					result.append([path_start.x, path_start.y])
					path_start = path_start.parent
					keep_adding = path_start.parent is not None

				# close working arrays

				astar = []
				closed_list =[]
				open_list = []
				result.reverse()

			else:
				# find which nearby neighbours are walkable
				current_neighbours = self.neighbours(current_node.x, current_node.y)

				for i in range(len(current_neighbours)):
					path_start = MapNode(current_node, current_neighbours[i])
					if not astar[path_start.value]:
						# estimated cost of this route so far
						path_start.g = current_node.g + distance_function(current_neighbours[i], current_node)
						# estimated cost of guessed route to destinatino
						path_start.f = path_start.g + distance_function(current_neighbours[i], path_end)
						# remember new path for testing
						open_list.append(path_start)
						astar[path_start.value] = True

				closed_list.append(current_node)

		self.goal_path = result




class View:
	def __init__(self, window, model):
		self.w = window
		self.m = model

		self.goal = pyglet.resource.image("goal.png")
		self.grass = pyglet.resource.image("grass.png")
		self.wall = pyglet.resource.image("wall.png")
		self.player = pyglet.resource.image("character.png")

		self.goal_s = pyglet.sprite.Sprite(self.goal, x=GOAL[0]*TILE_DIMENSIONS[0], y=GOAL[1]*TILE_DIMENSIONS[1])
		self.player_s = pyglet.sprite.Sprite(self.player, x=self.m.x, y=self.m.y)

		self.fps_display = pyglet.clock.ClockDisplay(
			format='%(fps).1f',
			color=(0.5,0.5,0.5,1))

		self.build_sprite_map()

	# Build a sprite map to facilitate batch drawing. Update is triggered on a mouse event.
	# Implementing this gave me a 10x boost in performance
	def build_sprite_map(self):

		self.batch = pyglet.graphics.Batch()
		self.map_tiles = []

		for x in range(WORLD_DIMENSIONS[0]):
			for y in range(WORLD_DIMENSIONS[1]):
				if self.m.world[y][x] == GRASS:
					pos = (x*TILE_DIMENSIONS[0],y*TILE_DIMENSIONS[1])
					self.map_tiles.append(pyglet.sprite.Sprite(self.grass, pos[0], pos[1],batch=self.batch,usage="static"))
				elif self.m.world[y][x] == WALL:
					pos = (x*TILE_DIMENSIONS[0], y*TILE_DIMENSIONS[1])
					self.map_tiles.append(pyglet.sprite.Sprite(self.wall, pos[0], pos[1],batch=self.batch,usage="static"))

	def draw_path(self):
		pyglet.gl.glLineWidth(2)
		self.m.vertex_list.draw(pyglet.gl.GL_LINES)

	def redraw(self):
		self.batch.draw()
		self.player_s.x = self.m.x
		self.player_s.y = self.m.y
		self.player_s.draw()
		self.goal_s.draw()
		self.draw_path()
		self.fps_display.draw()
		

class Controller:
	def __init__(self, model, view):
		self.m = model
		self.v = view

	def on_key_press(self, symbol, modifiers):
		self.m.pressed_keys.add(symbol)

	def on_key_release(self, symbol, modifiers):
		if symbol in self.m.pressed_keys:
			self.m.pressed_keys.remove(symbol)

	def on_mouse_press(self, x, y, button, modifiers):
		x_coord = math.trunc(x / TILE_DIMENSIONS[0])
		y_coord = math.trunc(y / TILE_DIMENSIONS[1])
		self.m.update_map_cell(x_coord, y_coord)
		self.v.build_sprite_map()

	def update(self, dt):
		self.m.update(dt)

# The Window class probably should just be the controller since it already handles event dispatches.
# But what do you people want??! This was a learning exercise. My desire to get shit working
# outweighted my desire to make the architecture as crisp as a freshly-starched shirty,
# Incidentally, if you're into functional programming this thing is side-effect city, population
# me. There's room if you want to emigrate, but I don't think you'll like it.

class Window(pyglet.window.Window):
	def __init__(self, *args, **kwargs):
		dim = (WORLD_DIMENSIONS[0]*TILE_DIMENSIONS[0], WORLD_DIMENSIONS[1]*TILE_DIMENSIONS[1])

		super(Window, self).__init__(
			width=dim[0],
			height=dim[1],
			caption=GAME_CAPTION,
			*args, **kwargs)

		# Set up MVC
		self.model = Model()
		self.view = View(self, self.model)
		self.controller = Controller(self.model, self.view)

		# Game clock
		pyglet.clock.schedule_interval(self.update, 1.0/FPS)
		pyglet.clock.set_fps_limit(FPS)

	def on_key_press(self, symbol, modifiers):
		self.controller.on_key_press(symbol, modifiers)

	def on_key_release(self, symbol, modifiers):
		self.controller.on_key_release(symbol, modifiers)

	def on_mouse_press(self, x,y,button,modifiers):
		self.controller.on_mouse_press(x,y,button,modifiers)

	def update(self, dt):
		self.clear()
		self.controller.update(dt)
		self.view.redraw()

def main():
	pyglet.resource.path = ["resources"]
	pyglet.resource.reindex()

	if debug: print("init window...")
	window = Window()
	if debug: print("done! initi app...")
	pyglet.app.run()

debug = 1

if __name__ == "__main__":
	main()

