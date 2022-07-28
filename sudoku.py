import pygame
import pygame_menu
from pygame_menu.examples import create_example_window
import pygame_menu.themes
from typing import Tuple, Any
import requests

bg_color = (178, 166, 141)
pygame.init()
window = pygame.display.set_mode((550,550))
pygame.display.set_caption("Sudoku")
myfont = pygame.font.SysFont('Comic Sans MS', 35)
surface = create_example_window('Sudoku', (550, 550))

original_grid_element_color = (145, 102, 66)
buffer = 5

diff = input("Select Difficulty(Easy,Medium,Hard): ")
url = "https://sugoku.herokuapp.com/board?difficulty=" + str(diff)
response = requests.get(url, verify=False)
grid = response.json()['board']
grid_original = [[grid[x][y] for y in range(len(grid[0]))] for x in range(len(grid))]
difficulty = [1]

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
                    value = myfont.render(str(event.key-48), True, (131, 108, 115))
                    window.blit(value, (position[0]*50 +15, position[1]*50))
                    grid[i-1][j-1] = event.key - 48
                    pygame.display.update()
                    return
                return

def start_the_game():
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


mytheme = pygame_menu.Theme(background_color=(209, 156, 76),
                title_background_color=(157, 95, 56))

menu = pygame_menu.Menu(
    height=300,
    theme=mytheme,
    title='Sudoku',
    width=400
)

menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)

if __name__ == '__main__':
    menu.mainloop(surface)