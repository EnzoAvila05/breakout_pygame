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

# Dimensões da tela ajustadas para uma altura maior
WIDTH = 700
HEIGHT = 850
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout")

# Definir o FPS
FPS = 60
clock = pygame.time.Clock()

# Fonte para o placar
font = pygame.font.Font(None, 74)

# Tamanho da raquete
paddle_width = 100
paddle_height = 10
paddle_x = (WIDTH - paddle_width) // 2
paddle_y = HEIGHT - 50
paddle_speed = 10

# Bola
ball_size = 20
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_speed_x = random.choice([-4, 4])
ball_speed_y = -5
ball_return = False

# Placar e vidas
score1 = 0
lifes = 3

# Blocos
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

# Função para desenhar a raquete
def draw_paddle():
    pygame.draw.rect(screen, BLUE, (paddle_x, paddle_y, paddle_width, paddle_height))

# Função para desenhar a bola
def draw_ball():
    pygame.draw.rect(screen, WHITE, (ball_x, ball_y, ball_size, ball_size))

# Função para desenhar os blocos
def draw_blocks():
    for row in blocks:
        for block, color in row:
            pygame.draw.rect(screen, color, block)

# Função para desenhar o placar
def draw_score():
    score1_surface = font.render(f"{score1:03}", True, WHITE)
    lifes_surface = font.render(f"{lifes:03}", True, WHITE)
    screen.blit(score1_surface, (50, 20))
    screen.blit(lifes_surface, (WIDTH - 150, 20))

count_hits = 0 # contador de acertos

# Função para detectar colisão com a raquete
def ball_collide_paddle():
    return pygame.Rect(paddle_x, paddle_y, paddle_width, paddle_height).colliderect(pygame.Rect(ball_x, ball_y, ball_size, ball_size))

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
    if ball_x <= 0 or ball_x >= WIDTH - ball_size:
        ball_speed_x = -ball_speed_x
    if ball_y <= 0:
        ball_speed_y = -ball_speed_y

    # Colisão com a raquete
    if ball_collide_paddle():
        ball_return = False
        ball_speed_y = -ball_speed_y
        count_hits += 1
        if count_hits == 4 or count_hits == 12:
            ball_speed_y *= 1.5

    # Colisão com o chão (perde vida)
    if ball_y >= HEIGHT:
        lifes -= 1  # Perde uma vida
        if lifes > 0:
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
            if block_rect.colliderect(pygame.Rect(ball_x, ball_y, ball_size, ball_size)) and not ball_return:
                row.remove(block)
                ball_speed_y = -ball_speed_y
                ball_return = True
                
                # Valor da pontuação em cada bloco
                if block[1] == YELLOW:
                    score1 += 1
                if block[1] == GREEN:
                    score1 += 3
                if block[1] == ORANGE:
                    score1 += 5
                if block[1] == RED:
                    score1 += 7

                break

    # Desenhar a tela
    screen.fill(BLACK)
    draw_paddle()
    draw_ball()
    draw_blocks()
    draw_score()

    # Atualizar a tela
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
