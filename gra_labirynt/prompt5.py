import pygame
import random
import time

# Rozmiary labiryntu
maze_width = 10
maze_height = 10
cell_size = 40

# Rozmiary ekranu
screen_width = maze_width * cell_size + 300
screen_height = maze_height * cell_size + 100  # Zwiększamy wysokość ekranu, aby wyświetlić tekst

# Kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 149, 237)  # Łagodny niebieski dla gracza
RED = (255, 69, 0)  # Pomarańczowy dla poziomów i czasu
LIGHT_GREY = (211, 211, 211)
DARK_GREY = (50, 50, 50)
PASTEL_GREEN = (152, 251, 152)
PASTEL_BLUE = (173, 216, 230)
PASTEL_YELLOW = (255, 239, 213)

# Kierunki: Góra, Dół, Lewo, Prawo
DIRECTIONS = [(0, -1), (0, 1), (-1, 0), (1, 0)]

# Inicjalizacja pygame
pygame.init()

# Ekran gry
screen = pygame.display.set_mode((screen_width, screen_height))
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
    screen.blit(level_text, (10, screen_height - 90))  # Przesuwamy tekst w dół


# Funkcja wyświetlająca pozostały czas
def display_time_left(time_left):
    time_text = font.render(f"Czas: {int(time_left)}s", True, RED)
    screen.blit(time_text, (screen_width - 150, screen_height - 90))  # Przesuwamy tekst w dół


# Funkcja wyświetlająca komunikat o końcu gry
def display_game_over(levels_completed):
    game_over_text = font.render(f"Koniec gry! Poziomy: {levels_completed}", True, RED)
    screen.blit(game_over_text, (screen_width // 4, screen_height // 2))


# Funkcja obsługująca menu początkowe
def start_menu():
    input_box = pygame.Rect(screen_width // 4, screen_height // 2 - 20, 140, 32)
    color_inactive = PASTEL_BLUE
    color_active = PASTEL_GREEN
    color = color_inactive
    active = False
    user_text = ''
    start_game = False
    clock = pygame.time.Clock()

    while not start_game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Jeśli kliknięto na pole tekstowe
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive

            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        start_game = True
                        return int(user_text) if user_text.isdigit() else 10  # Domyślnie 10 sekund
                    elif event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]
                    else:
                        user_text += event.unicode

        screen.fill(PASTEL_YELLOW)
        # Renderuj instrukcje
        start_text = font.render("Wpisz czas gry (w sekundach) i nacisnij Enter", True, DARK_GREY)
        screen.blit(start_text, (screen_width // 4 - 100, screen_height // 2 - 60))

        # Renderuj pole tekstowe
        txt_surface = font.render(user_text, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.flip()
        clock.tick(30)


# Funkcja obsługująca menu końcowe
def end_menu(levels_completed):
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Naciśnięcie Enter - nowa gra
                    return True
                elif event.key == pygame.K_ESCAPE:  # Naciśnięcie Esc - wyjście
                    pygame.quit()
                    return None

        screen.fill(PASTEL_BLUE)
        end_text = font.render(f"Koniec gry! Ukończono poziomów: {levels_completed}", True, DARK_GREY)
        restart_text = font.render("Naciśnij Enter, aby zagrać ponownie,  lub Esc, aby wyjść.", True, DARK_GREY)
        screen.blit(end_text, (screen_width // 4 - 100, screen_height // 2 - 20))
        screen.blit(restart_text, (screen_width // 4 - 100, screen_height // 2 + 40))

        pygame.display.flip()
        clock.tick(30)


# Główna funkcja gry
def main():
    running = True
    while running:
        # Menu startowe
        total_time = start_menu()
        if total_time is None:
            break  # Jeśli gracz wyjdzie z gry w menu

        level = 1  # Początkowy poziom
        maze = generate_maze(maze_width, maze_height)
        player_pos = (0, 0)
        start_time = time.time()  # Pobierz czas rozpoczęcia gry

        clock = pygame.time.Clock()
        game_over = False

        while not game_over:
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
                pygame.draw.rect(screen, BLUE,
                                 (player_pos[0] * cell_size, player_pos[1] * cell_size, cell_size, cell_size))

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
                running = end_menu(level)

            pygame.display.flip()
            clock.tick(30)


if __name__ == "__main__":
    main()
