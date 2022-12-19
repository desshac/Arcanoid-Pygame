import pygame

pygame.init()

screen_width = 600
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Arcanoid')

bg = ("#DDBEAA")
# blocks color
block_red = ("#BBC6C8")
block_green = ("#5BA199")
block_blue = ("#469597")

red_shadow = ("#839295")
green_shadow = ("#4A847E")
blue_shadow = ("#367B7D")

cols = 6
rows = 6


class wall():
    def __init__(self):
        self.width = screen_width // cols
        self.height = 50

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
                    block_col = block_blue
                    shadow = blue_shadow
                elif block[2] == 2:
                    block_col = block_green
                    shadow = green_shadow
                elif block[2] == 1:
                    block_col = block_red
                    shadow = red_shadow
                pygame.draw.rect(screen, shadow, block[1])
                pygame.draw.rect(screen, block_col, block[0])


wall = wall()
wall.create_wall()

run = True
while run:
    screen.fill(bg)
    wall.draw_wall()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()

pygame.quit()
