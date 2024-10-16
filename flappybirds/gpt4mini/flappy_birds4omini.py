import pygame
import random

# Inicjalizacja Pygame
pygame.init()

# Ustawienia okna gry
WIDTH, HEIGHT = 400, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Ustawienia gracza
bird_width, bird_height = 34, 24
bird_x = 50
bird_y = HEIGHT // 2
bird_velocity = 0
gravity = 0.5
flap_power = -10

# Ustawienia rur
pipe_width = 80
pipe_height = random.randint(100, 400)
pipe_gap = 150
pipe_x = WIDTH

# Zmienna do kontrolowania gry
clock = pygame.time.Clock()
running = True
score = 0

def draw_bird(x, y):
    pygame.draw.rect(win, GREEN, (x, y, bird_width, bird_height))

def draw_pipe(x, height):
    pygame.draw.rect(win, GREEN, (x, 0, pipe_width, height))
    pygame.draw.rect(win, GREEN, (x, height + pipe_gap, pipe_width, HEIGHT))

while running:
    clock.tick(30)
    win.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_velocity = flap_power

    # Ruch ptaka
    bird_velocity += gravity
    bird_y += bird_velocity

    # Rysowanie ptaka
    draw_bird(bird_x, bird_y)

    # Rysowanie rur
    draw_pipe(pipe_x, pipe_height)

    # Ruch rur
    pipe_x -= 5
    if pipe_x < -pipe_width:
        pipe_x = WIDTH
        pipe_height = random.randint(100, 400)
        score += 1

    # Kolizje
    if (bird_y < 0 or bird_y > HEIGHT - bird_height) or (pipe_x < bird_x + bird_width < pipe_x + pipe_width and (bird_y < pipe_height or bird_y + bird_height > pipe_height + pipe_gap)):
        running = False

    # Wyświetlanie wyniku
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f'Score: {score}', True, BLACK)
    win.blit(score_text, (10, 10))

    pygame.display.update()

pygame.quit()
