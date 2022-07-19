import pygame
import pygame_menu
from pygame_menu.examples import create_example_window
from typing import Tuple, Any
import requests

bg_color = (251, 247, 245)
pygame.init()
window = pygame.display.set_mode((550,550))
pygame.display.set_caption("Sudoku")
surface = create_example_window('Sudoku', (550, 550))


def set_difficulty(selected: Tuple, value: Any) -> None:
    """
    Set the difficulty of the game.
    """
    print(f'Set difficulty to {selected[0]} ({value})')


def start_the_game():
    # setup
    window.fill(bg_color)

    # displaying grid
    for i in range(0,10):
        if(i % 3 == 0):
            # thicker lines for border
            pygame.draw.line(window, (0,0,0), (50 + 50*i, 50), (50 + 50*i, 500), 4)
            pygame.draw.line(window, (0,0,0), (50, 50 + 50*i), (500, 50 + 50*i), 4)

        # main board lines
        pygame.draw.line(window, (0,0,0), (50 + 50*i, 50), (50 + 50*i, 500), 2)
        pygame.draw.line(window, (0,0,0), (50, 50 + 50*i), (500, 50 + 50*i), 2)
    pygame.display.update()
    

    # main game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return


menu = pygame_menu.Menu(
    height=300,
    theme=pygame_menu.themes.THEME_BLUE,
    title='Welcome',
    width=400
)

menu.add.button('Play', start_the_game)
menu.add.selector('Difficulty: ', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
menu.add.button('Quit', pygame_menu.events.EXIT)

if __name__ == '__main__':
    menu.mainloop(surface)