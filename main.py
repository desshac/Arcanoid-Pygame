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
platform_color = ("#E5E3E4")
# shadow color
red_shadow = ("#839295")
green_shadow = ("#4A847E")
blue_shadow = ("#367B7D")
platform_shadow = ("#C1C1C1")

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


class platform:
    def __init__(self):
        self.pl_width = 200
        self.pl_height = 30
        pl_x = screen_width // 2 - self.pl_width // 2
        pl_y = screen_height - 60
        self.platform = pygame.Rect(pl_x + 2, pl_y + 2, self.pl_width - 2, self.pl_height - 2)
        self.shadow = pygame.Rect(pl_x, pl_y, self.pl_width + 2, self.pl_height + 2)
        self.speed = 15

    def draw_platform(self):
        pygame.draw.rect(screen, platform_shadow, self.shadow)
        pygame.draw.rect(screen, platform_color, self.platform)

    def update_platform(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_RIGHT] and self.shadow.right < screen_width - 5:
            self.platform = self.platform.move(self.speed, 0)
            self.shadow = self.shadow.move(self.speed, 0)
        if key[pygame.K_LEFT] and self.shadow.left > 5:
            self.platform = self.platform.move(-self.speed, 0)
            self.shadow = self.shadow.move(-self.speed, 0)



wall = wall()
wall.create_wall()

platform = platform()

FPS = 30
clock = pygame.time.Clock()

run = True
while run:
    screen.fill(bg)
    wall.draw_wall()
    platform.draw_platform()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        '''if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                platform.update_platform('right')
            if event.key == pygame.K_LEFT:
                platform.update_platform('left')'''
    platform.update_platform()
    clock.tick(FPS)
    pygame.display.update()

pygame.quit()
