import pygame


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
DARK_GRAY = (70, 70, 70)
BLUE = (70, 130, 255)


class Button:
    def __init__(self, x, y, w, h, text, font):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = font

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        color = BLUE if self.rect.collidepoint(mouse_pos) else DARK_GRAY

        pygame.draw.rect(screen, color, self.rect, border_radius=12)
        pygame.draw.rect(screen, WHITE, self.rect, 2, border_radius=12)

        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )


def draw_text(screen, text, font, color, x, y, center=True):
    surface = font.render(text, True, color)
    rect = surface.get_rect()

    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)

    screen.blit(surface, rect)


def text_input_screen(screen, clock, title="Enter your name"):
    font_big = pygame.font.SysFont("Arial", 42)
    font = pygame.font.SysFont("Arial", 30)

    name = ""
    active = True

    while active:
        screen.fill((25, 25, 35))

        draw_text(screen, title, font_big, WHITE, 400, 180)
        draw_text(screen, name + "|", font, WHITE, 400, 280)
        draw_text(screen, "Press ENTER to start", font, GRAY, 400, 350)

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if name.strip():
                        return name.strip()

                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]

                else:
                    if len(name) < 12 and event.unicode.isprintable():
                        name += event.unicode
