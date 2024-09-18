import pygame
import random

# Inicializar o Pygame
pygame.init()

# Definir as cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Dimensões da tela
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
ball_radius = 10
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_speed_x = random.choice([-4, 4])
ball_speed_y = -4

# Placar
score1 = 17  # Exemplificando a pontuação da imagem
score2 = 0

# Blocos
block_rows = 5
block_cols = 14
block_width = WIDTH // block_cols
block_height = 30

# Definindo os blocos com as cores em estilo arcade (verde, amarelo, vermelho)
blocks = []
for row in range(block_rows):
    block_row = []
    for col in range(block_cols):
        block_x = col * block_width
        block_y = row * block_height + 100  # Ajuste para dar espaço ao placar
        if row < 2:
            block_color = RED
        elif row < 4:
            block_color = YELLOW
        else:
            block_color = GREEN
        block_rect = pygame.Rect(block_x, block_y, block_width, block_height)
        block_row.append((block_rect, block_color))
    blocks.append(block_row)

# Função para desenhar a raquete
def draw_paddle():
    pygame.draw.rect(screen, WHITE, (paddle_x, paddle_y, paddle_width, paddle_height))

# Função para desenhar a bola
def draw_ball():
    pygame.draw.circle(screen, WHITE, (ball_x, ball_y), ball_radius)

# Função para desenhar os blocos
def draw_blocks():
    for row in blocks:
        for block, color in row:
            pygame.draw.rect(screen, color, block)

# Função para desenhar o placar
def draw_score():
    score1_surface = font.render(f"{score1:03}", True, WHITE)
    score2_surface = font.render(f"{score2:03}", True, WHITE)
    screen.blit(score1_surface, (50, 20))
    screen.blit(score2_surface, (WIDTH - 150, 20))

# Função para detectar colisão com a raquete
def ball_collide_paddle():
    return pygame.Rect(paddle_x, paddle_y, paddle_width, paddle_height).collidepoint(ball_x, ball_y + ball_radius)

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
    if ball_x <= ball_radius or ball_x >= WIDTH - ball_radius:
        ball_speed_x = -ball_speed_x
    if ball_y <= ball_radius:
        ball_speed_y = -ball_speed_y

    # Colisão com a raquete
    if ball_collide_paddle():
        ball_speed_y = -ball_speed_y

    # Colisão com o chão (game over)
    if ball_y >= HEIGHT:
        print("Game Over")
        running = False

    # Colisão com os blocos
    for row in blocks:
        for block, color in row:
            if block.collidepoint(ball_x, ball_y - ball_radius):
                blocks.remove(row)
                ball_speed_y = -ball_speed_y
                break

    # Desenhar a tela
    screen.fill(BLACK)
    draw_paddle()
    draw_ball()
    draw_blocks()
    draw_score()  # Desenha o placar

    # Atualizar a tela
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
