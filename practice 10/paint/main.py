import pygame
import math

def main():
    pygame.init()

    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Paint")
    clock = pygame.time.Clock()

    BLACK = (0, 0, 0)

    canvas = pygame.Surface(screen.get_size())
    canvas.fill(BLACK)

    radius = 5
    drawing = False
    start_pos = None
    current_pos = None

    tool = "brush"
    color = (0, 0, 255)

    last_pos = None

    font = pygame.font.SysFont("Arial", 20)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return

                # цвет
                if event.key == pygame.K_r:
                    color = (255, 0, 0)
                elif event.key == pygame.K_g:
                    color = (0, 255, 0)
                elif event.key == pygame.K_b:
                    color = (0, 0, 255)
                elif event.key == pygame.K_w:
                    color = (255, 255, 255)
                elif event.key == pygame.K_y:
                    color = (255, 255, 0)

                # инструмент
                elif event.key == pygame.K_1:
                    tool = "brush"
                elif event.key == pygame.K_2:
                    tool = "rect"
                elif event.key == pygame.K_3:
                    tool = "circle"
                elif event.key == pygame.K_4:
                    tool = "eraser"

                # размер
                elif event.key == pygame.K_UP:
                    radius = min(50, radius + 1)
                elif event.key == pygame.K_DOWN:
                    radius = max(1, radius - 1)

                # Clear canvas
                elif event.key == pygame.K_c:
                    canvas.fill(BLACK)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                drawing = True
                start_pos = event.pos
                current_pos = event.pos
                last_pos = event.pos

                if tool == "brush":
                    pygame.draw.circle(canvas, color, event.pos, radius)
                elif tool == "eraser":
                    pygame.draw.circle(canvas, BLACK, event.pos, radius)

            if event.type == pygame.MOUSEMOTION:
                current_pos = event.pos

                if drawing:
                    if tool == "brush":
                        draw_line(canvas, color, last_pos, event.pos, radius)
                        last_pos = event.pos
                    elif tool == "eraser":
                        draw_line(canvas, BLACK, last_pos, event.pos, radius)
                        last_pos = event.pos

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if drawing:
                    end_pos = event.pos

                    if tool == "rect":
                        draw_rectangle(canvas, color, start_pos, end_pos)
                    elif tool == "circle":
                        draw_circle(canvas, color, start_pos, end_pos)

                drawing = False
                start_pos = None
                current_pos = None
                last_pos = None

        screen.fill(BLACK)
        screen.blit(canvas, (0, 0))

        if drawing and start_pos and current_pos:
            if tool == "rect":
                draw_rectangle(screen, color, start_pos, current_pos)
            elif tool == "circle":
                draw_circle(screen, color, start_pos, current_pos)

        tool_text = font.render(f"Tool: {tool}", True, (255, 255, 255))
        size_text = font.render(f"Size: {radius}", True, (255, 255, 255))
        info_text = font.render("1-Brush  2-Rect  3-Circle  4-Eraser | R G B W Y | UP/DOWN size | C clear", True, (255, 255, 255))

        screen.blit(tool_text, (10, 10))
        screen.blit(size_text, (10, 35))
        screen.blit(info_text, (10, 455))

        pygame.display.flip()
        clock.tick(60)


def draw_line(surface, color, start, end, width):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    distance = max(abs(dx), abs(dy))

    if distance == 0:
        pygame.draw.circle(surface, color, start, width)
        return

    for i in range(distance + 1):
        x = int(start[0] + dx * i / distance)
        y = int(start[1] + dy * i / distance)
        pygame.draw.circle(surface, color, (x, y), width)


def draw_rectangle(surface, color, start, end):
    x1, y1 = start
    x2, y2 = end

    left = min(x1, x2)
    top = min(y1, y2)
    width = abs(x2 - x1)
    height = abs(y2 - y1)

    pygame.draw.rect(surface, color, (left, top, width, height), 2)


def draw_circle(surface, color, start, end):
    x1, y1 = start
    x2, y2 = end

    radius = int(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))
    pygame.draw.circle(surface, color, (x1, y1), radius, 2)


main()