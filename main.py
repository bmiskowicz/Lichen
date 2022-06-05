import pygame
import pygame_menu
import numpy
import random
import time

from pygame_menu.examples import create_example_window

from typing import Tuple, Any

surface = create_example_window('Projekt - Liszaj', (1080, 720))


class Model:
    running = True
    param_size = [[10, 100], [25, 40], [50, 20], [100, 10], [250, 4], [500, 2]] #number of points and pixels
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
    """
    Set the difficulty of the simulation.
    """
    print(f'Set difficulty to {selected[0]} ({value})')


def set_probability(selected: Tuple, value: Any) -> None:
    """
    Set the size of the simulation.
    """
    print(f'Set size to {selected[0]} ({value})')


def set_size(selected: Tuple, value: Any) -> None:
    """
    Set the size of the simulation.
    """
    print(f'Set size to {selected[0]} ({value})')


def logic(size):
    "main logic of the simulation"
    buttonMenu.show()

    k = 0
    l = 0
    # drawing the cells
    for i in range(10, Model.param_size[size][1] * Model.param_size[size][0], Model.param_size[size][1] + 1):
        for j in range(10, Model.param_size[size][1] * Model.param_size[size][0], Model.param_size[size][1] + 1):
            if(Model.tab[0][k][l]==0):
                pygame.draw.rect(surface, "yellow", pygame.Rect(i, j, Model.param_size[size][1], Model.param_size[size][1]))
            if (Model.tab[0][k][l] == 1):
                pygame.draw.rect(surface, "red", pygame.Rect(i, j, Model.param_size[size][1], Model.param_size[size][1]))
            if (Model.tab[0][k][l] == 2):
                pygame.draw.rect(surface, "grey", pygame.Rect(i, j, Model.param_size[size][1], Model.param_size[size][1]))
            l=l+1
        k=k+1
        l=0
    k=0

    pygame.display.flip()


    i = 0
    j = 0
    # drawing the cells
    newtab = Model.tab.copy()
    for i in range(0, Model.param_size[size][0]):
        for j in range(0, Model.param_size[size][0]):
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
                    if i%Model.param_size[size][0]!=Model.param_size[size][0]-1: 
                        if(Model.tab[0][i+1][j]==0): neighbours.append([i+1,j])

                    if i%Model.param_size[size][0]!=0:
                        if(Model.tab[0][i-1][j]==0): neighbours.append([i-1,j])

                    if j>0:
                        if(Model.tab[0][i][j-1]==0): neighbours.append([i,j-1])

                    if j<Model.param_size[size][0]-1:
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
    diff = Model.diff.get_value()[1]
    size = Model.size.get_value()[1]
    prob = Model.prob.get_value()[1]
    simulation_name = Model.simulation_name.get_value()

    #creating the window
    background_colour = (0, 204, 153)
    (width, height) = (1920, 1080)
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption(simulation_name)
    screen.fill(background_colour)

    #parameters for simulation
    Model.tab = numpy.zeros((2, Model.param_size[size][0], Model.param_size[size][0]))
    Model.tab[0][int(Model.param_size[size][0]/2)][int(Model.param_size[size][0]/2)] = 1  #tab[0][]][] - table of states
    Model.tab[1][int(Model.param_size[size][0]/2)][int(Model.param_size[size][0]/2)] = 2  #tab[0][]][] - table of remaining times
    
    logic(size)

    #getting windows events
    timeStart = time.process_time()
    Model.running =True
    buttonMenu.show()
    while Model.running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Model.running = False
            buttonMenu.click(event)

        if time.process_time()-timeStart>1:
            logic(size)
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

    Model.simulation_name = Model.menu.add.text_input('Nazwa symulacji: ', default='liszaj01', maxchar=36)
    Model.diff = Model.menu.add.selector('Tempo propagacji choroby: ', [('Powoli', 1), ('Umiarkowanie', 2), ('Szybko (OSTROŻNIE)', 3)], onchange=set_difficulty)
    Model.size = Model.menu.add.selector('Wielkość powierzchni skóry: ', [('10x10', 1), ('25x25', 2), ('50x50', 3), ('100x100', 4), ('250x250', 5), ('500x500', 6)], onchange=set_size)
    Model.prob = Model.menu.add.selector('Prawdopodobieństwo zakażenia: ', [('10%', 1), ('25%', 2), ('50%', 3), ('75%', 4), ('90%', 5)], onchange=set_probability)


    Model.menu.add.button('Rozpocznij', start_the_simulation)
    Model.menu.add.button('Wyjdź', pygame_menu.events.EXIT)
    Model.menu.add.button('Zaimportuj parametry', import_param)
    Model.menu.add.button('Wyeksportuj parametry', export_param)

    Model.menu.mainloop(surface)


buttonMenu = Button(start, "Back to menu", 1350, 800, 200, 40, font=30, bg=(242, 255, 204))

start()