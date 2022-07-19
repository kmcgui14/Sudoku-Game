import pygame
import pygame_menu
from pygame_menu.examples import create_example_window
from typing import Tuple, Any
import requests

bg_color = (251, 247, 245)
pygame.init()
window = pygame.display.set_mode((550,550))
pygame.display.set_caption("Sudoku")
myfont = pygame.font.SysFont('Comic Sans MS', 35)
surface = create_example_window('Sudoku', (550, 550))

original_grid_element_color = (52, 31, 151)
buffer = 5

response = ""
grid = ""
grid_original = ""
difficulty = [1]

def set_difficulty(selected: Tuple, value: Any):
    """
    Set the difficulty of the game.
    """

    difficulty[0] = value

def insert(window, position):
    i,j = position[1], position[0]
    myfont = pygame.font.SysFont('Comic Sans MS', 35)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if(grid_original[i-1][j-1] != 0):
                    return
                if(event.key == 48): #checking with 0
                    grid[i-1][j-1] = event.key - 48
                    pygame.draw.rect(window, bg_color, (position[0]*50 + buffer, position[1]*50+ buffer,50 -2*buffer , 50 - 2*buffer))
                    pygame.display.update()
                    return
                if(0 < event.key - 48 <10):  #We are checking for valid input
                    pygame.draw.rect(window, bg_color, (position[0]*50 + buffer, position[1]*50+ buffer,50 -2*buffer , 50 - 2*buffer))
                    value = myfont.render(str(event.key-48), True, (0,0,0))
                    window.blit(value, (position[0]*50 +15, position[1]*50))
                    grid[i-1][j-1] = event.key - 48
                    pygame.display.update()
                    return
                return

def start_the_game():
    window.fill(bg_color)

    # change difficulty
    if (difficulty[0] == 1):
        pygame.display.set_caption("Sudoku - Easy")
        response = requests.get("https://sugoku.herokuapp.com/board?difficulty=easy", verify=False)
    if (difficulty[0] == 2):
        pygame.display.set_caption("Sudoku - Medium")
        response = requests.get("https://sugoku.herokuapp.com/board?difficulty=medium", verify=False)
    if (difficulty[0] == 3):
        pygame.display.set_caption("Sudoku - Hard")
        response = requests.get("https://sugoku.herokuapp.com/board?difficulty=hard", verify=False)
    
    grid = response.json()['board']
    grid_original = [[grid[x][y] for y in range(len(grid[0]))] for x in range(len(grid))]


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
    
    for i in range(0, len(grid[0])):
        for j in range(0, len(grid[0])):
            if(0<grid[i][j]<10):
                value = myfont.render(str(grid[i][j]), True, original_grid_element_color)
                window.blit(value, ((j+1)*50 + 15, (i+1)*50 ))
    pygame.display.update()

    # main game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = pygame.mouse.get_pos()
                insert(window, (pos[0]//50, pos[1]//50))
            if event.type == pygame.QUIT:
                pygame.quit()
                return


menu = pygame_menu.Menu(
    height=300,
    theme=pygame_menu.themes.THEME_BLUE,
    title='Sudoku',
    width=400
)

menu.add.button('Play', start_the_game)
menu.add.selector('Difficulty: ', [('Easy', 1), ('Medium', 2), ('Hard', 3)], onchange=set_difficulty)
menu.add.button('Quit', pygame_menu.events.EXIT)

if __name__ == '__main__':
    menu.mainloop(surface)