import pygame
import random
from pygame.locals import *

pygame.init()

# цвета
LILAC = (200, 162, 200)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

ws = (700, 700)
s = pygame.display.set_mode(ws)
pygame.display.set_caption("Snake")
c = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 25)
snake = [(100, 100), (80, 100), (60, 100)]
block = 20
direct = "RIGHT"
score = 0
level = 1
speed = 10

# генерация еды
def f_gen():
    while True:
        x = random.randrange(0, ws[0], block)
        y = random.randrange(0, ws[1], block)
        new_food = (x, y)
        if new_food not in snake:
            return new_food
food = f_gen()

run = True
while run:
    # обработка событий
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False

        # направления
        if event.type == KEYDOWN:
            if event.key == K_LEFT and direct != "RIGHT":
                direct = "LEFT"
            elif event.key == K_RIGHT and direct != "LEFT":
                direct = "RIGHT"
            elif event.key == K_UP and direct != "DOWN":
                direct = "UP"
            elif event.key == K_DOWN and direct != "UP":
                direct = "DOWN"

    head_x, head_y = snake[0]
    if direct == "RIGHT":
        new_head = (head_x + block, head_y)
    elif direct == "LEFT":
        new_head = (head_x - block, head_y)
    elif direct == "UP":
        new_head = (head_x, head_y - block)
    elif direct == "DOWN":
        new_head = (head_x, head_y + block)

    # проверка столкновений с границами и с собой
    if new_head[0] < 0 or new_head[0] >= ws[0] or new_head[1] < 0 or new_head[1] >= ws[1]:
        run = False
    if new_head in snake:
        run = False

    # добавление новой головы
    snake.insert(0, new_head)
    # удаление хвоста
    if new_head != food:
        snake.pop()
    else:
        score += 1
        food = f_gen()
        level = score // 5 + 1
        speed = 10 + (level - 1) * 2
        
    s.fill(GREEN)

    # еда
    pygame.draw.rect(s, (255, 0, 0), (food[0], food[1], block, block))
    
    # змея
    for segment in snake:
        pygame.draw.rect(s, BLUE, (segment[0], segment[1], block, block))
    
    # счет и уровень
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    speed_text = font.render(f"Speed: {speed}", True, WHITE)
    s.blit(score_text, (10, 10))
    s.blit(level_text, (10, 40))
    s.blit(speed_text, (10, 70))


    pygame.display.update()
    c.tick(speed)
pygame.quit()