import pygame
import random
import json
import os

from config import *
from db import create_tables, save_score, get_personal_best, get_leaderboard


class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake Game TSIS4")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24)
        self.big_font = pygame.font.SysFont("Arial", 48)

        create_tables()

        self.settings = self.load_settings()

        self.state = "menu"
        self.username = ""
        self.running = True

        self.reset_game()

    def load_settings(self):
        if not os.path.exists("settings.json"):
            data = {
                "snake_color": [0, 220, 0],
                "grid": True,
                "sound": False
            }
            with open("settings.json", "w") as file:
                json.dump(data, file, indent=4)
            return data

        with open("settings.json", "r") as file:
            return json.load(file)

    def save_settings(self):
        with open("settings.json", "w") as file:
            json.dump(self.settings, file, indent=4)

    def reset_game(self):
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.direction = "RIGHT"
        self.next_direction = "RIGHT"

        self.score = 0
        self.level = 1
        self.speed = BASE_SPEED

        self.food = None
        self.poison = None
        self.powerup = None
        self.powerup_type = None

        self.food_timer = 0
        self.poison_timer = 0
        self.powerup_timer = 0

        self.active_speed_effect = None
        self.speed_effect_end = 0

        self.shield = False
        self.obstacles = []

        self.personal_best = 0

        self.spawn_food()
        self.spawn_poison()

    def draw_text(self, text, x, y, color=WHITE, font=None):
        if font is None:
            font = self.font
        surface = font.render(text, True, color)
        self.screen.blit(surface, (x, y))

    def draw_button(self, text, rect):
        pygame.draw.rect(self.screen, GRAY, rect)
        pygame.draw.rect(self.screen, WHITE, rect, 2)

        text_surface = self.font.render(text, True, WHITE)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)

    def clicked(self, rect, pos):
        return rect.collidepoint(pos)

    def random_free_position(self):
        while True:
            x = random.randrange(0, WIDTH, BLOCK)
            y = random.randrange(0, HEIGHT, BLOCK)
            pos = (x, y)

            if (
                pos not in self.snake
                and pos not in self.obstacles
                and pos != self.food
                and pos != self.poison
                and pos != self.powerup
            ):
                return pos

    def spawn_food(self):
        self.food = self.random_free_position()
        self.food_timer = pygame.time.get_ticks()

    def spawn_poison(self):
        self.poison = self.random_free_position()
        self.poison_timer = pygame.time.get_ticks()

    def spawn_powerup(self):
        if self.powerup is None:
            self.powerup = self.random_free_position()
            self.powerup_type = random.choice(["speed", "slow", "shield"])
            self.powerup_timer = pygame.time.get_ticks()

    def generate_obstacles(self):
        self.obstacles = []

        if self.level < 3:
            return

        count = self.level + 2
        head = self.snake[0]

        while len(self.obstacles) < count:
            pos = self.random_free_position()

            distance = abs(pos[0] - head[0]) + abs(pos[1] - head[1])

            if distance > BLOCK * 3:
                self.obstacles.append(pos)

    def handle_direction(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] and self.direction != "DOWN":
            self.next_direction = "UP"
        elif keys[pygame.K_DOWN] and self.direction != "UP":
            self.next_direction = "DOWN"
        elif keys[pygame.K_LEFT] and self.direction != "RIGHT":
            self.next_direction = "LEFT"
        elif keys[pygame.K_RIGHT] and self.direction != "LEFT":
            self.next_direction = "RIGHT"

    def move_snake(self):
        self.direction = self.next_direction

        x, y = self.snake[0]

        if self.direction == "UP":
            y -= BLOCK
        elif self.direction == "DOWN":
            y += BLOCK
        elif self.direction == "LEFT":
            x -= BLOCK
        elif self.direction == "RIGHT":
            x += BLOCK

        new_head = (x, y)

        hit_wall = x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT
        hit_self = new_head in self.snake
        hit_obstacle = new_head in self.obstacles

        if hit_wall or hit_self or hit_obstacle:
            if self.shield:
                self.shield = False
                return
            self.game_over()
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 1
            self.spawn_food()

            if self.score % LEVEL_UP_EVERY == 0:
                self.level += 1
                self.speed += 2
                self.generate_obstacles()
        else:
            self.snake.pop()

        if new_head == self.poison:
            self.snake.pop()
            if len(self.snake) > 1:
                self.snake.pop()

            self.spawn_poison()

            if len(self.snake) <= 1:
                self.game_over()

        if new_head == self.powerup:
            self.activate_powerup()
            self.powerup = None
            self.powerup_type = None

    def activate_powerup(self):
        now = pygame.time.get_ticks()

        if self.powerup_type == "speed":
            self.active_speed_effect = "speed"
            self.speed_effect_end = now + 5000

        elif self.powerup_type == "slow":
            self.active_speed_effect = "slow"
            self.speed_effect_end = now + 5000

        elif self.powerup_type == "shield":
            self.shield = True

    def update_timers(self):
        now = pygame.time.get_ticks()

        if now - self.food_timer > 6000:
            self.spawn_food()

        if now - self.poison_timer > 8000:
            self.spawn_poison()

        if self.powerup is None:
            if random.randint(1, 200) == 1:
                self.spawn_powerup()
        else:
            if now - self.powerup_timer > 8000:
                self.powerup = None
                self.powerup_type = None

        if self.active_speed_effect and now > self.speed_effect_end:
            self.active_speed_effect = None

    def get_current_speed(self):
        if self.active_speed_effect == "speed":
            return self.speed + 5

        if self.active_speed_effect == "slow":
            return max(5, self.speed - 5)

        return self.speed

    def draw_grid(self):
        if not self.settings["grid"]:
            return

        for x in range(0, WIDTH, BLOCK):
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, HEIGHT))

        for y in range(0, HEIGHT, BLOCK):
            pygame.draw.line(self.screen, GRAY, (0, y), (WIDTH, y))

    def draw_game(self):
        self.screen.fill(BLACK)

        self.draw_grid()

        snake_color = tuple(self.settings["snake_color"])

        for part in self.snake:
            pygame.draw.rect(self.screen, snake_color, (*part, BLOCK, BLOCK))

        pygame.draw.rect(self.screen, NORMAL_FOOD_COLOR, (*self.food, BLOCK, BLOCK))
        pygame.draw.rect(self.screen, POISON_COLOR, (*self.poison, BLOCK, BLOCK))

        if self.powerup:
            color = BLUE

            if self.powerup_type == "slow":
                color = YELLOW
            elif self.powerup_type == "shield":
                color = PURPLE

            pygame.draw.rect(self.screen, color, (*self.powerup, BLOCK, BLOCK))

        for obs in self.obstacles:
            pygame.draw.rect(self.screen, OBSTACLE_COLOR, (*obs, BLOCK, BLOCK))

        self.draw_text(f"Score: {self.score}", 10, 10)
        self.draw_text(f"Level: {self.level}", 10, 40)
        self.draw_text(f"Best: {self.personal_best}", 10, 70)

        if self.shield:
            self.draw_text("Shield: ON", 10, 100, PURPLE)

        if self.active_speed_effect:
            self.draw_text(f"Effect: {self.active_speed_effect}", 10, 130, YELLOW)

    def game_over(self):
        if self.username.strip():
            save_score(self.username, self.score, self.level)

        self.state = "game_over"

    def menu_screen(self):
        self.screen.fill(BLACK)

        self.draw_text("SNAKE GAME", 210, 80, GREEN, self.big_font)
        self.draw_text("Enter username:", 230, 170)
        self.draw_text(self.username + "|", 250, 210, YELLOW)

        play_btn = pygame.Rect(250, 280, 200, 50)
        board_btn = pygame.Rect(250, 350, 200, 50)
        settings_btn = pygame.Rect(250, 420, 200, 50)
        quit_btn = pygame.Rect(250, 490, 200, 50)

        self.draw_button("Play", play_btn)
        self.draw_button("Leaderboard", board_btn)
        self.draw_button("Settings", settings_btn)
        self.draw_button("Quit", quit_btn)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.username = self.username[:-1]
                elif event.key == pygame.K_RETURN:
                    if self.username.strip():
                        self.personal_best = get_personal_best(self.username)
                        self.reset_game()
                        self.personal_best = get_personal_best(self.username)
                        self.state = "game"
                else:
                    if len(self.username) < 12:
                        self.username += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if self.clicked(play_btn, pos) and self.username.strip():
                    self.personal_best = get_personal_best(self.username)
                    self.reset_game()
                    self.personal_best = get_personal_best(self.username)
                    self.state = "game"

                elif self.clicked(board_btn, pos):
                    self.state = "leaderboard"

                elif self.clicked(settings_btn, pos):
                    self.state = "settings"

                elif self.clicked(quit_btn, pos):
                    self.running = False

    def leaderboard_screen(self):
        self.screen.fill(BLACK)

        self.draw_text("LEADERBOARD", 210, 50, YELLOW, self.big_font)

        try:
            leaders = get_leaderboard()
        except Exception:
            leaders = []

        y = 130
        self.draw_text("Rank  Username        Score  Level  Date", 60, y)
        y += 40

        for i, row in enumerate(leaders, start=1):
            username, score, level, date = row
            text = f"{i:<5} {username:<14} {score:<6} {level:<6} {date}"
            self.draw_text(text, 60, y)
            y += 35

        back_btn = pygame.Rect(250, 610, 200, 50)
        self.draw_button("Back", back_btn)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.clicked(back_btn, pygame.mouse.get_pos()):
                    self.state = "menu"

    def settings_screen(self):
        self.screen.fill(BLACK)

        self.draw_text("SETTINGS", 250, 70, YELLOW, self.big_font)

        grid_btn = pygame.Rect(220, 180, 260, 50)
        sound_btn = pygame.Rect(220, 250, 260, 50)
        color_btn = pygame.Rect(220, 320, 260, 50)
        back_btn = pygame.Rect(220, 430, 260, 50)

        grid_text = f"Grid: {'ON' if self.settings['grid'] else 'OFF'}"
        sound_text = f"Sound: {'ON' if self.settings['sound'] else 'OFF'}"

        self.draw_button(grid_text, grid_btn)
        self.draw_button(sound_text, sound_btn)
        self.draw_button("Change Snake Color", color_btn)
        self.draw_button("Save & Back", back_btn)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if self.clicked(grid_btn, pos):
                    self.settings["grid"] = not self.settings["grid"]

                elif self.clicked(sound_btn, pos):
                    self.settings["sound"] = not self.settings["sound"]

                elif self.clicked(color_btn, pos):
                    colors = [
                        [0, 220, 0],
                        [50, 140, 255],
                        [255, 150, 40],
                        [170, 70, 255],
                        [255, 255, 255]
                    ]

                    current = self.settings["snake_color"]

                    if current in colors:
                        index = colors.index(current)
                        self.settings["snake_color"] = colors[(index + 1) % len(colors)]
                    else:
                        self.settings["snake_color"] = colors[0]

                elif self.clicked(back_btn, pos):
                    self.save_settings()
                    self.state = "menu"

    def game_over_screen(self):
        self.screen.fill(BLACK)

        self.draw_text("GAME OVER", 220, 100, RED, self.big_font)
        self.draw_text(f"Score: {self.score}", 280, 190)
        self.draw_text(f"Level: {self.level}", 280, 230)

        best = max(self.personal_best, self.score)
        self.draw_text(f"Personal Best: {best}", 240, 270, YELLOW)

        retry_btn = pygame.Rect(250, 360, 200, 50)
        menu_btn = pygame.Rect(250, 430, 200, 50)

        self.draw_button("Retry", retry_btn)
        self.draw_button("Main Menu", menu_btn)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if self.clicked(retry_btn, pos):
                    self.personal_best = get_personal_best(self.username)
                    self.reset_game()
                    self.personal_best = get_personal_best(self.username)
                    self.state = "game"

                elif self.clicked(menu_btn, pos):
                    self.state = "menu"

    def game_screen(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        self.handle_direction()
        self.update_timers()
        self.move_snake()
        self.draw_game()

    def run(self):
        while self.running:
            if self.state == "menu":
                self.menu_screen()

            elif self.state == "game":
                self.game_screen()

            elif self.state == "leaderboard":
                self.leaderboard_screen()

            elif self.state == "settings":
                self.settings_screen()

            elif self.state == "game_over":
                self.game_over_screen()

            pygame.display.flip()
            self.clock.tick(self.get_current_speed() if self.state == "game" else FPS)

        pygame.quit()