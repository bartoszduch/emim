import pygame
import sys
import random

# Kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Rozmiar ekranu
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400

# Rozmiar węża i jedzenia
SNAKE_SIZE = 20
FOOD_SIZE = 20

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 35)

# Funkcje gry
def draw_snake(snake_body):
    for segment in snake_body:
        pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE))

def generate_food():
    x = random.randint(0, (SCREEN_WIDTH // SNAKE_SIZE) - 1) * SNAKE_SIZE
    y = random.randint(0, (SCREEN_HEIGHT // SNAKE_SIZE) - 1) * SNAKE_SIZE
    return (x, y)

def check_collision(snake_head, snake_body):
    if (snake_head[0] < 0 or snake_head[0] >= SCREEN_WIDTH or
        snake_head[1] < 0 or snake_head[1] >= SCREEN_HEIGHT):
        return True
    for segment in snake_body[1:]:
        if snake_head == segment:
            return True
    return False

# Główna pętla gry
def main():
    snake_body = [(100, 50), (90, 50), (80, 50)]
    snake_direction = (SNAKE_SIZE, 0)
    food_pos = generate_food()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake_direction != (0, SNAKE_SIZE):
                    snake_direction = (0, -SNAKE_SIZE)
                elif event.key == pygame.K_DOWN and snake_direction != (0, -SNAKE_SIZE):
                    snake_direction = (0, SNAKE_SIZE)
                elif event.key == pygame.K_LEFT and snake_direction != (SNAKE_SIZE, 0):
                    snake_direction = (-SNAKE_SIZE, 0)
                elif event.key == pygame.K_RIGHT and snake_direction != (-SNAKE_SIZE, 0):
                    snake_direction = (SNAKE_SIZE, 0)

        snake_head = (snake_body[0][0] + snake_direction[0], snake_body[0][1] + snake_direction[1])
        snake_body = [snake_head] + snake_body[:-1]

        if snake_head == food_pos:
            snake_body.append(snake_body[-1])
            food_pos = generate_food()

        screen.fill(BLACK)
        draw_snake(snake_body)
        pygame.draw.rect(screen, RED, pygame.Rect(food_pos[0], food_pos[1], FOOD_SIZE, FOOD_SIZE))
        pygame.display.flip()

        if check_collision(snake_head, snake_body):
            break

        clock.tick(15)

main()
