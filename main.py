import pygame
import pygame_menu
import numpy

from pygame_menu.examples import create_example_window

from typing import Tuple, Any

surface = create_example_window('Projekt - Liszaj', (1080, 720))


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

def start_the_simulation() ->None:

    menu.disable()
    """
    main function of the simulation 
    """
    #getting the global variables
    global simulation_name, diff, size, prob
    diff = diff.get_value()[1]
    size = size.get_value()[1]
    prob = prob.get_value()[1]
    simulation_name = simulation_name.get_value()

    #creating the window
    background_colour = (255, 255, 255)
    (width, height) = (1920, 1080)
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption(simulation_name)
    screen.fill(background_colour)

    #parameters for simulation
    param_size = [[10, 100], [25, 40], [50, 20], [100, 10], [250, 4], [500, 2]]
    tab = numpy.zeros((2, param_size[size][0], param_size[size][0]))
    tab[0][int(param_size[size][0]/2)][int(param_size[size][0]/2)] = 1
    tab[0][int(param_size[size][0]/2)][int(param_size[size][0]/2)] = 3
    print(tab)

    #drawing the cells
    for i in range(10, param_size[size][1]*param_size[size][0], param_size[size][1]+1):
        for j in range(10, param_size[size][1]*param_size[size][0], param_size[size][1]+1):
            pygame.draw.rect(surface, "red", pygame.Rect(i, j, param_size[size][1], param_size[size][1]))
    pygame.display.flip()

    #getting windows events
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False




def import_param() -> None:
    print()

def export_param() -> None:
    print()

menu = pygame_menu.Menu(
    height=720,
    theme=pygame_menu.themes.THEME_BLUE,
    title='Smacznej kawusi',
    width=1080
)
simulation_name = menu.add.text_input('Nazwa symulacji: ', default='liszaj01', maxchar=36)
diff = menu.add.selector('Tempo propagacji choroby: ', [('Powoli', 1), ('Umiarkowanie', 2), ('Szybko (OSTROŻNIE)', 3)], onchange=set_difficulty)
size = menu.add.selector('Wielkość powierzchni skóry: ', [('10x10', 1), ('25x25', 2), ('50x50', 3), ('100x100', 4), ('250x250', 5), ('500x500', 6)], onchange=set_size)
prob = menu.add.selector('Prawdopodobieństwo zakażenia: ', [('10%', 1), ('25%', 2), ('50%', 3), ('75%', 4), ('90%', 5)], onchange=set_probability)


menu.add.button('Rozpocznij', start_the_simulation)
menu.add.button('Wyjdź', pygame_menu.events.EXIT)
menu.add.button('Zaimportuj parametry', import_param)
menu.add.button('Wyeksportuj parametry', export_param)

if __name__ == '__main__':
    menu.mainloop(surface)