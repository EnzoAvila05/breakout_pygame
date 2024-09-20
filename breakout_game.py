import pygame
import random

# Initialize Pygame
pygame.init()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)

# Screen dimensions adjusted for greater height
WIDTH = 700
HEIGHT = 850
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout")

# Define FPS
FPS = 60
clock = pygame.time.Clock()

# Font for score
font = pygame.font.Font(None, 74)

# Paddle size
paddle_width = 100
paddle_height = 10
paddle_x = (WIDTH - paddle_width) // 2
paddle_y = HEIGHT - 50
paddle_speed = 10

# Ball
ball_size = 20
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_speed_x = random.choice([-4, 4])
ball_speed_y = -5
ball_return = False

# Score and lives
score1 = 0
lifes = 3

# Blocks
block_rows = 8
block_columns = 14
block_width = (WIDTH - (block_columns - 1) * 5) // block_columns
block_height = 15
column_spacing = 5
row_spacing = 5
block_colors = [RED, RED, ORANGE, ORANGE, GREEN, GREEN, YELLOW, YELLOW]

blocks = []
for row in range(block_rows):
    block_row = []
    for col in range(block_columns):
        block_x = col * (block_width + column_spacing)
        block_y = row * (block_height + row_spacing) + 125
        block_color = block_colors[row]
        block_rect = pygame.Rect(block_x, block_y, block_width, block_height)
        block_row.append((block_rect, block_color))
    blocks.append(block_row)


# Function to draw the paddle
def draw_paddle():
    pygame.draw.rect(screen, BLUE, (paddle_x, paddle_y, paddle_width, paddle_height))


# Function to draw the ball
def draw_ball():
    pygame.draw.rect(screen, WHITE, (ball_x, ball_y, ball_size, ball_size))


# Function to draw the blocks
def draw_blocks():
    for row in blocks:
        for block, color in row:
            pygame.draw.rect(screen, color, block)


# Function to draw the score
def draw_score():
    score1_surface = font.render(f"{score1:03}", True, WHITE)
    lifes_surface = font.render(f"{lifes:03}", True, WHITE)
    screen.blit(score1_surface, (50, 20))
    screen.blit(lifes_surface, (WIDTH - 150, 20))


count_hits = 0  # hit counter


# Function to detect collision with the paddle
def ball_collide_paddle():
    return pygame.Rect(paddle_x, paddle_y, paddle_width, paddle_height).colliderect(
        pygame.Rect(ball_x, ball_y, ball_size, ball_size))


# Main game function
running = True
while running:
    # Game events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Paddle movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle_x > 0:
        paddle_x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle_x < WIDTH - paddle_width:
        paddle_x += paddle_speed

    # Ball movement
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Collision with walls
    if ball_x <= 0 or ball_x >= WIDTH - ball_size:
        ball_speed_x = -ball_speed_x
    if ball_y <= 0:
        ball_speed_y = -ball_speed_y

    # Collision with the paddle
    if ball_collide_paddle():
        ball_return = False
        ball_speed_y = -ball_speed_y
        count_hits += 1
        if count_hits == 4 or count_hits == 12:
            ball_speed_y *= 1.5

    # Collision with the floor (lose a life)
    if ball_y >= HEIGHT:
        lifes -= 1  # Lose a life
        if lifes > 0:
            # Reset the ball if there are lives left
            ball_x = WIDTH // 2
            ball_y = HEIGHT // 2
            ball_speed_x = random.choice([-4, 4])
            ball_speed_y = -7
            ball_return = False
        else:
            # Game Over when lives are finished
            print("Game Over")
            running = False

    # Collision with blocks (remove only the hit block)
    for row in blocks:
        for block in row:
            block_rect = block[0]  # Access the block rectangle (first item in tuple)
            if block_rect.colliderect(pygame.Rect(ball_x, ball_y, ball_size, ball_size)) and not ball_return:
                row.remove(block)
                ball_speed_y = -ball_speed_y
                ball_return = True

                # Value of points for each block
                if block[1] == YELLOW:
                    score1 += 1
                if block[1] == GREEN:
                    score1 += 3
                if block[1] == ORANGE:
                    score1 += 5
                if block[1] == RED:
                    score1 += 7

                break

    # Draw the screen
    screen.fill(BLACK)
    draw_paddle()
    draw_ball()
    draw_blocks()
    draw_score()

    # Update the screen
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
