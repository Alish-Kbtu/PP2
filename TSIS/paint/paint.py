import pygame
from tools import *

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")
info_font = pygame.font.SysFont("Arial", 16)

canvas = pygame.Surface((WIDTH, HEIGHT))
canvas.fill((255, 255, 255))

clock = pygame.time.Clock()

color = (0, 0, 0)
tool = "pencil"
brush_size = 2

drawing = False
start_pos = None
last_pos = None

font = pygame.font.SysFont("Arial", 20)
text_input = ""
typing = False
text_pos = (0, 0)

running = True
while running:
    screen.fill((200, 200, 200))
    screen.blit(canvas, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # клавиши
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                brush_size = 2
            if event.key == pygame.K_2:
                brush_size = 5
            if event.key == pygame.K_3:
                brush_size = 10

            if event.key == pygame.K_l:
                tool = "line"
            if event.key == pygame.K_r:
                tool = "rect"
            if event.key == pygame.K_c:
                tool = "circle"
            if event.key == pygame.K_p:
                tool = "pencil"
            if event.key == pygame.K_f:
                tool = "fill"
            if event.key == pygame.K_t:
                tool = "text"
            if event.key == pygame.K_e:
                tool = "eraser"

            # сохранить
            if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                pygame.image.save(canvas, "image.png")

            # текст
            if typing:
                if event.key == pygame.K_RETURN:
                    txt = font.render(text_input, True, color)
                    canvas.blit(txt, text_pos)
                    typing = False
                    text_input = ""
                elif event.key == pygame.K_BACKSPACE:
                    text_input = text_input[:-1]
                elif event.key == pygame.K_ESCAPE:
                    typing = False
                    text_input = ""
                else:
                    text_input += event.unicode

        # мышка
        if event.type == pygame.MOUSEBUTTONDOWN:
            if tool == "fill":
                flood_fill(canvas, event.pos, color)
            elif tool == "text":
                typing = True
                text_pos = event.pos
            else:
                drawing = True
                start_pos = event.pos
                last_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                if tool == "line":
                    draw_line(canvas, color, start_pos, event.pos, brush_size)
                elif tool == "rect":
                    draw_rect(canvas, color, start_pos, event.pos, brush_size)
                elif tool == "circle":
                    draw_circle(canvas, color, start_pos, event.pos, brush_size)

            drawing = False

        if event.type == pygame.MOUSEMOTION:
            if drawing:
                if tool == "pencil":
                    draw_pencil(canvas, color, last_pos, event.pos, brush_size)
                    last_pos = event.pos

                elif tool == "eraser":
                    erase(canvas, last_pos, event.pos, brush_size)
                    last_pos = event.pos

    # preview фигур
    if drawing and tool in ["line", "rect", "circle"]:
        temp = canvas.copy()
        mouse_pos = pygame.mouse.get_pos()

        if tool == "line":
            draw_line(temp, color, start_pos, mouse_pos, brush_size)
        elif tool == "rect":
            draw_rect(temp, color, start_pos, mouse_pos, brush_size)
        elif tool == "circle":
            draw_circle(temp, color, start_pos, mouse_pos, brush_size)

        screen.blit(temp, (0, 0))

    # отображение текста
    if typing:
        txt = font.render(text_input, True, color)
        screen.blit(txt, text_pos)

    # инструкция
    instructions = [
        "P - pencil",
        "E - eraser",
        "L - line",
        "R - rectangle",
        "C - circle",
        "F - fill",
        "T - text",
        "1/2/3 - brush size",
        "Ctrl+S - save"
    ]
    y = 5
    for line in instructions:
        txt = info_font.render(line, True, (0, 0, 0))
        screen.blit(txt, (5, y))
        y += 18

    pygame.display.flip()
    clock.tick(60)

pygame.quit()