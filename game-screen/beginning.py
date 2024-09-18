import pygame

pygame.init()

# screen definitions
WIDTH = 860
HEIGHT = 960
size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Breakout')

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

# paddle dimensions
paddle_width = 50
paddle_height = 25

# grouping sprites
all_sprites = pygame.sprite.Group()

# brick dimensions
brick_width = 50
brick_height = 25

# brick gaps
x_gap = 7
y_gap = 7
wall_width = 25

# game loop
game_loop = True
game_clock = pygame.time.Clock()
FPS = 60

while game_loop:
    game_clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_loop = False

    all_sprites.update()

    screen.fill(BLACK)

    # walls
    pygame.draw.line(screen, GREY, [0, 19], [WIDTH, 19], 40) # Top
    pygame.draw.line(screen, GREY, [(wall_width / 2) - 1, 0], [(wall_width / 2) - 1, HEIGHT], wall_width) # Left wall
    pygame.draw.line(screen, GREY, [(WIDTH - wall_width / 2) - 1, 0], [(WIDTH - wall_width / 2) - 1, HEIGHT], wall_width) # Right wall

    # blue wall elements
    pygame.draw.line(screen, BLUE, [(wall_width / 2) - 1, HEIGHT - 65 + paddle_height / 2 - 54 / 2],[(wall_width / 2) - 1, HEIGHT - 65 + paddle_height / 2 - 54 / 2 + 54], wall_width) # left
    pygame.draw.line(screen, BLUE, [(WIDTH - wall_width / 2) - 1, HEIGHT - 65 + paddle_height / 2 - 54 / 2],[(WIDTH - wall_width / 2) - 1, HEIGHT - 65 + paddle_height / 2 - 54 / 2 + 54], wall_width) # right

    # red wall elements
    pygame.draw.line(screen, RED, [(wall_width / 2) - 1, 212.5],[(wall_width / 2) - 1, 212.5 + 2 * brick_height + 2 * y_gap], wall_width) # left
    pygame.draw.line(screen, RED, [(WIDTH - wall_width / 2) - 1, 212.5],[(WIDTH - wall_width / 2) - 1, 212.5 + 2 * brick_height + 2 * y_gap], wall_width) # right

    # orange wall elements
    pygame.draw.line(screen, ORANGE, [(wall_width / 2) - 1, 212.5 + 2 * brick_height + 2 * y_gap],[(wall_width / 2) - 1, 212.5 + 4 * brick_height + 4 * y_gap], wall_width) # left
    pygame.draw.line(screen, ORANGE, [(WIDTH - wall_width / 2) - 1, 212.5 + 2 * brick_height + 2 * y_gap],[(WIDTH - wall_width / 2) - 1, 212.5 + 4 * brick_height + 4 * y_gap], wall_width) # right

    # green wall elements
    pygame.draw.line(screen, GREEN, [(wall_width / 2) - 1, 212.5 + 4 * brick_height + 4 * y_gap],[(wall_width / 2) - 1, 212.5 + 6 * brick_height + 6 * y_gap], wall_width) #left
    pygame.draw.line(screen, GREEN, [(WIDTH - wall_width / 2) - 1, 212.5 + 4 * brick_height + 4 * y_gap],[(WIDTH - wall_width / 2) - 1, 212.5 + 6 * brick_height + 6 * y_gap], wall_width) # right

    # yellow wall elements
    pygame.draw.line(screen, YELLOW, [(wall_width / 2) - 1, 212.5 + 6 * brick_height + 6 * y_gap],[(wall_width / 2) - 1, 212.5 + 8 * brick_height + 8 * y_gap], wall_width) #left
    pygame.draw.line(screen, YELLOW, [(WIDTH - wall_width / 2) - 1, 212.5 + 6 * brick_height + 6 * y_gap],[(WIDTH - wall_width / 2) - 1, 212.5 + 8 * brick_height + 8 * y_gap], wall_width) #right

    all_sprites.draw(screen)

    pygame.display.update()

pygame.quit()