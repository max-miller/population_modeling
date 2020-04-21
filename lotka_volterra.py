import matplotlib.pyplot as plt
from matplotlib import animation
from numpy import random

fig = plt.figure()
ax1 = plt.axes(xlim=(0, 50), ylim=(0,100))
line, = ax1.plot([], [], lw=2)

labels = ['Prey','Predator']
lines = []
for index in range(2):
    lobj = ax1.plot([],[],lw=2)[0]
    lines.append(lobj)


def init():
    for index in range(2):
        line = lines[index]
        line.set_data([],[])
        line.set_label(labels[index])
    legend = plt.legend(loc='upper left')

    return lines

alpha = 3
beta = .1
gamma = .8
delta = .03


x1,y1 = [0],[50]
x2,y2 = [0],[20]

for n in range(100):
    new_y1 = y1[-1] + ((alpha - beta*y2[-1])*y1[-1])*.1
    new_y2 = y2[-1] + ((delta*y1[-1] - gamma)*y2[-1])*.1
    x1.append(n)
    y1.append(new_y1)
    x2.append(n)
    y2.append(new_y2)

def animate(i):

    xlist = [x1[:i+1], x2[:i+1]]
    ylist = [y1[:i+1], y2[:i+1]]

    for lnum,line in enumerate(lines):
        line.set_data(xlist[lnum], ylist[lnum]) # set data for each line separately.
        line.set_label(labels[lnum])
    legend = plt.legend(loc='upper left')
    return lines + [legend]

# call the animator.  blit=True means only re-draw the parts that have changed.
anim = animation.FuncAnimation(fig, animate, init_func=init, repeat=False,
                               frames=50, interval=50, blit=False)

plt.legend()
plt.show()
anim.save('lotka_volterra_test.gif', writer = 'imagemagick')
