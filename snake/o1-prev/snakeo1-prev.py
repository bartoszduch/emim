import pygame
import sys
import random

# Inicjalizacja Pygame
pygame.init()

# Ustawienia okna gry
rozmiar_okna = (600, 600)
okno = pygame.display.set_mode(rozmiar_okna)
pygame.display.set_caption('Snake')

# Kolory
kolor_tła = (0, 0, 0)
kolor_węża = (0, 255, 0)
kolor_jedzenia = (255, 0, 0)

# Rozmiar bloku
rozmiar_bloku = 20

# Prędkość gry
zegar = pygame.time.Clock()

def gra():
    x = rozmiar_okna[0] // 2
    y = rozmiar_okna[1] // 2

    x_zmiana = 0
    y_zmiana = 0

    ciało_węża = []
    długość_węża = 1

    jedzenie_x = round(random.randrange(0, rozmiar_okna[0] - rozmiar_bloku) / 20.0) * 20.0
    jedzenie_y = round(random.randrange(0, rozmiar_okna[1] - rozmiar_bloku) / 20.0) * 20.0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_zmiana != rozmiar_bloku:
                    x_zmiana = -rozmiar_bloku
                    y_zmiana = 0
                elif event.key == pygame.K_RIGHT and x_zmiana != -rozmiar_bloku:
                    x_zmiana = rozmiar_bloku
                    y_zmiana = 0
                elif event.key == pygame.K_UP and y_zmiana != rozmiar_bloku:
                    y_zmiana = -rozmiar_bloku
                    x_zmiana = 0
                elif event.key == pygame.K_DOWN and y_zmiana != -rozmiar_bloku:
                    y_zmiana = rozmiar_bloku
                    x_zmiana = 0

        if x >= rozmiar_okna[0] or x < 0 or y >= rozmiar_okna[1] or y < 0:
            pygame.quit()
            sys.exit()

        x += x_zmiana
        y += y_zmiana

        okno.fill(kolor_tła)
        pygame.draw.rect(okno, kolor_jedzenia, [jedzenie_x, jedzenie_y, rozmiar_bloku, rozmiar_bloku])

        głowa_węża = [x, y]
        ciało_węża.append(głowa_węża)

        if len(ciało_węża) > długość_węża:
            del ciało_węża[0]

        for segment in ciało_węża[:-1]:
            if segment == głowa_węża:
                pygame.quit()
                sys.exit()

        for segment in ciało_węża:
            pygame.draw.rect(okno, kolor_węża, [segment[0], segment[1], rozmiar_bloku, rozmiar_bloku])

        pygame.display.update()

        if x == jedzenie_x and y == jedzenie_y:
            jedzenie_x = round(random.randrange(0, rozmiar_okna[0] - rozmiar_bloku) / 20.0) * 20.0
            jedzenie_y = round(random.randrange(0, rozmiar_okna[1] - rozmiar_bloku) / 20.0) * 20.0
            długość_węża += 1

        zegar.tick(15)

gra()
