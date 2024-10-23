import pygame
import random
import time

# Rozmiary labiryntu
maze_width = 10
maze_height = 10
cell_size = 40

# Kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Kierunki: Góra, Dół, Lewo, Prawo
DIRECTIONS = [(0, -1), (0, 1), (-1, 0), (1, 0)]

# Inicjalizacja pygame
pygame.init()

# Ekran gry
screen = pygame.display.set_mode((maze_width * cell_size, maze_height * cell_size))
pygame.display.set_caption("Labirynt - Gra")

# Czcionka do wyświetlania poziomu i komunikatów
font = pygame.font.SysFont(None, 36)

# Funkcja generująca losowy labirynt przy pomocy algorytmu "backtracking"
def generate_maze(width, height):
    maze = [[1 for _ in range(width)] for _ in range(height)]
    start = (0, 0)
    stack = [start]
    maze[0][0] = 0

    while stack:
        current_cell = stack[-1]
        x, y = current_cell

        # Znajdź sąsiadów
        neighbors = []
        for direction in DIRECTIONS:
            nx, ny = x + direction[0] * 2, y + direction[1] * 2
            if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == 1:
                neighbors.append((nx, ny))

        if neighbors:
            next_cell = random.choice(neighbors)
            nx, ny = next_cell

            # Otwórz przejście między komórkami
            maze[y + (ny - y) // 2][x + (nx - x) // 2] = 0
            maze[ny][nx] = 0

            stack.append((nx, ny))
        else:
            stack.pop()

    return maze

# Funkcja rysująca labirynt
def draw_maze(maze):
    for y in range(maze_height):
        for x in range(maze_width):
            color = WHITE if maze[y][x] == 0 else BLACK
            pygame.draw.rect(screen, color, (x * cell_size, y * cell_size, cell_size, cell_size))

# Funkcja sprawdzająca, czy gracz znalazł wyjście
def check_exit(player_pos):
    return player_pos == (maze_width - 2, maze_height - 2)

# Funkcja do obsługi ruchu gracza
def move_player(player_pos, direction, maze):
    new_pos = (player_pos[0] + direction[0], player_pos[1] + direction[1])
    if 0 <= new_pos[0] < maze_width and 0 <= new_pos[1] < maze_height:
        if maze[new_pos[1]][new_pos[0]] == 0:  # Jeśli nie ma ściany
            return new_pos
    return player_pos

# Funkcja wyświetlająca poziom gry
def display_level(level):
    level_text = font.render(f"Poziom: {level}", True, RED)
    screen.blit(level_text, (10, 10))

# Funkcja wyświetlająca pozostały czas
def display_time_left(time_left):
    time_text = font.render(f"Czas: {int(time_left)}s", True, RED)
    screen.blit(time_text, (maze_width * cell_size - 150, 10))

# Funkcja wyświetlająca komunikat o końcu gry
def display_game_over(levels_completed):
    game_over_text = font.render(f"Koniec gry! Poziomy: {levels_completed}", True, RED)
    screen.blit(game_over_text, (maze_width * cell_size // 4, maze_height * cell_size // 2))

# Główna funkcja gry
def main():
    level = 1  # Początkowy poziom
    maze = generate_maze(maze_width, maze_height)
    player_pos = (0, 0)
    total_time = 10  # Całkowity czas gry w sekundach
    start_time = time.time()  # Pobierz czas rozpoczęcia gry

    clock = pygame.time.Clock()
    running = True
    game_over = False

    while running:
        screen.fill(BLACK)

        # Sprawdzenie, ile czasu pozostało
        elapsed_time = time.time() - start_time
        time_left = total_time - elapsed_time

        if time_left <= 0:
            # Koniec gry
            game_over = True

        if not game_over:
            draw_maze(maze)
            display_level(level)
            display_time_left(time_left)

            # Rysuj gracza
            pygame.draw.rect(screen, BLUE, (player_pos[0] * cell_size, player_pos[1] * cell_size, cell_size, cell_size))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Ruch gracza
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                player_pos = move_player(player_pos, (-1, 0), maze)
            if keys[pygame.K_RIGHT]:
                player_pos = move_player(player_pos, (1, 0), maze)
            if keys[pygame.K_UP]:
                player_pos = move_player(player_pos, (0, -1), maze)
            if keys[pygame.K_DOWN]:
                player_pos = move_player(player_pos, (0, 1), maze)

            # Sprawdź, czy gracz znalazł wyjście
            if check_exit(player_pos):
                level += 1  # Zwiększ poziom
                maze = generate_maze(maze_width, maze_height)  # Generuj nowy labirynt
                player_pos = (0, 0)  # Zresetuj pozycję gracza

        else:
            # Wyświetl komunikat o końcu gry
            display_game_over(level)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
