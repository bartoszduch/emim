import pygame
import sys
import random

# Konfiguracja gry
pygame.init()
screen = pygame.display.set_mode((400, 600))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Graficzne zasoby
bird = pygame.Rect(100, 300, 30, 30)
pipe_width = 70
pipe_gap = 200
pipes = []

# Ustawienia
gravity = 0.25
bird_movement = 0
game_active = True

# Funkcje gry
def draw_pipes(pipes):
    for pipe in pipes:
        pygame.draw.rect(screen, GREEN, pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird.colliderect(pipe):
            return False
    if bird.top <= 0 or bird.bottom >= 600:
        return False
    return True

def create_pipe():
    random_pipe_pos = random.randint(200, 400)
    bottom_pipe = pygame.Rect(400, random_pipe_pos, pipe_width, 600)
    top_pipe = pygame.Rect(400, random_pipe_pos - pipe_gap - 600, pipe_width, 600)
    return bottom_pipe, top_pipe

# Główna pętla gry
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 6
            if event.key == pygame.K_SPACE and not game_active:
                game_active = True
                pipes.clear()
                bird.center = (100, 300)
                bird_movement = 0

    screen.fill(WHITE)

    if game_active:
        # Ruch ptaka
        bird_movement += gravity
        bird.y += bird_movement

        # Ruch rur
        pipes = [pipe.move(-5, 0) for pipe in pipes]
        if len(pipes) > 0 and pipes[0].right < 0:
            pipes.pop(0)
            pipes.pop(0)

        # Nowe rury
        if len(pipes) == 0 or pipes[-1].left < 300:
            pipes.extend(create_pipe())

        draw_pipes(pipes)

        game_active = check_collision(pipes)

    pygame.draw.rect(screen, BLACK, bird)
    pygame.display.update()
    clock.tick(60)
