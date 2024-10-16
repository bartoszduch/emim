import pygame
import random

# Inicjalizacja Pygame
pygame.init()

# Wymiary okna gry
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Tworzenie okna gry
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')

# Ustawienie zegara
clock = pygame.time.Clock()

# Klasa gracza (ptaka)
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([30, 30])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = [50, SCREEN_HEIGHT / 2]
        self.velocity = 0

    def update(self):
        self.velocity += 0.5  # Grawitacja
        self.rect.y += int(self.velocity)

    def flap(self):
        self.velocity = -10  # Skok

# Klasa przeszkód (rur)
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, inverted):
        super().__init__()
        self.image = pygame.Surface([50, SCREEN_HEIGHT])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - 100]
        else:
            self.rect.topleft = [x, y + 100]

    def update(self):
        self.rect.x -= 5  # Przesuwanie rur w lewo
        if self.rect.right < 0:
            self.kill()

# Grupy sprite'ów
all_sprites = pygame.sprite.Group()
pipes = pygame.sprite.Group()

# Tworzenie instancji ptaka
bird = Bird()
all_sprites.add(bird)

# Funkcja tworząca rury
def create_pipes():
    y = random.randint(-150, 150)
    top_pipe = Pipe(SCREEN_WIDTH, SCREEN_HEIGHT / 2 + y, True)
    bottom_pipe = Pipe(SCREEN_WIDTH, SCREEN_HEIGHT / 2 + y, False)
    pipes.add(top_pipe)
    pipes.add(bottom_pipe)
    all_sprites.add(top_pipe)
    all_sprites.add(bottom_pipe)

# Główna pętla gry
running = True
pipe_timer = 0

while running:
    clock.tick(60)  # 60 FPS

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.flap()

    # Aktualizacja sprite'ów
    all_sprites.update()

    # Tworzenie nowych rur
    pipe_timer += 1
    if pipe_timer > 90:
        create_pipes()
        pipe_timer = 0

    # Sprawdzanie kolizji
    if pygame.sprite.spritecollideany(bird, pipes) or bird.rect.top < 0 or bird.rect.bottom > SCREEN_HEIGHT:
        running = False  # Koniec gry w przypadku kolizji

    # Rysowanie
    screen.fill(WHITE)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
