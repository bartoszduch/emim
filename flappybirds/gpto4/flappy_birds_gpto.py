import pygame
import random

# Inicjalizacja Pygame
pygame.init()

# Parametry gry
WIDTH, HEIGHT = 400, 600
FPS = 60
GRAVITY = 0.5
JUMP_STRENGTH = -10
PIPE_SPEED = 5
PIPE_GAP = 150

# Kolory
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Ustawienie okna gry
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Załadowanie obrazków
bird_img = pygame.Surface((40, 30))
bird_img.fill((255, 255, 0))  # Żółty prostokąt jako ptak

pipe_top_img = pygame.Surface((80, HEIGHT))
pipe_top_img.fill(GREEN)  # Zielony prostokąt jako górna rura

pipe_bottom_img = pygame.Surface((80, HEIGHT))
pipe_bottom_img.fill(GREEN)  # Zielony prostokąt jako dolna rura

# Klasa ptaka
class Bird:
    def __init__(self):
        self.x = 100
        self.y = HEIGHT // 2
        self.velocity = 0
        self.rect = pygame.Rect(self.x, self.y, 40, 30)

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        self.rect.topleft = (self.x, self.y)

    def jump(self):
        self.velocity = JUMP_STRENGTH

    def draw(self, screen):
        screen.blit(bird_img, (self.x, self.y))

# Klasa rur
class Pipe:
    def __init__(self):
        self.x = WIDTH
        self.height = random.randint(100, 400)
        self.rect_top = pygame.Rect(self.x, 0, 80, self.height)
        self.rect_bottom = pygame.Rect(self.x, self.height + PIPE_GAP, 80, HEIGHT - self.height - PIPE_GAP)

    def update(self):
        self.x -= PIPE_SPEED
        self.rect_top.topleft = (self.x, 0)
        self.rect_bottom.topleft = (self.x, self.height + PIPE_GAP)

    def draw(self, screen):
        screen.blit(pipe_top_img, self.rect_top)
        screen.blit(pipe_bottom_img, self.rect_bottom)

# Funkcja główna
def main():
    clock = pygame.time.Clock()
    bird = Bird()
    pipes = [Pipe()]
    score = 0
    font = pygame.font.Font(None, 36)

    running = True
    while running:
        clock.tick(FPS)

        # Obsługa zdarzeń
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird.jump()

        # Aktualizacja stanu gry
        bird.update()

        # Sprawdzanie kolizji z górą lub dołem ekranu
        if bird.y > HEIGHT or bird.y < 0:
            running = False

        # Aktualizacja rur
        for pipe in pipes:
            pipe.update()
            # Sprawdzanie kolizji z rurami
            if bird.rect.colliderect(pipe.rect_top) or bird.rect.colliderect(pipe.rect_bottom):
                running = False

        # Usuwanie rury, która wyszła poza ekran
        if pipes[0].x < -80:
            pipes.pop(0)
            score += 1

        # Dodawanie nowych rur
        if pipes[-1].x < WIDTH // 2:
            pipes.append(Pipe())

        # Rysowanie
        screen.fill(WHITE)
        bird.draw(screen)
        for pipe in pipes:
            pipe.draw(screen)

        # Wyświetlanie wyniku
        score_text = font.render(f"Score: {score}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
