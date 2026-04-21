import pygame
import random
from pygame.locals import *

pygame.init()

WHITE = (255, 255, 255)
GRAY = (80, 80, 80)
DARK_GRAY = (40, 40, 40)
LILAC = (200, 162, 200)
YELLOW = (255, 215, 0)
ws = (500, 700)
s = pygame.display.set_mode(ws)
pygame.display.set_caption("Racer")
c = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)
fps = 60
player = (60, 100)
player_pos = (ws[0] // 2, ws[1] // 2)
speed = 7
coin_size = 30
coins_collect = 0

# появление монеты
def random_coin():
    x = random.randint(110, ws[0] - 110 - coin_size)
    y = -coin_size
    return pygame.Rect(x, y, coin_size, coin_size)

coin_rect = random_coin()
coin_speed = 5

# размер машины
player_rect = pygame.Rect(player_pos[0], player_pos[1], player[0], player[1])

run = True
while run:
    c.tick(fps)
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False

    keys = pygame.key.get_pressed()

    # управление машиной
    if keys[K_LEFT]:
        player_rect.x -= speed
    if keys[K_RIGHT]:
        player_rect.x += speed

    #не даёт машине выйти за границы
    if player_rect.x < 100:
        player_rect.x = 100
    if player_rect.x > ws[0] - 100 - player[0]:
        player_rect.x = ws[0] - 100 - player[0]

    coin_rect.y += coin_speed

    if coin_rect.y > ws[1]:
        coin_rect = random_coin()

    if player_rect.colliderect(coin_rect):
        coins_collect += 1
        coin_rect = random_coin()

    s.fill(GRAY)

    pygame.draw.rect(s, DARK_GRAY, (100, 0, ws[0] - 200, ws[1]))

    for y in range(0, ws[1], 80):
        pygame.draw.rect(s, WHITE, (ws[0] // 2 - 5, y, 10, 40))

    pygame.draw.rect(s, LILAC, player_rect)

    pygame.draw.ellipse(s, YELLOW, coin_rect)

    score_text = font.render(f"Coins: {coins_collect}", True, WHITE)
    s.blit(score_text, (ws[0] - score_text.get_width() - 20, 20))

    pygame.display.update()

pygame.quit()