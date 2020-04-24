import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation

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

    def update_location(self):
        speed = self.speed
        bounds = self.bounds

        angle = np.random.uniform(0,2*np.pi)
        x_direction = np.cos(angle)
        y_direction = np.sin(angle)


        distance = speed*np.random.random()

        if self.coord[0] + distance*x_direction < 0:
            new_x = -distance*x_direction-self.coord[0]
        elif self.coord[0] + distance*x_direction > bounds[0]:
            new_x = 2*bounds[0]-distance*x_direction - self.coord[0]
        else:
            new_x = self.coord[0] + distance*x_direction

        if self.coord[1] + distance*y_direction < 0:
            new_y = -distance*y_direction-self.coord[1]
        elif self.coord[1] + distance*y_direction > bounds[1]:
            new_y = 2*bounds[1]-distance*y_direction - self.coord[1]
        else:
            new_y = self.coord[1] + distance*y_direction

        self.coord = (new_x,new_y)

    def transmission(self,others,radius,probability):
        if self.removed == 1:
            pass
        elif self.status == 1:
            self.time +=1
            if self.time == 15:
                self.status =0
                self.removed = 1
        else:
            neighbor_count = 0
            for other in others:
                if other.status == 1:
                    if distance(self.coord,other.coord) < radius:
                        neighbor_count +=1
            if sum([1 for x in np.random.random(neighbor_count) if x >probability]) > 0:
                self.status = 1

bounds = (10,10)
radius = .2
probability = .2

everyone = []
for n in range(5):
    everyone.append(individual((10*np.random.random(),10*np.random.random()),
                               1,bounds,np.random.random()))

for n in range(995):
    everyone.append(individual((10*np.random.random(),10*np.random.random()),
                               0,bounds,np.random.random()))

infected = [5]
removed = [0]
for n in range(45):
    for i in range(0,len(everyone)):
        everyone[i].transmission(everyone[:i]+everyone[i+1:],radius,probability)
    for person in everyone:
        person.update_location()
    infected.append(sum([x.status for x in everyone]))
    removed.append(sum([x.removed for x in everyone]))
vulnerable = [1000 - removed[i] - infected[i] for i in range(0,len(infected))]


fig = plt.figure(figsize=(6,4))
plt.xlim(0,45)
plt.ylim(0,1000)
plt.tick_params(axis='x',which='both',bottom=False,top=False,labelbottom=False)
ax = plt.axes()
ims =[]
for n in range(1,len(infected)+1):
    x = list(range(0,len(infected)))[:n]
    y = [infected[:n],vulnerable[:n],removed[:n]]

    im = ax.stackplot(x,y, labels=[ 'infected','vulnerable','removed'],
             colors=['r','b','grey'])
    ims.append(im)
for n in range(10):
    ims.append(im)

ani = animation.ArtistAnimation(fig, ims, interval=120, blit=True,repeat_delay=1000)
plt.show()

ani.save('epidemiological_model.gif',writer='imagemagick')
