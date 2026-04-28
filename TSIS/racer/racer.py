import pygame
import random
from persistence import add_score


WIDTH = 800
HEIGHT = 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ROAD = (45, 45, 45)
GRASS = (35, 120, 55)
YELLOW = (255, 220, 0)
RED = (220, 50, 50)
BLUE = (60, 120, 255)
GREEN = (40, 210, 100)
PURPLE = (170, 70, 220)
ORANGE = (255, 140, 30)
GRAY = (160, 160, 160)
CYAN = (40, 220, 220)

LANES = [250, 350, 450, 550]
ROAD_LEFT = 200
ROAD_RIGHT = 600

CAR_COLORS = {
    "Red": RED,
    "Blue": BLUE,
    "Green": GREEN,
    "Purple": PURPLE
}

DIFFICULTY = {
    "Easy": {
        "enemy_speed": 4,
        "spawn_delay": 1100,
        "obstacle_delay": 1500
    },
    "Normal": {
        "enemy_speed": 5,
        "spawn_delay": 850,
        "obstacle_delay": 1200
    },
    "Hard": {
        "enemy_speed": 7,
        "spawn_delay": 650,
        "obstacle_delay": 900
    }
}


class Player(pygame.sprite.Sprite):
    def __init__(self, color):
        super().__init__()
        self.image = pygame.Surface((50, 80), pygame.SRCALPHA)
        pygame.draw.rect(self.image, color, (0, 0, 50, 80), border_radius=10)
        pygame.draw.rect(self.image, WHITE, (10, 10, 30, 18), border_radius=5)
        pygame.draw.rect(self.image, BLACK, (8, 55, 8, 18))
        pygame.draw.rect(self.image, BLACK, (34, 55, 8, 18))

        self.rect = self.image.get_rect()
        self.rect.center = (400, 500)
        self.speed = 7

    def update(self, keys, nitro_active=False):
        move_speed = self.speed + 4 if nitro_active else self.speed

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= move_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += move_speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= move_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += move_speed

        self.rect.left = max(ROAD_LEFT + 5, self.rect.left)
        self.rect.right = min(ROAD_RIGHT - 5, self.rect.right)
        self.rect.top = max(0, self.rect.top)
        self.rect.bottom = min(HEIGHT, self.rect.bottom)


class EnemyCar(pygame.sprite.Sprite):
    def __init__(self, speed, player_rect):
        super().__init__()
        self.image = pygame.Surface((50, 80), pygame.SRCALPHA)
        pygame.draw.rect(self.image, ORANGE, (0, 0, 50, 80), border_radius=10)
        pygame.draw.rect(self.image, WHITE, (10, 50, 30, 18), border_radius=5)

        self.rect = self.image.get_rect()
        self.rect.centerx = random.choice(LANES)
        self.rect.y = -100

        while abs(self.rect.centerx - player_rect.centerx) < 80 and player_rect.y < 180:
            self.rect.centerx = random.choice(LANES)

        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, kind, speed, player_rect):
        super().__init__()
        self.kind = kind
        self.speed = speed

        self.image = pygame.Surface((60, 40), pygame.SRCALPHA)

        if kind == "oil":
            pygame.draw.ellipse(self.image, BLACK, (0, 5, 60, 30))
        elif kind == "pothole":
            pygame.draw.ellipse(self.image, GRAY, (0, 0, 60, 40))
            pygame.draw.ellipse(self.image, BLACK, (10, 8, 40, 24))
        elif kind == "barrier":
            pygame.draw.rect(self.image, RED, (0, 5, 60, 30))
            pygame.draw.line(self.image, WHITE, (5, 30), (55, 5), 5)
        elif kind == "moving_barrier":
            pygame.draw.rect(self.image, PURPLE, (0, 5, 60, 30))
            pygame.draw.line(self.image, WHITE, (5, 5), (55, 30), 5)
            self.direction = random.choice([-1, 1])
        elif kind == "speed_bump":
            pygame.draw.rect(self.image, YELLOW, (0, 12, 60, 16), border_radius=8)
        elif kind == "nitro_strip":
            pygame.draw.rect(self.image, CYAN, (0, 5, 60, 30), border_radius=8)

        self.rect = self.image.get_rect()
        self.rect.centerx = random.choice(LANES)
        self.rect.y = -70

        while abs(self.rect.centerx - player_rect.centerx) < 80 and player_rect.y < 160:
            self.rect.centerx = random.choice(LANES)

    def update(self):
        self.rect.y += self.speed

        if self.kind == "moving_barrier":
            self.rect.x += self.direction * 3
            if self.rect.left < ROAD_LEFT or self.rect.right > ROAD_RIGHT:
                self.direction *= -1

        if self.rect.top > HEIGHT:
            self.kill()


class Coin(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.value = random.choice([1, 2, 5])
        size = 25 + self.value * 2

        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(self.image, YELLOW, (size // 2, size // 2), size // 2)
        pygame.draw.circle(self.image, ORANGE, (size // 2, size // 2), size // 2, 3)

        self.rect = self.image.get_rect()
        self.rect.centerx = random.choice(LANES)
        self.rect.y = -50
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.kind = random.choice(["Nitro", "Shield", "Repair"])
        self.spawn_time = pygame.time.get_ticks()
        self.timeout = 6000
        self.speed = speed

        self.image = pygame.Surface((38, 38), pygame.SRCALPHA)

        if self.kind == "Nitro":
            color = CYAN
            letter = "N"
        elif self.kind == "Shield":
            color = BLUE
            letter = "S"
        else:
            color = GREEN
            letter = "R"

        pygame.draw.circle(self.image, color, (19, 19), 19)
        pygame.draw.circle(self.image, WHITE, (19, 19), 19, 2)

        font = pygame.font.SysFont("Arial", 22, bold=True)
        text = font.render(letter, True, WHITE)
        rect = text.get_rect(center=(19, 19))
        self.image.blit(text, rect)

        self.rect = self.image.get_rect()
        self.rect.centerx = random.choice(LANES)
        self.rect.y = -50

    def update(self):
        self.rect.y += self.speed

        now = pygame.time.get_ticks()
        if now - self.spawn_time > self.timeout:
            self.kill()

        if self.rect.top > HEIGHT:
            self.kill()


class RacerGame:
    def __init__(self, screen, clock, settings, player_name):
        self.screen = screen
        self.clock = clock
        self.settings = settings
        self.player_name = player_name

        difficulty = settings["difficulty"]
        self.base_enemy_speed = DIFFICULTY[difficulty]["enemy_speed"]
        self.spawn_delay = DIFFICULTY[difficulty]["spawn_delay"]
        self.obstacle_delay = DIFFICULTY[difficulty]["obstacle_delay"]

        color = CAR_COLORS.get(settings["car_color"], RED)
        self.player = Player(color)

        self.enemies = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.coins = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group(self.player)

        self.font = pygame.font.SysFont("Arial", 24)
        self.big_font = pygame.font.SysFont("Arial", 42)

        self.score = 0
        self.coins_count = 0
        self.distance = 0
        self.finish_distance = 3000

        self.active_power = None
        self.power_end_time = 0
        self.shield_hits = 0
        self.repair_available = False

        self.last_enemy_spawn = 0
        self.last_obstacle_spawn = 0
        self.last_coin_spawn = 0
        self.last_power_spawn = 0

        self.road_y = 0
        self.running = True
        self.game_over = False

    def current_speed_bonus(self):
        return self.distance // 500

    def current_world_speed(self):
        return 5 + self.current_speed_bonus()

    def draw_road(self):
        self.screen.fill(GRASS)

        pygame.draw.rect(self.screen, ROAD, (ROAD_LEFT, 0, ROAD_RIGHT - ROAD_LEFT, HEIGHT))

        for x in [300, 400, 500]:
            for y in range(-40, HEIGHT, 80):
                pygame.draw.rect(self.screen, WHITE, (x - 3, y + self.road_y, 6, 40))

        pygame.draw.line(self.screen, YELLOW, (ROAD_LEFT, 0), (ROAD_LEFT, HEIGHT), 5)
        pygame.draw.line(self.screen, YELLOW, (ROAD_RIGHT, 0), (ROAD_RIGHT, HEIGHT), 5)

        self.road_y += self.current_world_speed()
        if self.road_y >= 80:
            self.road_y = 0

    def draw_hud(self):
        active = self.active_power if self.active_power else "None"

        if self.active_power == "Nitro":
            remaining = max(0, (self.power_end_time - pygame.time.get_ticks()) // 1000)
            active = f"Nitro {remaining}s"

        texts = [
            f"Score: {self.score}",
            f"Coins: {self.coins_count}",
            f"Distance: {self.distance}/{self.finish_distance}",
            f"Power-up: {active}"
        ]

        y = 10
        for text in texts:
            surface = self.font.render(text, True, WHITE)
            self.screen.blit(surface, (10, y))
            y += 30

        progress_width = 250
        pygame.draw.rect(self.screen, WHITE, (530, 15, progress_width, 18), 2)
        filled = int(progress_width * min(self.distance / self.finish_distance, 1))
        pygame.draw.rect(self.screen, GREEN, (530, 15, filled, 18))

    def spawn_objects(self):
        now = pygame.time.get_ticks()

        density_bonus = min(self.current_speed_bonus() * 70, 350)

        if now - self.last_enemy_spawn > max(300, self.spawn_delay - density_bonus):
            speed = self.base_enemy_speed + self.current_speed_bonus()
            enemy = EnemyCar(speed, self.player.rect)
            self.enemies.add(enemy)
            self.all_sprites.add(enemy)
            self.last_enemy_spawn = now

        if now - self.last_obstacle_spawn > max(350, self.obstacle_delay - density_bonus):
            kind = random.choice([
                "oil",
                "pothole",
                "barrier",
                "moving_barrier",
                "speed_bump",
                "nitro_strip"
            ])
            obstacle = Obstacle(kind, self.current_world_speed(), self.player.rect)
            self.obstacles.add(obstacle)
            self.all_sprites.add(obstacle)
            self.last_obstacle_spawn = now

        if now - self.last_coin_spawn > 700:
            coin = Coin(self.current_world_speed())
            self.coins.add(coin)
            self.all_sprites.add(coin)
            self.last_coin_spawn = now

        if now - self.last_power_spawn > 9000:
            power = PowerUp(self.current_world_speed())
            self.powerups.add(power)
            self.all_sprites.add(power)
            self.last_power_spawn = now

    def activate_powerup(self, kind):
        if self.active_power is not None:
            return

        if kind == "Nitro":
            self.active_power = "Nitro"
            self.power_end_time = pygame.time.get_ticks() + random.randint(3000, 5000)
            self.score += 25

        elif kind == "Shield":
            self.active_power = "Shield"
            self.shield_hits = 1
            self.score += 20

        elif kind == "Repair":
            self.active_power = "Repair"
            self.repair_available = True
            self.score += 20

    def update_powerups(self):
        if self.active_power == "Nitro":
            if pygame.time.get_ticks() > self.power_end_time:
                self.active_power = None

    def handle_collision(self):
        hit_enemy = pygame.sprite.spritecollideany(self.player, self.enemies)
        hit_obstacle = pygame.sprite.spritecollideany(self.player, self.obstacles)

        hit = hit_enemy or hit_obstacle

        if hit:
            if hasattr(hit, "kind"):
                if hit.kind == "oil":
                    self.player.rect.x += random.choice([-80, 80])
                    hit.kill()
                    return

                if hit.kind == "speed_bump":
                    self.distance = max(0, self.distance - 25)
                    hit.kill()
                    return

                if hit.kind == "nitro_strip":
                    self.active_power = "Nitro"
                    self.power_end_time = pygame.time.get_ticks() + 3000
                    hit.kill()
                    return

            if self.active_power == "Shield" and self.shield_hits > 0:
                self.shield_hits -= 1
                self.active_power = None
                hit.kill()
                return

            if self.active_power == "Repair" and self.repair_available:
                self.repair_available = False
                self.active_power = None
                hit.kill()
                return

            self.game_over = True

    def update(self):
        keys = pygame.key.get_pressed()

        nitro_active = self.active_power == "Nitro"
        self.player.update(keys, nitro_active)

        self.spawn_objects()

        self.enemies.update()
        self.obstacles.update()
        self.coins.update()
        self.powerups.update()

        self.update_powerups()

        collected_coins = pygame.sprite.spritecollide(self.player, self.coins, True)
        for coin in collected_coins:
            self.coins_count += coin.value
            self.score += coin.value * 10

        collected_powerups = pygame.sprite.spritecollide(self.player, self.powerups, True)
        for power in collected_powerups:
            self.activate_powerup(power.kind)

        self.handle_collision()

        self.distance += 1 + self.current_speed_bonus()
        self.score = self.coins_count * 10 + self.distance

        if self.distance >= self.finish_distance:
            self.score += 500
            self.game_over = True

    def draw(self):
        self.draw_road()
        self.all_sprites.draw(self.screen)
        self.draw_hud()

    def run(self):
        while self.running and not self.game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"

            self.update()
            self.draw()

            pygame.display.flip()
            self.clock.tick(60)

        add_score(self.player_name, self.score, self.distance, self.coins_count)

        return {
            "score": self.score,
            "distance": self.distance,
            "coins": self.coins_count
        }
