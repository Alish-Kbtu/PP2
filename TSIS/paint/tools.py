import pygame

def draw_line(surface, color, start_pos, end_pos, width):
    pygame.draw.line(surface, color, start_pos, end_pos, width)


def draw_circle(surface, color, start_pos, end_pos, width):
    radius = int(((end_pos[0] - start_pos[0])**2 + (end_pos[1] - start_pos[1])**2) ** 0.5)
    pygame.draw.circle(surface, color, start_pos, radius, width)


def draw_rect(surface, color, start_pos, end_pos, width):
    x = min(start_pos[0], end_pos[0])
    y = min(start_pos[1], end_pos[1])
    w = abs(start_pos[0] - end_pos[0])
    h = abs(start_pos[1] - end_pos[1])
    pygame.draw.rect(surface, color, (x, y, w, h), width)


def draw_pencil(surface, color, last_pos, current_pos, width):
    pygame.draw.line(surface, color, last_pos, current_pos, width)

def erase(surface, last_pos, current_pos, width):
    pygame.draw.line(surface, (255, 255, 255), last_pos, current_pos, width)

def flood_fill(surface, pos, fill_color):
    target_color = surface.get_at(pos)
    if target_color == fill_color:
        return

    stack = [pos]

    while stack:
        x, y = stack.pop()

        if surface.get_at((x, y)) != target_color:
            continue

        surface.set_at((x, y), fill_color)

        if x > 0: stack.append((x - 1, y))
        if x < surface.get_width() - 1: stack.append((x + 1, y))
        if y > 0: stack.append((x, y - 1))
        if y < surface.get_height() - 1: stack.append((x, y + 1))