import itertools                                            #   to turn iterables into lists

import matplotlib.pyplot as plt
from matplotlib.widgets import Button, CheckButtons

import numpy as np 
import random                                               #   the Random in RandomWalk
import sys                                                  #   to run function from terminal while using inputs

class Point():
    '''
    This Class will be used to generate individual Agents, each as a Point in space
    '''
    def __init__(self,x,y,z,dim) -> None:
            self.x = x              
            self.y = y
            self.z = z                                      #   When using 2d representation, the z coordinate will take fixed value of 1, but it will never be accessed when plotting.
            self.dim = dim                                  #   dim - standing for Dimensionality, may take either value 2 or 3, depending on whether the plot should be two/three-dimensional
            intervals = np.linspace(0,1,self.dim*2 + 1)     #   generates list of values to use as equal probability intervals for the agent, to decide which direction to walk
            self.intervals_commands = {}                    #   by the end of the for loop, this dictionary will contain keys corresponding to values in the intervals (apart from 0),
                                                            #   and values according to the commands, in string format, to run for changing the coordinates of the Point
            coords = ['x','y','z']
            for i,el in enumerate(intervals[1:]): 
                self.intervals_commands[str(intervals[((i//2)*2 + [0,1][i%2])+1])] = 'self.' + coords[(i)//2] + ['+=1','-=1'][i%2]      #   i%2 is used to indicate whether i is even or odd for each step
                                                                                                                                        #   i//2 maps for example [0,1,2,3,4,5] to -> [0,0,1,1,2,2]

    def show(self):                                         #   useful function for debugging, showing coordinates at given time alongside dimensionality of the point
        print(self.x,self.y,self.z,self.dim)
    
    def coords(self):                                       #   returns the three spatial coordinates x y and z.
        return (self.x, self.y,self.z) 
    
    def walk(self):                                         #   Walk when called will move to point in one of the possible directions, 4 in case of 2d and 6 in 3d
        num = random.random()
        for el in self.intervals_commands.keys():
            if num <= float(el):                            #   checks for each interval, iteratively, whether it falls below the upper limit
                exec(self.intervals_commands[el])           #   executes command associated with interval
                break                                       #   once we identify in which interval the random_value resides we break the cycle



def RandomWalk(points,n,steps,dimensions):                  #   The Main Function
    '''
    points      -> number of agents/points to plot
    n           -> number of moves/turns for each agent
    steps       -> number of steps/walks allowed for each move. for example: steps=2 allows a Point to move in 1 turn/move to go from [x:0,y:0] to [x:2,y:0]
    dimensions  -> dimensions of the plot, either 2 or 3
    '''

    fig = plt.figure(figsize= (12,8))
    colours = ['red','orange','yellow','green','lightblue','blue','pink','violet','purple','brown','lightgray','gray','black']          #   this will be used to differentiate the Agents
    if dimensions == 3:                                     #   changing ax projection depending on dimensionality
        ax = fig.add_subplot(1, 3, (1, 2), projection='3d')
    elif dimensions == 2:
        ax = fig.add_subplot(1, 3, (1, 2))

    plt.subplots_adjust(bottom=.1,left=.1)
    
    global counter, points_paths, paths_files
    counter = n+1                                           #   counter will be used to know at which step of the RandomWalk we are as we move back and forth.
    points_paths = {}                                       #   this dictionary will contain Points' ids as keys and their coordinates as values
    paths_files = {'paths':{},'starts':{},'ends':{}}        #   this dictionary will contain for each Point's id, the Point object itself, the starting point (by default 0,0,0) and ending point


    #   [ Next/Previous ] Buttons set-up
    ax_next = plt.axes([.8,.8,.1,.05])                      #   setting up position of the buttons
    next_button = Button(ax_next, 'Next', color='white', hovercolor='grey')     #   instatiating Button and aspect
    ax_prev = plt.axes([.7,.8,.1,.05])
    prev_button = Button(ax_prev, 'Prev', color='white', hovercolor='grey')
    # check button initalization is moved to the bottom


    def set_ticks(point_dict,axis):
        '''
        set ticks for all axis of the plot, fixing them as we move back and forth through steps.
        
        Inputs:
        point_dict : points_paths, a dictionary with points coordinates
        axis       : ax on which to plot the point, created in ax = add.subplot...
        '''

        max_x = np.max(list(itertools.chain.from_iterable([point_dict[x]['x'] for x in point_dict])))       #   retrieve max and min value from all points' coordinate X
        min_x = np.min(list(itertools.chain.from_iterable([point_dict[x]['x'] for x in point_dict])))

        axis.set_xticks(np.arange(min_x-2,max_x+3,steps))                                                   #   set ticks for the plot. -2 and +2 are used to make the plot better visually, +1 for max is used to include max in range.
                                                                                                            #   and using steps as steps in the range makes it so that we don't plot too many ticks
        
        max_y = np.max(list(itertools.chain.from_iterable([point_dict[x]['y'] for x in point_dict])))
        min_y = np.min(list(itertools.chain.from_iterable([point_dict[x]['y'] for x in point_dict])))
        
        axis.set_yticks(np.arange(min_y-2,max_y+3,steps))

        if dimensions == 3:
        
            max_z = np.max(list(itertools.chain.from_iterable([point_dict[x]['z'] for x in point_dict])))
            min_z = np.min(list(itertools.chain.from_iterable([point_dict[x]['z'] for x in point_dict])))
            axis.set_zticks(np.arange(min_z-2,max_z+2,steps))
        
    def draw_plot(count):
        '''
        Each time the plot needs to be updated, this function will redraw each agent's path, start point and end point.
        '''
        global paths_files                                  #   we need to set it global, as within this function, paths_files will be updated/changed

        for j in range(points):

            color = colours[j%len(colours)]
            x = points_paths['Point_'+str(j)]['x'][:count]
            y = points_paths['Point_'+str(j)]['y'][:count]
            z = points_paths['Point_'+str(j)]['z'][:count]

            if dimensions == 3:

                paths_files['starts']['Point_'+str(j)] = ax.scatter3D(x[0],y[0],z[0],c=color,alpha=paths_files['starts']['Point_'+str(j)].get_alpha())
                paths_files['paths']['Point_'+str(j)], = ax.plot3D(x,y,z,c=color,label='Point_'+str(j),lw=2,alpha=paths_files['paths']['Point_'+str(j)].get_alpha())
                paths_files['ends']['Point_'+str(j)] = ax.scatter3D(x[-1],y[-1],z[-1],c=color,marker='x',alpha=paths_files['ends']['Point_'+str(j)].get_alpha())
                set_ticks(points_paths,ax)
            elif dimensions == 2:

                paths_files['starts']['Point_'+str(j)] = ax.scatter(x[0],y[0],c=color,alpha=paths_files['starts']['Point_'+str(j)].get_alpha())
                paths_files['paths']['Point_'+str(j)], = ax.plot(x,y,c=color,label='Point_'+str(j),lw=2,alpha=paths_files['paths']['Point_'+str(j)].get_alpha())
                paths_files['ends']['Point_'+str(j)] = ax.scatter(x[-1],y[-1],c=color,marker='x',alpha=paths_files['ends']['Point_'+str(j)].get_alpha())
                set_ticks(points_paths,ax)
    
    def select_plot(label):
        '''
        This function will determine the functioning of our CheckPoints -> [x], everytime we check a box,
        the corresponding agent will have its alpha (transparency) changed back and forth between 0.05 (almost fully transparent) and 1 (fully visible)
        '''
        if paths_files['paths'][label].get_alpha() == .05:
            paths_files['paths'][label].set_alpha(1)
            paths_files['starts'][label].set_alpha(1)
            paths_files['ends'][label].set_alpha(1)
        else:
            paths_files['paths'][label].set_alpha(.05)
            paths_files['starts'][label].set_alpha(.05)
            paths_files['ends'][label].set_alpha(.05)
            
        fig.canvas.draw()
    
    def next(val):
        '''
        plots are pushed forward one move, if possible
        '''
        global counter  # both next and val call upon counter, to know and change 'time-position' within the plot

        ax.clear()
        if counter == n+1:
            pass
        else:
            counter += 1
        draw_plot(counter)
        fig.canvas.draw()

    def prev(val):
        '''
        plots are pulled back one move, if possible
        '''
        global counter

        ax.clear()
        if counter == 1:
            pass
        else:
            counter -= 1
        draw_plot(counter)
        fig.canvas.draw()

    for j in range(points):                                 #   This loop is ran only one time, and is responsible for the first plot (full paths)

        color = colours[j%len(colours)]
        a = Point(0,0,0,dimensions)                         #   Agent/Point j initialization
        x, y, z = [], [], []
        x.append(a.coords()[0]), y.append(a.coords()[1]), z.append(a.coords()[2])       # append Starting Point (default is 0,0,0)
        
        for i in range(n):                                  #   loop for each move
    
            for h in range(steps):                          #   loop for each step

                a.walk()
    
            new = a.coords()
            x.append(new[0]), y.append(new[1]), z.append(new[2])
        
        points_paths['Point_'+str(j)] = {                   #   first instance of points_paths completed
            'x' : x,
            'y' : y,
            'z' : z,
        }
        if dimensions == 3:                                 #   plotting full paths, starts, denoted by 'o', and ends, denoted by 'x'
            paths_files['starts']['Point_'+str(j)] = ax.scatter3D(a.coords()[0],a.coords()[1],a.coords()[2],c=color)
            paths_files['ends']['Point_'+str(j)] = ax.scatter3D(a.coords()[0],a.coords()[1],a.coords()[2],c=color,marker='x')
            paths_files['paths']['Point_'+str(j)], = ax.plot3D(x,y,z,c=color,label='Point_'+str(j),lw=2)
        elif dimensions == 2:
            paths_files['starts']['Point_'+str(j)] = ax.scatter(a.coords()[0],a.coords()[1],c=color)
            paths_files['ends']['Point_'+str(j)] = ax.scatter(a.coords()[0],a.coords()[1],c=color,marker='x')
            paths_files['paths']['Point_'+str(j)], = ax.plot(x,y,c=color,label='Point_'+str(j),lw=2)

    next_button.on_clicked(next)                             #  defining function to be called by the buttons
    prev_button.on_clicked(prev)

    activated = [True]*len(list(points_paths.keys()))        #  state of each CheckButton at start
    labels = list(paths_files['paths'].keys())               #  names to give each CheckButton
    ax_check = plt.axes([.7,0.79-(.025*len(labels)),.2,.025*len(labels)])

    check_button = CheckButtons(ax_check,labels,activated)
    check_button.on_clicked(select_plot)
    
    set_ticks(points_paths,ax)
    
    plt.show()

#-------------------------------------------------

if __name__=='__main__':                                    #   to run from terminal, format:  >>>py RandomWalk.py <agents> <moves> <steps> <dimensions>
                                                            #   example:                       >>>py RandomWalk.py 3    5   2   3
    RandomWalk(int(float(sys.argv[1])),int(float(sys.argv[2])),int(float(sys.argv[3])),int(float(sys.argv[4])))