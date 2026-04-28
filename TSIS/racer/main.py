import pygame
from ui import Button, draw_text, text_input_screen
from racer import RacerGame, WIDTH, HEIGHT, WHITE, GRAY
from persistence import load_settings, save_settings, load_leaderboard


pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS 3 Racer Game")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 28)
small_font = pygame.font.SysFont("Arial", 22)
big_font = pygame.font.SysFont("Arial", 48)

settings = load_settings()


def main_menu():
    play_btn = Button(300, 210, 200, 50, "Play", font)
    leaderboard_btn = Button(300, 280, 200, 50, "Leaderboard", font)
    settings_btn = Button(300, 350, 200, 50, "Settings", font)
    quit_btn = Button(300, 420, 200, 50, "Quit", font)

    buttons = [play_btn, leaderboard_btn, settings_btn, quit_btn]

    while True:
        screen.fill((25, 25, 35))

        draw_text(screen, "RACER GAME", big_font, WHITE, WIDTH // 2, 120)

        for button in buttons:
            button.draw(screen)

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if play_btn.is_clicked(event):
                return "play"

            if leaderboard_btn.is_clicked(event):
                return "leaderboard"

            if settings_btn.is_clicked(event):
                return "settings"

            if quit_btn.is_clicked(event):
                return "quit"


def leaderboard_screen():
    back_btn = Button(300, 520, 200, 45, "Back", font)

    while True:
        screen.fill((25, 25, 35))
        draw_text(screen, "LEADERBOARD TOP 10", big_font, WHITE, WIDTH // 2, 70)

        leaderboard = load_leaderboard()

        if not leaderboard:
            draw_text(screen, "No scores yet", font, GRAY, WIDTH // 2, 230)
        else:
            y = 135
            draw_text(screen, "Rank    Name        Score    Distance", small_font, GRAY, WIDTH // 2, 110)

            for i, item in enumerate(leaderboard, start=1):
                line = f"{i:<7} {item['name']:<10} {item['score']:<8} {item['distance']}"
                draw_text(screen, line, small_font, WHITE, 230, y, center=False)
                y += 35

        back_btn.draw(screen)

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if back_btn.is_clicked(event):
                return "menu"


def settings_screen():
    global settings

    sound_btn = Button(270, 190, 260, 45, "", font)
    color_btn = Button(270, 260, 260, 45, "", font)
    difficulty_btn = Button(270, 330, 260, 45, "", font)
    back_btn = Button(300, 480, 200, 45, "Back", font)

    colors = ["Red", "Blue", "Green", "Purple"]
    difficulties = ["Easy", "Normal", "Hard"]

    while True:
        screen.fill((25, 25, 35))

        draw_text(screen, "SETTINGS", big_font, WHITE, WIDTH // 2, 90)

        sound_btn.text = f"Sound: {'On' if settings['sound'] else 'Off'}"
        color_btn.text = f"Car Color: {settings['car_color']}"
        difficulty_btn.text = f"Difficulty: {settings['difficulty']}"

        sound_btn.draw(screen)
        color_btn.draw(screen)
        difficulty_btn.draw(screen)
        back_btn.draw(screen)

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_settings(settings)
                return "quit"

            if sound_btn.is_clicked(event):
                settings["sound"] = not settings["sound"]
                save_settings(settings)

            if color_btn.is_clicked(event):
                index = colors.index(settings["car_color"])
                settings["car_color"] = colors[(index + 1) % len(colors)]
                save_settings(settings)

            if difficulty_btn.is_clicked(event):
                index = difficulties.index(settings["difficulty"])
                settings["difficulty"] = difficulties[(index + 1) % len(difficulties)]
                save_settings(settings)

            if back_btn.is_clicked(event):
                save_settings(settings)
                return "menu"


def game_over_screen(result):
    retry_btn = Button(300, 370, 200, 50, "Retry", font)
    menu_btn = Button(300, 440, 200, 50, "Main Menu", font)

    while True:
        screen.fill((25, 25, 35))

        draw_text(screen, "GAME OVER", big_font, WHITE, WIDTH // 2, 100)
        draw_text(screen, f"Score: {result['score']}", font, WHITE, WIDTH // 2, 190)
        draw_text(screen, f"Distance: {result['distance']}", font, WHITE, WIDTH // 2, 235)
        draw_text(screen, f"Coins: {result['coins']}", font, WHITE, WIDTH // 2, 280)

        retry_btn.draw(screen)
        menu_btn.draw(screen)

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if retry_btn.is_clicked(event):
                return "retry"

            if menu_btn.is_clicked(event):
                return "menu"


def play_game():
    name = text_input_screen(screen, clock)

    if name is None:
        return "quit"

    while True:
        game = RacerGame(screen, clock, settings, name)
        result = game.run()

        if result == "quit":
            return "quit"

        choice = game_over_screen(result)

        if choice == "retry":
            continue

        return choice


def main():
    state = "menu"

    while True:
        if state == "menu":
            state = main_menu()

        elif state == "play":
            state = play_game()

        elif state == "leaderboard":
            state = leaderboard_screen()

        elif state == "settings":
            state = settings_screen()

        elif state == "quit":
            break

    pygame.quit()


if __name__ == "__main__":
    main()
