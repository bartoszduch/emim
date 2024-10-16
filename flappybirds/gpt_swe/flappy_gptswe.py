import pygame
import random

# Inicjalizacja Pygame
pygame.init()

# Kolory
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Ustawienia ekranu
width = 600
height = 400
dis = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flappy Bird")

# Parametry ptaka
bird_x = 100
bird_y = 200
bird_width = 20
bird_height = 20
bird_vel_y = 0
gravity = 0.5
jump_strength = -10

# Parametry rur
pipe_width = 50
pipe_gap = 150
pipe_speed = 3

# Zegar gry
clock = pygame.time.Clock()
fps = 60


# Funkcja rysująca ptaka
def draw_bird(bird_x, bird_y):
    pygame.draw.rect(dis, blue, [bird_x, bird_y, bird_width, bird_height])


# Funkcja rysująca rury
def draw_pipes(pipes):
    for pipe in pipes:
        pygame.draw.rect(dis, green, [pipe['x'], 0, pipe_width, pipe['height']])
        pygame.draw.rect(dis, green, [pipe['x'], pipe['height'] + pipe_gap, pipe_width, height])


# Funkcja sprawdzająca kolizje
def check_collision(bird_x, bird_y, pipes):
    for pipe in pipes:
        if bird_x + bird_width > pipe['x'] and bird_x < pipe['x'] + pipe_width:
            if bird_y < pipe['height'] or bird_y + bird_height > pipe['height'] + pipe_gap:
                return True
        if bird_y + bird_height > height:
            return True
    return False


# Funkcja głównej pętli gry
def gameLoop():
    bird_y = 200
    bird_vel_y = 0

    # Inicjalizacja rur
    pipes = [{'x': width, 'height': random.randint(50, height - pipe_gap - 50)}]

    score = 0
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_vel_y = jump_strength

        # Grawitacja
        bird_vel_y += gravity
        bird_y += bird_vel_y

        # Poruszanie rur
        for pipe in pipes:
            pipe['x'] -= pipe_speed

        # Dodanie nowej rury
        if pipes[-1]['x'] < width - 300:
            pipes.append({'x': width, 'height': random.randint(50, height - pipe_gap - 50)})

        # Usuwanie rur poza ekranem
        if pipes[0]['x'] < -pipe_width:
            pipes.pop(0)
            score += 1

        # Sprawdzanie kolizji
        if check_collision(bird_x, bird_y, pipes):
            game_over = True

        # Rysowanie
        dis.fill(white)
        draw_bird(bird_x, bird_y)
        draw_pipes(pipes)

        # Wyświetlanie wyniku
        font = pygame.font.SysFont(None, 35)
        score_text = font.render(f"Score: {score}", True, black)
        dis.blit(score_text, [10, 10])

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()


gameLoop()
