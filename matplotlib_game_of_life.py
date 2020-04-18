import time

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation

grid_size = int(input('What size grid?'))
dummy_grid = np.zeros((grid_size,grid_size))
length = len(dummy_grid)
fig = plt.figure(figsize=(5,5))

ax = plt.axes()
im = ax.imshow(dummy_grid,cmap='binary')
for n in range(0,length):
    plt.axvline(.5+n)
    plt.axhline(.5+n)

startup_points = []
while True:
    while len(startup_points) < 5:
        pt = plt.ginput(1, timeout=-1)
        p_1 = int(round(pt[0][1],0))
        p_2 = int(round(pt[0][0],0))
        coord = (p_2,len(dummy_grid)-p_1-1)
        if coord in startup_points:
            dummy_grid[p_1][p_2] = 0
            startup_points.remove(coord)
        else:
            dummy_grid[p_1][p_2] = 1
            startup_points.append(coord)
        plt.imshow(dummy_grid,cmap='binary')


    pt = plt.ginput(1, timeout=-1)
    p_1 = int(round(pt[0][1],0))
    p_2 = int(round(pt[0][0],0))
    coord = (p_2,len(dummy_grid)-p_1-1)
    if coord in startup_points:
        dummy_grid[p_1][p_2] = 0
        startup_points.remove(coord)
    else:
        dummy_grid[p_1][p_2] = 1
        startup_points.append(coord)
    plt.imshow(dummy_grid,cmap='binary')
    if plt.waitforbuttonpress():
        break

#fig.clf()

def list_out_neighbors(x,y,grid_max):
    neighbor_xs = list(range(max(0,x-1),min(x+2,grid_max)))
    neighbor_ys = list(range(max(0,y-1),min(y+2,grid_max)))

    neighbors = []
    for i in neighbor_xs:
        for j in neighbor_ys:
            if (i,j) != (x,y):
                neighbors.append((i,j))
    return neighbors

class conway_cell:
    def __init__(self,status,x,y,grid_max):
        self.coord = (x,y)
        if status == 'live':
            self.live = 1
        else:
            self.live = 0

        self.neighbors = list_out_neighbors(x,y,grid_max)

    def update_n_live_neighbors(self,n):
        self.live_neighbors = n

    def update_live_status(self):
        if self.live_neighbors <2:
            self.live = 0
        elif self.live_neighbors ==2:
            #no change
            pass
        elif self.live_neighbors ==3:
            self.live = 1
        else:
            self.live = 0

def make_grid(grid_size,live_points):
    grid = []
    for x in range(0,grid_size):
        temp=[]
        for y in range(0,grid_size):
            if (x,y) in live_points:
                temp.append(conway_cell('live',x,y,grid_size))
            else:
                temp.append(conway_cell('dead',x,y,grid_size))
        grid.append(temp)
    return grid
def count_live_neighbors(cell,grid):
    count = 0
    for neighbor in cell.neighbors:
        count += grid[neighbor[0]][neighbor[1]].live
    return count

def neighbor_count_sweep(grid):
    active = []
    for x in range(0,len(grid)):
        for y in range(0,len(grid)):
            count = count_live_neighbors(grid[x][y],grid)
            grid[x][y].update_n_live_neighbors(count)
            if count>0 or grid[x][y].live > 0:
                active.append((x,y))
    return grid, active

def status_update_sweep(grid,active_list):
    n_changed = 0
    for cell in active_list:
        old_status = grid[cell[0]][cell[1]].live
        grid[cell[0]][cell[1]].update_live_status()
        new_status = grid[cell[0]][cell[1]].live
        if old_status != new_status:
            n_changed +=1
    return n_changed

def update_plot_grid(object_grid,plot_grid):
    for row in object_grid:
        for cell in row:
            x, y = cell.coord
            p_1 = len(plot_grid)-y-1
            p_2 = x
            plot_grid[p_1][p_2] = object_grid[x][y].live

def animate_update(n,plot_grid, object_grid):
    object_grid, active_list = neighbor_count_sweep(object_grid)
    update_plot_grid(object_grid,active_list,plot_grid)
    n_changed = status_update_sweep(object_grid,active_list)
    print(n)
    im.set_data(plot_grid)

plot_grid = np.zeros((length,length))
object_grid = make_grid(length,startup_points)
object_grid, active_list = neighbor_count_sweep(object_grid)
update_plot_grid(object_grid,plot_grid)

fig = plt.figure(figsize=(5,5))
ax = plt.axes()

ims = []
im = ax.imshow(plot_grid,cmap='binary')

ims.append([im])
n_changed = 1
for i in range(0,100):
    if n_changed>0:
        n_changed = status_update_sweep(object_grid,active_list)
        object_grid, active_list = neighbor_count_sweep(object_grid)
        update_plot_grid(object_grid,plot_grid)

        im = ax.imshow(plot_grid,cmap='binary')
        ims.append([im])



ani = animation.ArtistAnimation(fig, ims, interval=300, blit=True,
                                repeat_delay=1000)


plt.show()
ani.save('animation.gif',writer='imagemagick')
