# Author : Rohan Nirmal
# This is an Pathfinding Visulization Tool in python
# it is recommended to use Pygame library but i have used tkinter(not best with animations)

from tkinter import *
from random import *
import time
import math
from queue import PriorityQueue
root = Tk()
root.title('Pathfinder')
root.resizable(0,0)
root.geometry('600x600')
Heading = Label(root,text="Pathfinder",font=("Arial Black",30),fg="#ffca42",bg="black")
Heading.pack()
instruction = Label(root,text="Note : Tap of the screen to select the start and end node",font=("Arial Black",12),fg="#e342ff",bg="black")
instruction.pack()

canvas  = Canvas(root,height=400, width=400)
root.configure(background='Black')
canvas.pack()


frame1 = Frame(root)
frame1.pack()

width = 400
height = 400
n  = 10

# create the states for grid
grid = []
w,h  = width/n,height/n
offset = n/10
size = w
global stat
stat = 0

class Node():
	def __init__(self,x1,y1,x2,y2,color):
		self.g = 0
		self.h = 0
		self.f = 0
		self.x1 = x1
		self.y1 = y1
		self.x2 = x2
		self.y2 = y2
		self.color = color
		self.desg = 'blank'
		self.id = 0
		self.nbrs = []
		self.row = int(self.x1/(400/n))
		self.col = int((self.y2-(400/n))/(400/n))
		
	def show(self):
		self.id  = canvas.create_rectangle(self.x1-1,self.y1-1,self.x2+1,self.y2+1,fill=self.color) #(x1,y1,x2,y2)
		
	def upnbrs(self):
		self.nbrs = []
		x,y = self.row,self.col
		if x < n-1 and  grid[x+1][y].desg != 'Wall':
			self.nbrs.append(grid[x+1][y] ) #Below
		if x > 0 and  grid[x-1][y].desg != 'Wall':
			self.nbrs.append(grid[x-1][y] ) #Above
		if y > 0 and  grid[x][y-1].desg != 'Wall':
			self.nbrs.append(grid[x][y-1] ) #Left
		if y < n-1 and  grid[x][y+1].desg != 'Wall':
			self.nbrs.append(grid[x][y+1] ) #Right
		print()
		
def mingscore(openset):
	min = openset[0]
	for i in openset:
		if i.g < min.g:
			min = i
	return min

def hue(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(camefrom, current):
	while current in camefrom:
		current = camefrom[current]
		print(current.row,current.col)
		current.color = "red"
		draw()
		#time.sleep(0.01)
	root.update()



def astar(start,goal):
	endpoints()
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	camefrom = {}

	g_score = {node: float("inf") for row in grid for node in row}
	g_score[start] = 0

	f_score = {node: float("inf") for row in grid for node in row}
	f_score[start] = hue((start.row,start.col),(goal.row,goal.col))
	open_set_hash = {start}

	while not open_set.empty():
		current = open_set.get()[2]
		open_set_hash.remove(current)

		#current =  mingscore(openset)
		#openset.remove(current)


		if current == goal:
			goal.color = 'red'
			return reconstruct_path(camefrom, current)
			print('reached goal')
			#print(goal.row,goal.col)
		
		for neighbor in current.nbrs :
			tentative_gScore = g_score[current] + 1
			if tentative_gScore < g_score[neighbor]:
				camefrom[neighbor] = current
				g_score[neighbor] = tentative_gScore
				f_score[neighbor] = g_score[neighbor] + hue((neighbor.row,neighbor.col),(goal.row,goal.col))
				
				if neighbor not in open_set_hash :
					count+=1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.color = "green"
			
			
					
		draw()
		#time.sleep(0.01)
		#root.update()
		if current != start:
			current.color = "yellow"
		
	return -1
 

def endpoints():
	start.color = 'blue'
	goal.color = 'pink'
	draw()
	root.update()
	


def draw():
	for i in range(n):
		for j in range(n):
			grid[i][j].show()
			#time.sleep(0.1)
	root.update()
			#print(grid[i][j].desg)
			
def update_nbr():
	for i in range(n):
		for j in range(n):
			grid[i][j].upnbrs()

def trav():
	val = [0,0]
	while (val[0] != n and val[1] != n):
		if grid[val[0]][val[1]].desg != 'Wall': 
			grid[val[0]][val[1]].color = 'red'
			val[0] += 1
			val[1] += 1
		
		draw()
		time.sleep(0.1)
		root.update()
	print("Reached the End")



def obstacles():
	reset()
	for i in range(n):
		for j in range(n):
			if uniform(0,1) < 0.2:
				grid[i][j].color = 'grey'
				grid[i][j].desg = 'Wall'
	draw()
	update_nbr()


def reset():
	global stat
	stat = 0
	for i in range(n):
		for j in range(n):
			grid[i][j].color = 'White'
			grid[i][j].desg = 'blank'
	draw()

	



#colour = ['red','blue','green','orange','pink','grey','brown','yellow']
# making grid of nodes
for i in range(n):
	grid.append([])
	for j in range(n):
		x1, y1 , x2, y2 = i*w+offset , j*h+offset , size+i*w , size+j*h
		node = Node(x1, y1 , x2, y2,'white')
		grid[i].append(node)
		#node.show()

# event mouse click function to get the start and end node from user
def click(event):
	global stat,start,goal
	pos = (canvas.coords(CURRENT)) #mouse pointer in the canvas
	r = int(pos[0]/(400/n))
	c = int((pos[1])/(400/n))
	print(r,c)
	#increasing stat as start and node selected 
	if stat <2:
		if stat == 0:
			start = grid[r][c]
			start.color = "blue"
			draw()
			root.update()
		else:
			goal = grid[r][c]
			goal.color = "pink"
			draw()
			root.update()
	stat+=1

global start,goal
start = grid[0][0]
goal = grid[n-1][n-1]

canvas.bind_all("<Button-1>",click)

button = Button(frame1,padx=20,pady=20,text='A*',command=lambda:astar(start,goal))
button1 = Button(frame1,padx=20,pady=20,text='Obstacles',command=obstacles)
button2 = Button(frame1,padx=20,pady=20,text='Reset',command=reset)

button.pack(side = LEFT)
button1.pack(side = LEFT)
button2.pack(side =LEFT)
draw()
update_nbr()
root.mainloop()