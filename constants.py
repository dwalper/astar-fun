GRASS = 0
WALL = 1
NUM_TILETYPES = 2
MAX_WALKABLE_TILE = 0
WORLD_DIMENSIONS = (20,20)
TILE_DIMENSIONS = (64,64)
INIT = (0,0)
GOAL = (WORLD_DIMENSIONS[0]-1, WORLD_DIMENSIONS[1]-1)
FPS = 75.0
GAME_CAPTION = "A* pathfinding tomfoolery"
SPEED = 150

class MapNode():
	def __init__(self,parent,point):
		self.parent = parent
		self.value = point[0] + (point[1]*WORLD_DIMENSIONS[0])
		self.x = point[0]
		self.y = point[1]
		self.f = 0
		self.g = 0