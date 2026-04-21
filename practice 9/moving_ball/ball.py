import pygame


WINDOW_SIZE = (600, 600)
WHITE = (255, 255, 255)
LILAC = (200, 162, 200)
STEP = 5
RADIUS = 25
FPS = 120


def keep_inside(x, y):
    x = max(RADIUS, min(WINDOW_SIZE[0] - RADIUS, x))
    y = max(RADIUS, min(WINDOW_SIZE[1] - RADIUS, y))
    return x, y


def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Moving Ball")
    clock = pygame.time.Clock()

    x = WINDOW_SIZE[0] // 2
    y = WINDOW_SIZE[1] // 2
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            y -= STEP
        if pressed[pygame.K_DOWN]:
            y += STEP
        if pressed[pygame.K_LEFT]:
            x -= STEP
        if pressed[pygame.K_RIGHT]:
            x += STEP

        x, y = keep_inside(x, y)

        screen.fill(WHITE)
        pygame.draw.circle(screen, LILAC, (x, y), RADIUS)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()