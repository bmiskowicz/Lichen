import pygame
import pygame_menu
import numpy
import random
import time
from pygame_menu.examples import create_example_window
from typing import Tuple, Any

surface = create_example_window('Projekt - Liszaj', (1080, 720))



import matplotlib
matplotlib.use("Agg")
import matplotlib.backends.backend_agg as agg
import pylab
import matplotlib.pyplot as plt

plt.rcParams.update({
    #"lines.marker": "o",         # available ('o', 'v', '^', '<', '>', '8', 's', 'p', '*', 'h', 'H', 'D', 'd', 'P', 'X')
    "lines.linewidth": "0.8",
    "axes.prop_cycle": plt.cycler('color', ['white']),  # line color
    "text.color": "white",       # no text in this example
    "axes.facecolor": "black",   # background of the figure
    "axes.edgecolor": "lightgray",
    "axes.labelcolor": "white",  # no labels in this example
    "axes.grid": "True",
    "grid.linestyle": "--",      # {'-', '--', '-.', ':', '', (offset, on-off-seq), ...}
    "xtick.color": "white",
    "ytick.color": "white",
    "grid.color": "lightgray",
    "figure.facecolor": "black", # color surrounding the plot
    "figure.edgecolor": "black",
})




class Graph:
    numbers = []
    red=[]
    yellow=[]
    grey=[]
    

class Model:
    stop=0
    running = True
    param_size = [[10, 100], [20, 50], [40, 25], [50, 20], [100, 10], [200, 5]] 
    diff_tab = [0, 5, 10]
    prob_tab = [50, 70, 90, 10, 20]
    tab = numpy.zeros((2, param_size[1][0], param_size[1][0]))
    menu=None
    diff = None
    size = None
    prob = None
    simulation_name = None


class Button:
    def __init__(self, fk, text, posX, posY, sizeX, sizeY, font, bg="White"):
        self.x = posX
        self.y = posY
        self.font = pygame.font.SysFont("Arial", font)
        self.text = self.font.render(text, 1, pygame.Color("Black"))
        self.size = (sizeX, sizeY)
        self.surface = pygame.Surface(self.size)
        self.surface.fill(bg)
        self.surface.blit(self.text, (5, 2))
        rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])
        self.rect = rect
        self.fk=fk


    def click(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    self.fk()


    def show(self):
        surface.blit(self.surface, (self.x, self.y))


def set_difficulty(selected: Tuple, value: Any) -> None:
    ""

def set_probability(selected: Tuple, value: Any) -> None:
    ""

def set_size(selected: Tuple, value: Any) -> None:
    ""


def resize(val, valSize):
        newtab =  Model.tab.copy()
        Model.param_size[Model.size][0] = Model.param_size[Model.size][0]+val
        Model.param_size[Model.size][1] = 1000/Model.param_size[Model.size][0]
        newtab2 = numpy.zeros((2, Model.param_size[Model.size][0], Model.param_size[Model.size][0]))
        Model.tab.resize((2, Model.param_size[Model.size][0], Model.param_size[Model.size][0]), refcheck=False)
        Model.tab=newtab2.copy()
        for k in range(2):
            for i in range(Model.param_size[Model.size][0]+valSize):
                for j in range(Model.param_size[Model.size][0]+valSize):
                    Model.tab[k][i][j]=newtab[k][i][j]


def speedUp():
    if(Model.diff>0.9):
        Model.diff=Model.diff-1


def speedDown():
    if(Model.diff<9.1):
        Model.diff=Model.diff+1


def sizeUp():
    if(Model.param_size[Model.size][0]<200):
        resize(10, -10)


def sizeDown():
    if(Model.param_size[Model.size][0]>10):
        resize(-10, 0)


def probUp():
    if(Model.prob<100):
        Model.prob=Model.prob+5


def probDown():
    if(Model.prob>5):
        Model.prob=Model.prob-5


def graph():
    Model.stop= not Model.stop


def reset():
    Model.param_size = [[10, 100], [20, 50], [40, 25], [50, 20], [100, 10], [200, 5]] 
    newtab =  numpy.zeros((2, Model.param_size[Model.size][0], Model.param_size[Model.size][0]))
    Model.tab = newtab.copy()
    
    l = Model.param_size[Model.size][0]

    Model.tab = numpy.zeros((2, l, l))
    Model.tab[0][int(l/2)][int(l/2)] = 1
    Model.tab[1][int(l/2)][int(l/2)] = 2

    if(Model.stop==1): Model.stop=0


def clear():
    newtab =  numpy.zeros((2, Model.param_size[Model.size][0], Model.param_size[Model.size][0]))
    Model.tab = newtab.copy()


def drawGraph():    

    fig = pylab.figure(figsize=[7, 7], # Inches
            dpi=100)        # 100 dots per inch
    fig.patch.set_alpha(0.1)           # make the surrounding of the plot 90% transparent to show what it does

    ax = fig.gca()
    ax.set_prop_cycle(color=['red', 'yellow', 'grey'])
    ax.plot(Graph.red)
    ax.plot(Graph.yellow)
    ax.plot(Graph.grey)

    canvas = agg.FigureCanvasAgg(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.buffer_rgba()

    pygame.init()
    screen = pygame.display.get_surface()

    size = canvas.get_width_height()
    surf = pygame.image.frombuffer (raw_data, size, "RGBA")

    screen.blit(surf, (1150, 400)) # x, y position on screen


def saveGraph():
    plt.savefig(Model.simulation_name.get_value() + '.png', bbox_inches='tight')


def drawCells():
    l = Model.param_size[Model.size][1]
    # drawing the cells
    for i in range(0, Model.param_size[Model.size][0]):
        for j in range(0, Model.param_size[Model.size][0]):
            if(Model.tab[0][i][j]==0):
                pygame.draw.rect(surface, "yellow", pygame.Rect(50+i*l, 50+j*l, l, l))
            if (Model.tab[0][i][j] == 1):
                pygame.draw.rect(surface, "red", pygame.Rect(50+i*l, 50+j*l, l, l))
            if (Model.tab[0][i][j] == 2):
                pygame.draw.rect(surface, "grey", pygame.Rect(50+i*l, 50+j*l, l, l))


def printText():
    font = pygame.font.Font(None, 32)
    txt_surface = font.render("Speed = " + str(Model.diff), True, "Black")
    surface.blit(txt_surface, (1100, 110,))
    txt_surface = font.render("Probability = " + str(Model.prob) +"%", True, "Black")
    surface.blit(txt_surface, (1100, 160))
    txt_surface = font.render("Size = " + str(Model.param_size[Model.size][0]) + " x " + str(Model.param_size[Model.size][0]), True, "Black")
    surface.blit(txt_surface, (1100, 210))


def changeSurface():
    x, y = pygame.mouse.get_pos()
    l = Model.param_size[Model.size][1]
    if(x<Model.param_size[Model.size][0]*l and y<Model.param_size[Model.size][0]*l and x>50 and y>50):
        
        i=int((x-50)/l)
        j=int((y-50)/l)

        if Model.tab[0][i][j]==0: 
            Model.tab[0][i][j]=1
            Model.tab[1][i][j]=2
            pygame.draw.rect(surface, "yellow", pygame.Rect(50+i*l, 50+j*l, l, l))

        elif Model.tab[0][i][j]==1: 
            Model.tab[0][i][j]=2
            Model.tab[1][i][j]=2
            pygame.draw.rect(surface, "red", pygame.Rect(50+i*l, 50+j*l, l, l))

        elif Model.tab[0][i][j]==2: 
            Model.tab[0][i][j]=0
            Model.tab[1][i][j]=3
            pygame.draw.rect(surface, "grey", pygame.Rect(50+i*l, 50+j*l, l, l))


def logic():
    "main logic of the simulation"
    for i in buttons:
        i.show()
    printText()

    drawCells()
    drawGraph()
    pygame.display.flip()


    Graph.numbers = [0, 0, 0]

    k = 0
    i = 0
    j = 0
    newtab = Model.tab.copy()

    l=Model.param_size[Model.size][0]

    for i in range(0, l):
        for j in range(0, l):
            Graph.numbers[int(Model.tab[0][i][j])] = Graph.numbers[int(Model.tab[0][i][j])]+1
            neighbours=[]
            if(Model.tab[1][i][j]==0):
                if Model.tab[0][i][j]==2: 
                    newtab[0][i][j]=0
                    newtab[1][i][j]=3

                if Model.tab[0][i][j]==1: 
                    newtab[0][i][j]=2
                    newtab[1][i][j]=2


            else: 
                newtab[1][i][j]=newtab[1][i][j]-1
                
                if(Model.tab[0][i][j]==1):
                    if i%l!=l-1: 
                        if(Model.tab[0][i+1][j]==0): neighbours.append([i+1,j])

                    if i%l!=0:
                        if(Model.tab[0][i-1][j]==0): neighbours.append([i-1,j])

                    if j>0:
                        if(Model.tab[0][i][j-1]==0): neighbours.append([i,j-1])

                    if j<l-1:
                        if(Model.tab[0][i][j+1]==0): neighbours.append([i,j+1])

                    for k in range(len(neighbours)):
                        randomNumber=random.randint(0, 99)
                        if(randomNumber<Model.prob):
                            newtab[0][neighbours[k][0]][neighbours[k][1]]=1
                            newtab[1][neighbours[k][0]][neighbours[k][1]]=2
    
    Model.tab=newtab.copy()

    
    Graph.yellow.append(Graph.numbers[0]*100/(l*l))
    Graph.red.append(Graph.numbers[1]*100/(l*l))
    Graph.grey.append(Graph.numbers[2]*100/(l*l))   


def start_the_simulation():
    #getting the global variables
    Model.diff = Model.diff_tab[Model.diff.get_value()[1]]
    Model.size = Model.size.get_value()[1]
    Model.prob = Model.prob_tab[Model.prob.get_value()[1]]
    simulation_name = Model.simulation_name.get_value()

    #creating the window
    background_colour = (0, 204, 153)

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption(simulation_name)
    screen.fill(background_colour)

    l = Model.param_size[Model.size][0]
    #parameters for simulation
    Model.tab = numpy.zeros((2, l, l))
    Model.tab[0][int(l/2)][int(l/2)] = 1  #tab[0][]][] - table of states
    Model.tab[1][int(l/2)][int(l/2)] = 2  #tab[0][]][] - table of remaining times
    
    logic()

    #getting windows events
    timeStart = time.process_time()
    Model.running =True

    for i in buttons:
        i.show()
    printText()
    

    while Model.running:
        screen.fill(background_colour)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0] and Model.stop==0:
                    changeSurface()
              

            if event.type == pygame.QUIT:
                Model.running = False
            for i in buttons:
                i.click(event)
        
        if(Model.stop==0):
            if time.process_time()-timeStart>Model.diff/10:
                logic()
                
                timeStart = time.process_time()
        



def start():
    surface = create_example_window('Projekt - Liszaj', (1080, 720))
    Model.menu = pygame_menu.Menu(
    height=720,
    theme=pygame_menu.themes.THEME_BLUE,
    title='Smacznej kawusi',
    width=1080
    )


    Model.simulation_name = Model.menu.add.text_input('Nazwa symulacji: ', default='liszaj01', maxchar=36)
    Model.diff = Model.menu.add.selector('Tempo propagacji choroby: ', [('Szybko (OSTROŻNIE)', 6), ('Umiarkowanie', 4), ('Powoli', 1) ], onchange=set_difficulty)
    Model.size = Model.menu.add.selector('Wielkość powierzchni skóry: ', [('10x10', 1), ('20x20', 2), ('40x40', 3), ('50x50', 4), ('100x100', 5), ('200x200', 6)], onchange=set_size)
    Model.prob = Model.menu.add.selector('Prawdopodobieństwo zakażenia: ', [ ('50%', 4), ('70%', 5), ('90%', 6), ('10%', 1), ('20%', 2)], onchange=set_probability)


    Model.menu.add.button('Rozpocznij', start_the_simulation)
    Model.menu.add.button('Wyjdź', pygame_menu.events.EXIT)

    Model.menu.mainloop(surface)




buttons = []
buttons.append(Button(graph, "Start/Stop", 1350, 50, 300, 40, font=30, bg=(242, 255, 204)))
buttons.append(Button(speedUp, "Speed +", 1350, 100, 120, 40, font=30, bg=(242, 255, 204)))
buttons.append(Button(speedDown, "Speed -", 1530, 100, 120, 40, font=30, bg=(242, 255, 204)))
buttons.append(Button(probUp, "Prob + 5%", 1350, 150, 120, 40, font=30, bg=(242, 255, 204)))
buttons.append(Button(probDown, "Prob - 5%", 1530, 150, 120, 40, font=30, bg=(242, 255, 204)))
buttons.append(Button(sizeUp, "Size + 10", 1350, 200, 120, 40, font=30, bg=(242, 255, 204)))
buttons.append(Button(sizeDown, "Size - 10", 1530, 200, 120, 40, font=30, bg=(242, 255, 204)))
buttons.append(Button(reset, "Reset", 1350, 250, 300, 40, font=30, bg=(242, 255, 204)))
buttons.append(Button(clear, "Clear", 1350, 300, 300, 40, font=30, bg=(242, 255, 204)))
buttons.append(Button(start, "Back to menu", 1350, 350, 300, 40, font=30, bg=(242, 255, 204)))
buttons.append(Button(saveGraph, "Save graph", 1700, 350, 150, 40, font=30, bg=(242, 255, 204)))

start()