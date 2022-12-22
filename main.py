import pygame
import sys

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


def terminate():
    pygame.quit()
    sys.exit()


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    return level_map


class wall():
    def __init__(self, level_map):
        self.width = screen_width // cols
        self.height = 50
        self.map = level_map

    def create_wall(self):
        self.blocks = []
        for row in range(len(self.map)):
            block_row = []
            strength = 1
            for col in range(len(self.map[row])):
                col_n = int(self.map[row][col])
                block_x = col * self.width
                block_y = row * self.height
                rect = pygame.Rect(block_x + 4, block_y + 4, self.width - 6, self.height - 6)
                shadow = pygame.Rect(block_x + 2, block_y + 2, self.width - 2, self.height - 2)
                if col_n == 3:
                    strength = 3
                elif col_n == 2:
                    strength = 2
                elif col_n == 1:
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
        self.direction = 0

    def draw_platform(self):
        pygame.draw.rect(screen, platform_shadow, self.shadow)
        pygame.draw.rect(screen, platform_color, self.platform)

    def update_platform(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_RIGHT] and self.shadow.right < screen_width - 5:
            self.platform = self.platform.move(self.speed, 0)
            self.shadow = self.shadow.move(self.speed, 0)
            self.direction = 1
        if key[pygame.K_LEFT] and self.shadow.left > 5:
            self.platform = self.platform.move(-self.speed, 0)
            self.shadow = self.shadow.move(-self.speed, 0)
            self.direction = -1


class ball:
    def __init__(self, x, y):
        self.ball_radius = 15
        self.x = x - self.ball_radius
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, self.ball_radius * 2, self.ball_radius * 2)
        self.speed_x = 5
        self.speed_y = -5
        self.speed = 15
        self.speed_max = 8
        self.game_over = 0

    def draw_ball(self):
        pygame.draw.circle(screen, platform_shadow, (self.rect.x + self.ball_radius, self.rect.y + self.ball_radius),
                           self.ball_radius + 2)
        pygame.draw.circle(screen, platform_color, (self.rect.x + self.ball_radius, self.rect.y + self.ball_radius),
                           self.ball_radius)

    def update_ball(self):

        collision = 5

        wall_destroyed = 0
        row_count = 0
        for row in wall.blocks:
            item_count = 0
            for item in row:
                if self.rect.colliderect(item[0]):
                    if abs(self.rect.bottom - item[0].top) < collision and self.speed_y > 0:
                        self.speed_y *= -1
                    if abs(self.rect.top - item[0].bottom) < collision and self.speed_y < 0:
                        self.speed_y *= -1
                    if abs(self.rect.right - item[0].left) < collision and self.speed_x > 0:
                        self.speed_x *= -1
                    if abs(self.rect.left - item[0].right) < collision and self.speed_x < 0:
                        self.speed_x *= -1

                    if wall.blocks[row_count][item_count][2] > 1:
                        wall.blocks[row_count][item_count][2] -= 1
                    else:
                        wall.blocks[row_count][item_count][0] = pygame.Rect(0, 0, 0, 0)
                        wall.blocks[row_count][item_count][1] = pygame.Rect(0, 0, 0, 0)
                item_count += 1
            row_count += 1

        if not ball_running:
            key = pygame.key.get_pressed()
            if key[pygame.K_RIGHT] and self.rect.right < screen_width - 5:
                self.rect = self.rect.move(self.speed, 0)
            if key[pygame.K_LEFT] and self.rect.left > 5:
                self.rect = self.rect.move(-self.speed, 0)
        else:
            if self.rect.left < 0 or self.rect.right > screen_width:
                self.speed_x *= -1
            if self.rect.top < 0:
                self.speed_y *= -1

            if self.rect.bottom > screen_height:
                self.game_over = -1

            if self.rect.colliderect(platform.platform):
                if abs(self.rect.bottom - platform.platform.top) < collision and self.speed_y > 0:
                    self.speed_y *= -1
                    self.speed_x += platform.direction
                    if self.speed_x > self.speed_max:
                        self.speed_x = self.speed_max
                    elif self.speed_x < 0 and self.speed_x < -self.speed_max:
                        self.speed_x = -self.speed_max
                else:
                    self.speed_x *= -1
            self.rect = self.rect.move(self.speed_x, self.speed_y)

            return self.game_over


level_map = load_level('lvl1.txt')

wall = wall(level_map)
wall.create_wall()

platform = platform()

ball = ball(platform.pl_x + (platform.pl_width // 2), platform.pl_y - platform.pl_height)

FPS = 60
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
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if not ball_running:
                ball_running = True
    platform.update_platform()
    game_over = ball.update_ball()
    if game_over == -1:
        print('game_over')
        terminate()
    elif game_over == 1:
        print('you win')
        terminate()
    clock.tick(FPS)
    pygame.display.update()

pygame.quit()
