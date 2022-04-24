import pygame
import pygame_menu

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

def start_the_simulation() -> None:
    """
    Function that starts a simulation. This is raised by the menu button,
    here menu can be disabled, etc.
    """
    global simulation_name
    print(f'{simulation_name.get_value()}, Here will be the implementation of the simulation')
    menu.disable()

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
simulation_name = menu.add.text_input('Nazwa symulacji: ', default='liszaj01.txt', maxchar=16)
menu.add.selector('Tempo propagacji choroby: ', [('Powoli', 1), ('Umiarkowanie', 2), ('Szybko (OSTROŻNIE)', 3)], onchange=set_difficulty)
menu.add.selector('Wielkość powierzchni skóry: ', [('10x10', 1), ('25x25', 2), ('50x50', 3), ('100x100', 4), ('250x250', 5), ('500x500', 6)], onchange=set_size)
menu.add.selector('Prawdopodobieństwo zakażenia: ', [('10%', 1), ('25%', 2), ('50%', 3), ('75%', 4), ('90%', 5)], onchange=set_probability)
menu.add.button('Rozpocznij', start_the_simulation)
menu.add.button('Wyjdź', pygame_menu.events.EXIT)
menu.add.button('Zaimportuj parametry', import_param)
menu.add.button('Wyeksportuj parametry', export_param)

if __name__ == '__main__':
    menu.mainloop(surface)