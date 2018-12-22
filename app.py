import tkinter as tk
from random import randint, shuffle, choice,randrange
import matplotlib.pyplot as plt
import time

SPACE = 0
WALL = 1
basic_operations = 0

MAX_HEIGHT = 50
MAX_WIDTH = 50

####################################################################################

def findStart(maze):
	for ii, i in enumerate(maze):
		for jj, j in enumerate(i):
			if j == 0:
				return tuple([ii, jj])
	return None
	
def findEnd(maze):
	for ii, i in enumerate(maze[::-1]):
		for jj, j in enumerate(i[::-1]):
			if j == 0:
				return tuple([len(i)-(ii+1), len(i)-(jj+1)])
	return None

####################################################################################

def bfs_main(maze):
	start = findStart(maze)
	end = findEnd(maze)
	print(start, end)
	startTime = time.time()
	path = BFS(maze, start, end)
	endTime = time.time()
	
   
	print("Shortest path: ")
	printPath(maze, path, start, end)
	print(path)

	print("Time taken:", endTime-startTime, "secs")
	print("Basic operations: ", basic_operations)
	print("\n")

def BFS(maze, start, end):
	queue = [start]
	visited = set()
	while len(queue) != 0:
		if queue[0] == start:
			path = [queue.pop(0)] 
		else:
			path = queue.pop(0)
		front = path[-1]
		if front == end:
			return path
		elif front not in visited:
			l = getAdjacentSpaces(maze, front, visited)
			#print(l)
			for adjacentSpace in l:
				newPath = list(path)
				newPath.append(adjacentSpace)
				queue.append(newPath)
				global basic_operations
				basic_operations += 1
			visited.add(front)
	return path


def getAdjacentSpaces(maze, space, visited):
	spaces = list()
	spaces.append((space[0]-1, space[1]))  # Up
	spaces.append((space[0]+1, space[1]))  # Down
	spaces.append((space[0], space[1]-1))  # Left
	spaces.append((space[0], space[1]+1))  # Right

	s = list()
	for i in spaces:
		if i[0] < -50 or i[1] < -50 or i[0]>49 or i[1]>49:
			continue
		s.append(i)
	final = list()
	for i in s:
		if (maze[i[0]][i[1]] != 1) and (i not in visited) :
			final.append(i)
	return final
	
def printPath(maze, path, start, end):
	maze[end[0]][end[1]] = 0.5
	for i in path:
		maze[i[0]][i[1]] = 0.5
	plotfig(maze, "MAZE GENERATION AND SOLVING")      

##################################################################################

def plotfig(image, name):
	plt.figure(figsize=(15, 15))
	plt.imshow(image, cmap=plt.cm.binary, interpolation='nearest')
	plt.xticks([]) 
	plt.yticks([])
	plt.title(name)
	plt.show()

#################################################################################

def prim_maze( option, width=MAX_WIDTH, height=MAX_HEIGHT, complexity=1, density=1):
	shape = (height+1, width+1)
	complexity = int(complexity * (10 * (shape[0] + shape[1]))) #number of components
	density    = int(density * (shape[0]//2) * (shape[1]//2)) #size of components
	
	img = [[0 for i in range(shape[1])] for j in range(shape[0])]
	#img[0, :] = img[-1, :] = img[:, 0] = img[:, -1] = 1
	for i in range(density):
		x, y = randint(0, shape[1]//2)*2, randint(0, shape[0]//2)*2 
		img[y][x] = 1
		for j in range(complexity):
			neighbours = []
			if x > 1:
				neighbours.append((y, x-2))
			if x < shape[1] - 2:
				neighbours.append((y, x+2))
			if y > 1:
				neighbours.append((y-2, x))
			if y < shape[0] - 2:
				neighbours.append((y+2, x))
			if len(neighbours):
				y_hat,x_hat = neighbours[randint(0, len(neighbours) - 1)]
				if img[y_hat][x_hat] == 0:
					img[y_hat][x_hat] = 1
					img[y_hat + (y - y_hat)//2][x_hat + (x - x_hat)//2] = 1
					x, y = x_hat, y_hat
	if option==1:
		bfs_main(img)
	else:
		a_star_main(img)

	#plotfig(img, "Prims-Algorithm for Maze generation")

####################################################################################

def dfs_maze(option,height=MAX_HEIGHT, width=MAX_WIDTH ):
	mx = height #rows
	my = width #columns

	img = [[0 for i in range(my)] for j in range(mx)]
	dx = [0, 1, 0, -1]
	dy = [-1, 0, 1, 0]
	color = [(0,0,0),(255,255,255)]
	#img[0, :] = img[-1, :] = img[:, 0] = img[:, -1] = 1
	stack = [(randint(0, mx-1), randint(0, my-1))]

	while len(stack)>0:
		(cx,cy) = stack[-1]
		img[cy][cx] = 1
		neighbors = []
		for i in range(4):
			nx = cx + dx[i]
			ny = cy + dy[i]
			if nx >= 0 and nx < mx and ny >= 0 and ny < my:
				if img[ny][nx] == 0:
					ctr = 0
					for j in range(4):
						ex = nx + dx[j]
						ey = ny + dy[j]
						if ex >=0 and ex < mx and ey >= 0 and ey < my:
							if img[ey][ex] == 1:
								ctr += 1
					if ctr == 1:
						neighbors.append(i)
		
		if len(neighbors) > 0:
			ir = neighbors[randint(0, len(neighbors) - 1)]
			cx += dx[ir]
			cy += dy[ir]
			stack.append((cx, cy))
		else: 
			stack.pop()
	if option==1:		
		bfs_main(img)
	else:
		a_star_main(img)
	#plotfig(img, "DFS-Backtracking for Maze Algorithm") 

############################################################################################	

def convert(op, maze):
	pretty_maze = [[1]*(2*len(maze[0])+1) for a in range(2*len(maze)+1)]
	for y,row in enumerate(maze):
		for x,col in enumerate(row):
			pretty_maze[2*y+1][2*x+1] = 0
			for direction in col:
				pretty_maze[2*y+1+direction[0]][2*x+1+direction[1]] = 0
	if op==1:
		bfs_main(pretty_maze)
	else:
		a_star_main(pretty_maze)
	#plotfig(pretty_maze, "Ellers")


def ellers_maze(option, width=MAX_WIDTH, height=MAX_HEIGHT):
	maze = [[[] for b in range(width)] for a in range(height)]
	sets = list(range(len(maze[0])))
	for y, row in enumerate(maze):
		for x, col in enumerate(row[:-1]):
			if ((row == maze[-1] or randint(0,1)) and sets[x] != sets[x+1]):
				sets[x+1] = sets[x]
				maze[y][x].append((0,1))
				maze[y][x+1].append((0,-1))
		if row != maze[-1]:
			next_sets = list(range(y*len(maze[0]), (y+1)*len(maze[0])))
			all_sets = set(sets)
			have_moved = set()
			while all_sets != have_moved:
				for x, col in enumerate(row):
					if randint(0,1) and sets[x] not in have_moved:
						have_moved.add(sets[x])
						next_sets[x] = sets[x]
						maze[y][x].append((1,0))
						maze[y+1][x].append((-1,0))
			sets = next_sets
	convert(option, maze)


#######################################################################################


def create_empty_grid(width, height, default_value=SPACE):
	grid = []
	for row in range(height):
		grid.append([])
		for column in range(width):
			grid[row].append(default_value)
	return grid


def create_outside_walls(maze):
	for row in range(len(maze)):
		maze[row][0] = WALL
		maze[row][len(maze[row])-1] = WALL

	for column in range(1, len(maze[0]) - 1):
		maze[0][column] = WALL
		maze[len(maze) - 1][column] = WALL
	return maze


def make_maze_recursive_call(maze, top, bottom, left, right):
	# Figure out where to divide horizontally
	start_range = bottom + 2
	end_range = top - 1
	y = randrange(start_range, end_range, 2)

	# Do the division
	for column in range(left + 1, right):
		maze[y][column] = WALL

	# Figure out where to divide vertically
	start_range = left + 2
	end_range = right - 1
	x = randrange(start_range, end_range, 2)

	# Do the division
	for row in range(bottom + 1, top):
		maze[row][x] = WALL

	# Now we'll make a gap on 3 of the 4 walls.
	# Figure out which wall does NOT get a gap.
	wall = randrange(4)
	if wall != 0:
		gap = randrange(left + 1, x, 2)
		maze[y][gap] = SPACE

	if wall != 1:
		gap = randrange(x + 1, right, 2)
		maze[y][gap] = SPACE

	if wall != 2:
		gap = randrange(bottom + 1, y, 2)
		maze[gap][x] = SPACE

	if wall != 3:
		gap = randrange(y + 1, top, 2)
		maze[gap][x] = SPACE

	# If there's enough space, to a recursive call.
	if top > y + 3 and x > left + 3:
		make_maze_recursive_call(maze, top, y, left, x)

	if top > y + 3 and x + 3 < right:
		make_maze_recursive_call(maze, top, y, x, right)

	if bottom + 3 < y and x + 3 < right:
		make_maze_recursive_call(maze, y, bottom, x, right)

	if bottom + 3 < y and x > left + 3:
		make_maze_recursive_call(maze, y, bottom, left, x)


def recursive_div_maze(option, maze_width=MAX_WIDTH, maze_height=MAX_HEIGHT):
	
	maze = create_empty_grid(maze_width, maze_height)
	# Fill in the outside walls
	maze = create_outside_walls(maze)

	# Start the recursive process
	make_maze_recursive_call(maze, maze_height - 1, 0, 0, maze_width - 1)
	if option==1:
		bfs_main(maze)
	else:
		a_star_main(maze)
	#plotfig(maze, "Recursive Division")

####################################################################################


root = tk.Tk()
frame = tk.Frame(root)
frame.pack()

button0 = tk.Button(frame, text="QUIT", fg="red",command=quit)
button0.pack(side=tk.BOTTOM)
button1 = tk.Button(frame,text="Backtracking, BFS",command=lambda: dfs_maze(1))
button1.pack(side=tk.BOTTOM)
button2 = tk.Button(frame,text="Prim, BFS",command=lambda: prim_maze(1))
button2.pack(side=tk.BOTTOM)
button3 = tk.Button(frame,text="Ellers, BFS",command=lambda: ellers_maze(1))
button3.pack(side=tk.BOTTOM)
button4 = tk.Button(frame,text="Recursive Division, BFS",command=lambda: recursive_div_maze(1))
button4.pack(side=tk.BOTTOM)
button5 = tk.Button(frame,text="Backtracking, A*",command=lambda: dfs_maze(2))
button5.pack(side=tk.BOTTOM)
button6 = tk.Button(frame,text="Prim, A*",command=lambda: prim_maze(2))
button6.pack(side=tk.BOTTOM)
button7 = tk.Button(frame,text="Ellers, A*",command=lambda: ellers_maze(2))
button7.pack(side=tk.BOTTOM)
button8 = tk.Button(frame,text="Recursive Division, A*",command=lambda: recursive_div_maze(2))
button8.pack(side=tk.BOTTOM)

root.mainloop()