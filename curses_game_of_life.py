import curses
import time

def translate_from_curses(y,x,gridsize):
    x = x-1
    y = gridsize-y
    return (x,y)

def translate_to_curses(x,y,gridsize):
    x = x+1
    y = gridsize - y
    return (y,x)

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

#use wrapper
def main(stdscr):
    #stop cursor from blinking
    curses.curs_set(0)
    curses.init_pair(1,curses.COLOR_BLACK, curses. COLOR_WHITE)

    #find sizes of terminal window
    h, w = stdscr.getmaxyx()



    #Find coordinates to center this text
    text = "Welcome to Conway's Game of Life"
    x = w//2 - len(text)//2
    y = h//2

    #add something to screen and refresh
    stdscr.addstr(y,x,text)

    text_scr = "Consider expanding the terminal window to allow for a larger grid"
    x_scr = w//2 - len(text_scr)//2
    y_scr = h//2 + 2
    stdscr.addstr(y_scr,x_scr,text_scr)

    text_2 = "Press 'a' to begin"
    x_2 = x = w//2 - len(text_2)//2
    stdscr.addstr(h-1,x_2,text_2)
    stdscr.refresh()

    pause = True
    while pause == True:
        if stdscr.getch() == ord('a'):
            stdscr.clear()
            pause = False

        #key = stdscr.getch()
        #if key == curses.KEY_UP:
        #    stdscr.clear()
        #    pause = False

    text = "How big a grid would you like?"
    #set max gridsize and reset window size calc
    h, w = stdscr.getmaxyx()
    max_gridsize = min(h,w) - 8

    x = w//2 - len(text)//2
    y = h//2
    stdscr.addstr(y,x,text)

    text_2 = "Up and down arrows to change grid size"
    text_3 = "right arrow to select size"
    x_2 = w//2 - len(text_2)//2
    stdscr.addstr(h-2,x_2,text_2)
    x_3 = w//2 - len(text_3)//2
    stdscr.addstr(h-1,x_3,text_3)
    stdscr.refresh()
    pause = True
    while pause == True:
        gridsize = 10
        stdscr.addstr(y+1,x,str(gridsize))

        while 1:
            key = stdscr.getch()

            if key == curses.KEY_DOWN and gridsize > 0:
                gridsize -= 1
            elif key == curses.KEY_UP and gridsize < max_gridsize:
                gridsize += 1
            elif key == curses.KEY_RIGHT:
                pause = False
                break

            stdscr.clear()
            stdscr.addstr(y,x,text)
            stdscr.addstr(y+1,x,str(gridsize))
            stdscr.addstr(h-2,x_2,text_2)
            stdscr.addstr(h-1,x_3,text_3)
            stdscr.refresh()

    stdscr.clear()


    text = f"You've selected a {str(gridsize)} X {str(gridsize)} grid"
    x = w//2 - len(text)//2
    y = h//2
    stdscr.addstr(y,x,text)
    stdscr.refresh()
    time.sleep(2)

    border_line = '+' + (gridsize * '_') + '+'
    sides = '|' + (gridsize*u'\u25A1') + '|'
    top_y = h//2 - gridsize//2
    if gridsize%2==0:
        bottom_y = h//2 + gridsize//2 + 1
    else:
        bottom_y = h//2 + gridsize//2 + 2
    left_x = w//2 - gridsize//2
    right_x =w//2 + gridsize//2
    stdscr.clear()
    #turn on cursor now
    curses.curs_set(1)
    stdscr.addstr(top_y,left_x,border_line)
    stdscr.addstr(bottom_y,left_x,border_line)
    for n in range(1,gridsize+1):
        stdscr.addstr(top_y+n,left_x,sides)

    text_2 = "Move around grid with arrow keys"
    text_3 = "Press 'a' to toggle cell alive/dead"
    text_4 = "Press 's' to start"
    x_2 = w//2 - len(text_2)//2
    stdscr.addstr(h-3,x_2,text_2)
    x_3 = x = w//2 - len(text_3)//2
    stdscr.addstr(h-2,x_3,text_3)
    x_4 = x = w//2 - len(text_4)//2
    stdscr.addstr(h-1,x_4,text_4)

    stdscr.refresh()
    loc_y = 1
    loc_x = 1
    location_dict = {}
    looping = True
    while looping == True:
        stdscr.move(top_y+loc_y, left_x+loc_x)
        c = stdscr.getch()

        if c == curses.KEY_UP and loc_y>1:
            loc_y -= 1
        elif c == curses.KEY_DOWN and loc_y<gridsize:
            loc_y += 1
        elif c == curses.KEY_LEFT and loc_x > 1:
            loc_x -= 1
        elif c == curses.KEY_RIGHT and loc_x < gridsize:
            loc_x += 1
        c = chr(c)
        if c in 'Aa':
            if (loc_x,loc_y) in location_dict.keys():
                if location_dict[(loc_x,loc_y)] == 1:
                    stdscr.addstr(top_y+loc_y,left_x+loc_x,u'\u25A1')
                    location_dict[(loc_x,loc_y)] = 0
                else:
                    stdscr.addstr(top_y+loc_y,left_x+loc_x,'*')
                    location_dict[(loc_x,loc_y)] = 1
            else:
                location_dict[(loc_x,loc_y)] = 1
                stdscr.addstr(top_y+loc_y,left_x+loc_x,'*')
            stdscr.refresh()
        elif c in 'Ss':
            break

    #turn off cursor now
    curses.curs_set(0)

    # let's turn the location dict into a list to pass the grid creator
    initial_live_list = []
    for key in location_dict.keys():
        if location_dict[key] == 1:
            initial_live_list.append(translate_from_curses(key[1],key[0],gridsize))

    #Now generate a grid with live cells at these positions
    grid = make_grid(gridsize,initial_live_list)

    #for initial display, we'll need to go through everything
    stdscr.clear()
    stdscr.addstr(top_y,left_x,border_line)
    stdscr.addstr(bottom_y,left_x,border_line)
    sides = '|' + (gridsize*' ') + '|'
    for n in range(1,gridsize+1):
        stdscr.addstr(top_y+n,left_x,sides)

    for n in range(1,gridsize+1):
        stdscr.addstr(top_y+n,left_x,sides)
    for column in grid:
        for cell in column:
            if cell.live == 1:
                coord_x = cell.coord[0]
                coord_y = cell.coord[1]
                curse_coord = translate_to_curses(coord_x,coord_y,gridsize)
                stdscr.addstr(top_y+curse_coord[0],left_x+curse_coord[1],'*')
    text_2 = "Observe the Game of Life play out"
    text_3 = "Press 'q' to quit"
    x_2 = w//2 - len(text_2)//2
    stdscr.addstr(h-2,x_2,text_2)
    x_3 = w//2 - len(text_3)//2
    stdscr.addstr(h-1,x_3,text_3)

    stdscr.refresh()
    time.sleep(2)

    #Let's start a counter
    counter = 1
    while 1:

        #sweep through for active list
        grid, active_list = neighbor_count_sweep(grid)
        #update the status of each possibly active cell
        n_changed = status_update_sweep(grid,active_list)
        # replace screen elements for cells in active list
        for (x,y) in active_list:
            curse_coord = translate_to_curses(x,y,gridsize)
            if grid[x][y].live == 1:
                stdscr.addstr(top_y+curse_coord[0],left_x+curse_coord[1],'*')
            else:
                stdscr.addstr(top_y+curse_coord[0],left_x+curse_coord[1],' ')
        if n_changed >0:
            counter +=1

        text = f'Turn: {str(counter)}'
        stdscr.addstr(top_y-1,left_x,text)
        stdscr.refresh()

        # if no keystroke is available, instead of waiting.
        stdscr.nodelay(1)
        if stdscr.getch() == ord('q'):
            break
        time.sleep(.5)


    time.sleep(1)

curses.wrapper(main)
