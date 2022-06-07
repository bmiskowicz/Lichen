import pygame
import pygame_menu
import numpy
import random
import time

from pygame_menu.examples import create_example_window

from typing import Tuple, Any

surface = create_example_window('Projekt - Liszaj', (1080, 720))


class Model:
    stop=0
    running = True
    param_size = [[10, 100], [20, 50], [40, 25], [50, 20], [100, 10], [200, 5]] 
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


def sizeUp():
    if(Model.param_size[Model.size][0]<200):
        resize(10, -10)


def sizeDown():
    if(Model.param_size[Model.size][0]>10):
        resize(-10, 0)


def reset():
    Model.param_size = [[10, 100], [20, 50], [40, 25], [50, 20], [100, 10], [200, 5]] 
    newtab =  numpy.zeros((2, Model.param_size[Model.size][0], Model.param_size[Model.size][0]))
    Model.tab = newtab.copy()
    
    l = Model.param_size[Model.size][0]

    Model.tab = numpy.zeros((2, l, l))
    Model.tab[0][int(l/2)][int(l/2)] = 1
    Model.tab[1][int(l/2)][int(l/2)] = 2

def clear():
    newtab =  numpy.zeros((2, Model.param_size[Model.size][0], Model.param_size[Model.size][0]))
    Model.tab = newtab.copy()


def logic():
    "main logic of the simulation"
    for i in buttons:
        i.show()

    l = Model.param_size[Model.size][1]
    # drawing the cells
    for i in range(0, Model.param_size[Model.size][0]-1):
        for j in range(0, Model.param_size[Model.size][0]-1):
            if(Model.tab[0][i][j]==0):
                pygame.draw.rect(surface, "yellow", pygame.Rect(50+i*l, 50+j*l, l, l))
            if (Model.tab[0][i][j] == 1):
                pygame.draw.rect(surface, "red", pygame.Rect(50+i*l, 50+j*l, l, l))
            if (Model.tab[0][i][j] == 2):
                pygame.draw.rect(surface, "grey", pygame.Rect(50+i*l, 50+j*l, l, l))




    pygame.display.flip()


    k = 0
    i = 0
    j = 0
    # drawing the cells
    newtab = Model.tab.copy()
    for i in range(0, Model.param_size[Model.size][0]):
        for j in range(0, Model.param_size[Model.size][0]):
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
                    if i%Model.param_size[Model.size][0]!=Model.param_size[Model.size][0]-1: 
                        if(Model.tab[0][i+1][j]==0): neighbours.append([i+1,j])

                    if i%Model.param_size[Model.size][0]!=0:
                        if(Model.tab[0][i-1][j]==0): neighbours.append([i-1,j])

                    if j>0:
                        if(Model.tab[0][i][j-1]==0): neighbours.append([i,j-1])

                    if j<Model.param_size[Model.size][0]-1:
                        if(Model.tab[0][i][j+1]==0): neighbours.append([i,j+1])

                    for k in range(len(neighbours)):
                        randomNumber=random.randint(0, 99)
                        if(randomNumber<50):
                            newtab[0][neighbours[k][0]][neighbours[k][1]]=1
                            newtab[1][neighbours[k][0]][neighbours[k][1]]=2

    Model.tab=newtab.copy()


def start_the_simulation():

    #menu.disable()
    """
    main function of the simulation 
    """
    #getting the global variables
    Model.diff = Model.diff.get_value()[1]
    Model.size = Model.size.get_value()[1]
    Model.prob = Model.prob.get_value()[1]
    simulation_name = Model.simulation_name.get_value()

    #creating the window
    background_colour = (0, 204, 153)
    (width, height) = (1920, 1080)
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
    

    while Model.running:
        screen.fill(background_colour)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
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
              

            if event.type == pygame.QUIT:
                Model.running = False
            for i in buttons:
                i.click(event)

        if time.process_time()-timeStart>0.01:
            logic()
            timeStart = time.process_time()
        

def import_param() -> None:
    print()

def export_param() -> None:
    print()


def start():
    surface = create_example_window('Projekt - Liszaj', (1080, 720))
    Model.menu = pygame_menu.Menu(
    height=720,
    theme=pygame_menu.themes.THEME_BLUE,
    title='Smacznej kawusi',
    width=1080
    )

    Model.param_size = [[10, 100], [20, 50], [40, 25], [50, 20], [100, 10], [200, 5]] 

    Model.simulation_name = Model.menu.add.text_input('Nazwa symulacji: ', default='liszaj01', maxchar=36)
    Model.diff = Model.menu.add.selector('Tempo propagacji choroby: ', [('Powoli', 1), ('Umiarkowanie', 2), ('Szybko (OSTROŻNIE)', 3)], onchange=set_difficulty)
    Model.size = Model.menu.add.selector('Wielkość powierzchni skóry: ', [('10x10', 1), ('20x20', 2), ('40x40', 3), ('50x50', 4), ('100x100', 5), ('200x200', 6)], onchange=set_size)
    Model.prob = Model.menu.add.selector('Prawdopodobieństwo zakażenia: ', [('50%', 1), ('75%', 2), ('90%', 3), ('10%', 4), ('25%', 5)], onchange=set_probability)


    Model.menu.add.button('Rozpocznij', start_the_simulation)
    Model.menu.add.button('Wyjdź', pygame_menu.events.EXIT)
    Model.menu.add.button('Zaimportuj parametry', import_param)
    Model.menu.add.button('Wyeksportuj parametry', export_param)

    Model.menu.mainloop(surface)




buttons = []
buttons.append(Button(start, "Back to menu", 1350, 800, 200, 40, font=30, bg=(242, 255, 204)))
buttons.append(Button(sizeUp, "Size + 10", 1350, 600, 200, 40, font=30, bg=(242, 255, 204)))
buttons.append(Button(sizeDown, "Size - 10", 1350, 700, 200, 40, font=30, bg=(242, 255, 204)))
buttons.append(Button(reset, "Reset", 1350, 500, 200, 40, font=30, bg=(242, 255, 204)))
buttons.append(Button(clear, "Clear", 1350, 400, 200, 40, font=30, bg=(242, 255, 204)))

start()