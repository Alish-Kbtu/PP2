from datetime import datetime
from pathlib import Path

import pygame


WINDOW_SIZE = (600, 600)
FPS = 30
BACKGROUND = (245, 245, 245)
MINUTE_COLOR = (32, 32, 32)
SECOND_COLOR = (220, 40, 40)
CENTER_DOT_COLOR = (25, 25, 25)


def load_clock_face():
    image_path = Path(__file__).resolve().parent / "images" / "mickeyclock.png"

    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    original = pygame.image.load(str(image_path)).convert_alpha()
    face = pygame.transform.smoothscale(original, (620, 465))
    face_rect = face.get_rect(center=(WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2 - 20))
    center = face_rect.center
    return face, face_rect, center


def draw_hand(screen, center, angle, length, color, width):
    hand_surface = pygame.Surface((width, length), pygame.SRCALPHA)
    pygame.draw.rect(hand_surface, color, (0, 0, width, length), border_radius=2)
    rotated_hand = pygame.transform.rotate(hand_surface, -angle)

    offset = pygame.math.Vector2(0, -length / 2).rotate(angle)
    hand_rect = rotated_hand.get_rect(center=(center[0] + offset.x, center[1] + offset.y))
    screen.blit(rotated_hand, hand_rect)


def draw_scene(screen, face, face_rect, center, font):
    now = datetime.now()

    minute_angle = now.minute * 6 + now.second * 0.1
    second_angle = now.second * 6

    screen.fill(BACKGROUND)
    screen.blit(face, face_rect)

    draw_hand(screen, center, minute_angle, 110, MINUTE_COLOR, 12)
    draw_hand(screen, center, second_angle, 155, SECOND_COLOR, 10)
    pygame.draw.circle(screen, CENTER_DOT_COLOR, center, 10)

    time_text = font.render(now.strftime("%H:%M:%S"), True, (30, 30, 30))
    screen.blit(time_text, time_text.get_rect(center=(WINDOW_SIZE[0] // 2, 40)))


def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Mickey's Clock")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 28)

    face, face_rect, center = load_clock_face()

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        draw_scene(screen, face, face_rect, center, font)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()