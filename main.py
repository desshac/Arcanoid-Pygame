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
ball_color = (0, 0, 0)
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
        self.pl_x = screen_width // 2 - self.pl_width // 2
        self.pl_y = screen_height - 60
        self.platform = pygame.Rect(self.pl_x + 2, self.pl_y + 2, self.pl_width - 2, self.pl_height - 2)
        self.shadow = pygame.Rect(self.pl_x, self.pl_y, self.pl_width + 2, self.pl_height + 2)
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


class ball:
    def __init__(self, x, y):
        self.ball_radius = 15
        self.x = x - self.ball_radius
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, self.ball_radius * 2, self.ball_radius * 2)
        self.speed_x = 4
        self.speed_y = -4

    def draw_ball(self):
        pygame.draw.circle(screen, platform_shadow, (self.rect.x + self.ball_radius, self.rect.y + self.ball_radius),
                           self.ball_radius + 2)
        pygame.draw.circle(screen, platform_color, (self.rect.x + self.ball_radius, self.rect.y + self.ball_radius),
                           self.ball_radius)


wall = wall()
wall.create_wall()

platform = platform()

ball = ball(platform.pl_x + (platform.pl_width // 2), platform.pl_y - platform.pl_height)

FPS = 30
clock = pygame.time.Clock()

ball_running = False
run = True
while run:
    screen.fill(bg)
    wall.draw_wall()
    platform.draw_platform()
    ball.draw_ball()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    platform.update_platform()
    clock.tick(FPS)
    pygame.display.update()

pygame.quit()
