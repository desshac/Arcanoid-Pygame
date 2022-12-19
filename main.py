import pygame
import sys


def terminate():
    pygame.quit()
    sys.exit()


pygame.init()

screen_width = 800
screen_height = 800

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Arcanoid')
# bg color
bg = ("#DDBEAA")
# blocks color
block_red = ("#BBC6C8")
block_green = ("#5BA199")
block_blue = ("#469597")
# shadow color
red_shadow = ("#839295")
green_shadow = ("#467974")
blue_shadow = ("#347476")

cols = 6
rows = 6


class wall:
    def __init__(self):
        self.width = screen_width // cols
        self.height = 60

    def create_wall(self):
        self.blocks = []
        block = []
        for row in range(rows):
            block_row = []
            for col in range(cols):
                block_x = col * self.width
                block_y = row * self.height
                rect = pygame.Rect(block_x + 2, block_y + 2, self.width - 4, self.height - 4)
                shadow = pygame.Rect(block_x + 2, block_y + 2, self.width - 2, self.height - 2)
                if row < 2:
                    strength = 3
                elif row < 4:
                    strength = 2
                elif row < 6:
                    strength = 1
                block = [rect, shadow, strength]
                block_row.append(block)
            self.blocks.append(block_row)

    def draw_wall(self):
        for row in self.blocks:
            for block in row:
                if block[2] == 3:
                    col = block_blue
                    shadow = blue_shadow
                elif block[2] == 2:
                    col = block_green
                    shadow = green_shadow
                elif block[2] == 1:
                    col = block_red
                    shadow = red_shadow
                pygame.draw.rect(screen, shadow, block[1])
                pygame.draw.rect(screen, col, block[0])


wall = wall()
wall.create_wall()

running = True
while running:

    screen.fill((bg))

    wall.draw_wall()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

terminate()
