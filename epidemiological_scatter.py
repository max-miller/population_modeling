import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation
from matplotlib.colors import ListedColormap, BoundaryNorm

cm = ListedColormap(['b','r','k'],N=3)
norm = BoundaryNorm([-.5,.5,1.5,2.5],3)


def distance(coord_1,coord_2):
    return np.sqrt((coord_1[0]-coord_2[0])**2 + (coord_1[1]-coord_2[1])**2)

class individual:
    def __init__(self,coords,status,bounds,speed):
        self.coord = coords
        self.status = status
        self.bounds = bounds
        self.speed = speed
        self.time = 0
        self.removed = 0

    def set_direction(self):
        angle = np.random.uniform(0,2*np.pi)
        x_direction = np.cos(angle)
        y_direction = np.sin(angle)

        self.x_direction = x_direction
        self.y_direction = y_direction

    def update_location(self):
        speed = self.speed
        bounds = self.bounds


        distance = speed*np.random.random()

        if self.coord[0] + distance*self.x_direction < 0:
            new_x = -distance*self.x_direction-self.coord[0]
            self.x_direction = -self.x_direction
        elif self.coord[0] + distance*self.x_direction > bounds[0]:
            new_x = 2*bounds[0]-distance*self.x_direction - self.coord[0]
            self.x_direction = -self.x_direction
        else:
            new_x = self.coord[0] + distance*self.x_direction

        if self.coord[1] + distance*self.y_direction < 0:
            new_y = -distance*self.y_direction-self.coord[1]
            self.y_direction = -self.y_direction
        elif self.coord[1] + distance*self.y_direction > bounds[1]:
            new_y = 2*bounds[1]-distance*self.y_direction - self.coord[1]
            self.y_direction = -self.y_direction
        else:
            new_y = self.coord[1] + distance*self.y_direction

        self.coord = (new_x,new_y)

    def transmission(self,others,radius,probability):
        if self.removed == 1:
            pass
        elif self.status == 1:
            self.time +=1
            if self.time == 175:
                self.status =2
                self.removed = 1
        else:
            neighbor_count = 0
            for other in others:
                if other.status == 1:
                    if distance(self.coord,other.coord) < radius:
                        neighbor_count +=1
            if sum([1 for x in np.random.random(neighbor_count) if x >probability]) > 0:
                self.status = 1

bounds = (5,5)
radius = .05
probability = .1

everyone = []
for n in range(5):
    everyone.append(individual((10*np.random.random(),10*np.random.random()),
                               1,bounds,np.random.random()/25))

for n in range(195):
    everyone.append(individual((10*np.random.random(),10*np.random.random()),
                               0,bounds,np.random.random()/25))

for n in range(0,len(everyone)):
    everyone[n].set_direction()

fig = plt.figure(figsize=(5,5))
plt.xlim(0,5)
plt.ylim(0,5)
ax=plt.axes()

master_coords = []
master_status = []
ims=[]

for n in range(300):
    coords = []
    status = []
    for person in everyone:
        coords.append(person.coord)
        status.append(person.status)
    status = np.array(status)
    coords = np.array(coords)
    im=[ax.scatter(coords[:,0],coords[:,1],c=status,cmap=cm,norm=norm)]
    ims.append(im)

    master_coords.append(coords)
    master_status.append(status)


    for i in range(0,len(everyone)):
        everyone[i].transmission(everyone[:i]+everyone[i+1:],radius,probability)
    for i in range(0,len(everyone)):
        everyone[i].update_location()


# def init():
#     scat.set_array([],[])
#
#     return scat

# def animate(i):
#     coordinates = master_coords[i]
#     statuses = master_status[i]
#     scat.set_array(coordinates)
#     scat.set_array(statuses)
#     return scat,
#
# # call the animator.  blit=True means only re-draw the parts that have changed.
# anim = animation.FuncAnimation(fig, animate, repeat=False,
#                                frames=50, interval=50, blit=False)

ani = animation.ArtistAnimation(fig, ims, interval=20, blit=True,repeat_delay=1000)
ani.save('epidemiological_scatter.gif', writer = 'imagemagick')
plt.show()
