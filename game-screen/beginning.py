import pygame
import random

# Inicializar o Pygame
pygame.init()

# Definir as cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)

# Dimensões da tela ajustadas para uma altura maior
WIDTH = 700
HEIGHT = 850
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout")

# Definir o FPS
FPS = 60
clock = pygame.time.Clock()

# Tamanho da raquete
paddle_width = 50
paddle_height = 20
paddle_x = (WIDTH - paddle_width) // 2
paddle_y = HEIGHT - 80
paddle_speed = 12

# Bola
ball_size = 10
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_speed_x = random.choice([-4, 4])
ball_speed_y = -4
ball_return = False

# Placar e vidas
score = 0
lifes_start = 1
LIFES_MAX = 4

# Blocos
block_rows = 8
block_columns = 14
block_width = (WIDTH - (block_columns - 1) * 5) // block_columns
block_height = 15
column_spacing = 5
row_spacing = 5
block_colors = [RED, RED, ORANGE, ORANGE, GREEN, GREEN, YELLOW, YELLOW]
wall_width = 15

# sounds
brick_sound = pygame.mixer.Sound('sounds/soundsbrick.wav')
paddle_sound = pygame.mixer.Sound('sounds/soundspaddle.wav')
wall_sound = pygame.mixer.Sound('sounds/soundswall.wav')

blocks = []
for row in range(block_rows):
    block_row = []
    for col in range(block_columns):
        block_x = col * (block_width + column_spacing)
        block_y = row * (block_height + row_spacing) + 170
        block_color = block_colors[row]
        block_rect = pygame.Rect(block_x, block_y, block_width, block_height)
        block_row.append((block_rect, block_color))
    blocks.append(block_row)

# Função para desenhar a raquete
def draw_paddle():
    pygame.draw.rect(screen, BLUE, (paddle_x, paddle_y, paddle_width, paddle_height))

# Função para desenhar a bola
def draw_ball():
    pygame.draw.rect(screen, WHITE, (ball_x, ball_y, ball_size + 5 , ball_size))

# Função para desenhar os blocos
def draw_blocks():
    for row in blocks:
        for block, color in row:
            pygame.draw.rect(screen, color, block)

# Função para desenhar o placar
def draw_score():
    font = pygame.font.Font('text_style/SFProverbialGothic-Bold.ttf', 80)
    text = font.render(str(f"{score:03}"), 0, WHITE)
    screen.blit(text, (90, 100))
    text = font.render(str(lifes_start), 0, WHITE)
    screen.blit(text, (400, 40))
    text = font.render('000', 0, WHITE)
    screen.blit(text, (440, 100))
    text = font.render('1', 0, WHITE)
    screen.blit(text, (60, 40))

# Função para detectar colisão com a raquete
def ball_collide_paddle():
    return (pygame.Rect(paddle_x, paddle_y, paddle_width, paddle_height)
            .colliderect(pygame.Rect(ball_x, ball_y, ball_size + 5, ball_size)))

# Função principal do jogo
running = True
while running:
    # Eventos do jogo
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movimentação da raquete
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle_x > 0:
        paddle_x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle_x < WIDTH - paddle_width:
        paddle_x += paddle_speed

    # Movimentação da bola
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Colisão com as paredes
    if ball_x <= 0 + wall_width or ball_x >= WIDTH - wall_width - ball_size :
        ball_speed_x = -ball_speed_x
        wall_sound.play()
    if ball_y + wall_width <= 0 - wall_width:
        ball_speed_y = -ball_speed_y
        wall_sound.play()

    # Colisão com a raquete
    if ball_collide_paddle():
        paddle_sound.play()
        ball_return = False
        ball_speed_y = -ball_speed_y

    # Colisão com o chão (perde vida)
    if ball_y >= HEIGHT:
        lifes_start += 1  # Perde uma vida
        if lifes_start != LIFES_MAX:
            # Reiniciar a bola se ainda houver vidas
            ball_x = WIDTH // 2
            ball_y = HEIGHT // 2
            ball_speed_x = random.choice([-4, 4])
            ball_speed_y = -7
            ball_return = False
        else:
            # Game Over quando as vidas acabarem
            print("Game Over")
            running = False

    # Colisão com os blocos (apagar apenas o bloco atingido)
    for row in blocks:
        for block in row:
            block_rect = block[0]  # Acessa o retângulo do bloco (primeiro item da tupla)
            if block_rect.collidepoint(ball_x, ball_y ) and not ball_return:
                row.remove(block)
                brick_sound.play()
                ball_speed_y = -ball_speed_y
                ball_return = True
                # Valor da pontuação em cada bloco
                if block[1] == YELLOW:
                    score += 1
                if block[1] == GREEN:
                    score += 3
                if block[1] == ORANGE:
                    score += 5
                if block[1] == RED:
                    score += 7
                break

    # Desenhar a tela
    screen.fill(BLACK)
    draw_paddle()
    draw_ball()
    draw_blocks()
    draw_score()

    # walls
    pygame.draw.line(screen, GREY, [0, 17], [WIDTH, 17], 40)  # Top
    pygame.draw.line(screen, GREY, [(wall_width / 2) - 1, 0], [(wall_width / 2) - 1, HEIGHT], wall_width)  # Left wall
    pygame.draw.line(screen, GREY, [(WIDTH - wall_width / 2) , 0], [(WIDTH - wall_width / 2) , HEIGHT],wall_width)  # Right wall

    # blue wall elements
    pygame.draw.line(screen, BLUE, [(wall_width / 2) - 1, HEIGHT - 70 + paddle_height / 2 - 54 / 2],[(wall_width / 2) - 1, HEIGHT - 90 + paddle_height / 2 - 54 / 2 + 54], wall_width)  # left
    pygame.draw.line(screen, BLUE, [(WIDTH - wall_width / 2) , HEIGHT - 70 + paddle_height / 2 - 54 / 2],[(WIDTH - wall_width / 2) , HEIGHT - 90 + paddle_height / 2 - 54 / 2 + 54], wall_width)  # right

    # red wall elements
    pygame.draw.line(screen, RED, [(wall_width / 2) - 1, 165],[(wall_width / 2) - 1, 165 + 2 * block_height + 2 * column_spacing], wall_width)  # left
    pygame.draw.line(screen, RED, [(WIDTH - wall_width / 2) , 165],[(WIDTH - wall_width / 2) , 165 + 2 * block_height + 2 * column_spacing], wall_width)  # right

    # orange wall elements
    pygame.draw.line(screen, ORANGE, [(wall_width / 2) - 1, 165 + 2 * block_height + 2 * column_spacing],[(wall_width / 2) - 1, 165 + 4 * block_height + 4 * column_spacing], wall_width)  # left
    pygame.draw.line(screen, ORANGE, [(WIDTH - wall_width / 2) , 165 + 2 * block_height + 2 * column_spacing],[(WIDTH - wall_width / 2) , 165 + 4 * block_height + 4 * column_spacing], wall_width)  # right

    # green wall elements
    pygame.draw.line(screen, GREEN, [(wall_width / 2) - 1, 165 + 4 * block_height + 4 * column_spacing],[(wall_width / 2) - 1, 165 + 6 * block_height + 6 * column_spacing], wall_width)  # left
    pygame.draw.line(screen, GREEN, [(WIDTH - wall_width / 2) , 165 + 4 * block_height + 4 * column_spacing],[(WIDTH - wall_width / 2) , 165 + 6 * block_height + 6 * column_spacing], wall_width)  # right

    # yellow wall elements
    pygame.draw.line(screen, YELLOW, [(wall_width / 2) - 1, 165 + 6 * block_height + 6 * column_spacing],[(wall_width / 2) - 1, 165 + 8 * block_height + 8 * column_spacing], wall_width)  # left
    pygame.draw.line(screen, YELLOW, [(WIDTH - wall_width / 2) , 165 + 6 * block_height + 6 * column_spacing],[(WIDTH - wall_width / 2) , 165 + 8 * block_height + 8 * column_spacing], wall_width)  # right


    # Atualizar a tela
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()