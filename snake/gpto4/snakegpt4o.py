import pygame
import time
import random

# Inicjalizacja pygame
pygame.init()

# Definiowanie kolorów
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Wymiary okna gry
window_width = 600
window_height = 400

# Ustawienia ekranu
game_window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Snake Game')

# Ustawienia zegara
clock = pygame.time.Clock()

snake_block = 10
snake_speed = 15

# Ustawienia czcionki
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Funkcja wyświetlająca wynik
def score(score):
    value = score_font.render("Your Score: " + str(score), True, yellow)
    game_window.blit(value, [0, 0])

# Funkcja tworząca ciało węża
def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(game_window, black, [x[0], x[1], snake_block, snake_block])

# Funkcja wyświetlania wiadomości na ekranie
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    game_window.blit(mesg, [window_width / 6, window_height / 3])

# Główna funkcja gry
def gameLoop():
    game_over = False
    game_close = False

    # Początkowe pozycje węża
    x1 = window_width / 2
    y1 = window_height / 2

    # Zmiany pozycji
    x1_change = 0
    y1_change = 0

    # Ciało węża
    snake_list = []
    length_of_snake = 1

    # Pozycja jedzenia
    foodx = round(random.randrange(0, window_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, window_height - snake_block) / 10.0) * 10.0

    while not game_over:

        while game_close:
            game_window.fill(blue)
            message("You Lost! Press C-Play Again or Q-Quit", red)
            score(length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        # Sprawdzanie kolizji z krawędziami
        if x1 >= window_width or x1 < 0 or y1 >= window_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        game_window.fill(blue)

        # Rysowanie jedzenia
        pygame.draw.rect(game_window, green, [foodx, foody, snake_block, snake_block])

        # Ruch węża
        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        # Sprawdzanie kolizji z ciałem węża
        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        our_snake(snake_block, snake_list)
        score(length_of_snake - 1)

        pygame.display.update()

        # Sprawdzanie, czy wąż zjadł jedzenie
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, window_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, window_height - snake_block) / 10.0) * 10.0
            length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()

# Uruchomienie gry
gameLoop()
