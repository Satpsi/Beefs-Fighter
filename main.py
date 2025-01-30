import pygame
from pygame import mixer
from Fighter import Fighter
import sqlite3
import sys

mixer.init()
pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 675
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Beefs Fighter")
clock = pygame.time.Clock()
FPS = 60
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
score = [0, 0]
ROUND_OVER_COOLDOWN = 2000
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]

WIZARD_SIZE = 162
WIZARD_SCALE = 4
WIZARD_OFFSET = [72, 56]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

current_bg = "image/fon1.png"
bg_image = pygame.image.load(current_bg).convert_alpha()
warrior_skins = ["image/obladaet.png", "image/toxis.png", "image/og buda.png"]
wizard_skins = ["image/toxis.png", "image/obladaet.png", "image/og buda.png"]
warrior_sheet = pygame.image.load("image/obladaet.png").convert_alpha()
wizard_sheet = pygame.image.load("image/og buda.png").convert_alpha()
victory_img = pygame.image.load("image/victory.png").convert_alpha()

WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]

count_font = pygame.font.SysFont(None, 80)
score_font = pygame.font.SysFont(None, 30)
table_font = pygame.font.SysFont(None, 40)


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))


def draw_bg():
    screen.blit(scaled_bg, (0, 0))


def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))


def draw_button(text, x, y, width, height, color, font, text_col):
    pygame.draw.rect(screen, color, (x, y, width, height))
    draw_text(text, font, text_col, x + width // 4, y + height // 4)


def display_leaderboard():
    running = True
    while running:
        screen.fill((0, 0, 0))
        draw_bg()
        draw_text("Leaderboard", count_font, WHITE, SCREEN_WIDTH // 3, 50)
        records = get_top_records()
        y_offset = 200
        draw_text("Name", table_font, YELLOW, 300, 150)
        draw_text("Score", table_font, YELLOW, 600, 150)
        for i, (name, score) in enumerate(records):
            draw_text(f"{i + 1}. {name}", table_font, WHITE, 300, y_offset)
            draw_text(str(score), table_font, WHITE, 600, y_offset)
            y_offset += 50
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
        pygame.display.update()
        clock.tick(FPS)


def init_db():
    conn = sqlite3.connect("leaderboard.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leaderboard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            score INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def add_record(name, score):
    conn = sqlite3.connect('leaderboard.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO leaderboard (name, score) VALUES (?, ?)", (name, score))

    conn.commit()
    conn.close()


def get_top_records():
    conn = sqlite3.connect("leaderboard.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, score FROM leaderboard ORDER BY score DESC LIMIT 5")
    records = cursor.fetchall()
    conn.close()
    return records


def update_player_score(player_name, score_change):
    conn = sqlite3.connect('leaderboard.db')
    cursor = conn.cursor()
    cursor.execute("SELECT score FROM leaderboard WHERE name=?", (player_name,))
    result = cursor.fetchone()

    if result:
        current_score = result[0]
        new_score = current_score + score_change
        cursor.execute("UPDATE leaderboard SET score=? WHERE name=?", (new_score, player_name))
    else:
        cursor.execute("INSERT INTO leaderboard (name, score) VALUES (?, ?)", (player_name, score_change))

    conn.commit()
    conn.close()


warrior_skins = ["image/obladaet.png", "image/toxis.png", "image/og buda.png"]
wizard_skins = ["image/toxis.png", "image/obladaet.png", "image/og buda.png"]

current_warrior_skin_index = 0
current_wizard_skin_index = 0


def settings_menu():
    settings_running = True
    while settings_running:
        screen.fill((0, 0, 0))
        draw_bg()
        draw_text("Settings", count_font, WHITE, SCREEN_WIDTH // 3, 100)
        draw_button("Background", 400, 200, 200, 50, RED, score_font, WHITE)
        draw_button("Skins", 400, 270, 200, 50, RED, score_font, WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(400, 200, 200, 50).collidepoint(event.pos):
                    background_menu()
                elif pygame.Rect(400, 270, 200, 50).collidepoint(event.pos):
                    skin_menu()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    settings_running = False

        pygame.display.update()
        clock.tick(FPS)


def background_menu():
    global current_bg
    bg_options = [
        "image/fon1.png",
        "image/fon2.png",
        "image/fon3.png"
    ]

    bg_menu_running = True
    while bg_menu_running:
        screen.fill((0, 0, 0))
        draw_bg()
        draw_text("Select Background", count_font, WHITE, SCREEN_WIDTH // 4, 50)
        draw_button("BG 1", 200, 150, 200, 50, RED, score_font, WHITE)
        draw_button("BG 2", 400, 150, 200, 50, RED, score_font, WHITE)
        draw_button("BG 3", 600, 150, 200, 50, RED, score_font, WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(200, 150, 200, 50).collidepoint(event.pos):
                    current_bg = bg_options[0]
                elif pygame.Rect(400, 150, 200, 50).collidepoint(event.pos):
                    current_bg = bg_options[1]
                elif pygame.Rect(600, 150, 200, 50).collidepoint(event.pos):
                    current_bg = bg_options[2]
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    bg_menu_running = False

        pygame.display.update()
        clock.tick(FPS)


def skin_menu():
    global current_warrior_skin_index, current_wizard_skin_index
    skin_menu_running = True
    while skin_menu_running:
        screen.fill((0, 0, 0))
        draw_bg()
        draw_text("Select Skins", count_font, WHITE, SCREEN_WIDTH // 4, 50)

        draw_text(f"1 player: {warrior_skins[current_warrior_skin_index]}", table_font, WHITE, 300, 150)
        draw_text(f"2 player: {wizard_skins[current_wizard_skin_index]}", table_font, WHITE, 300, 250)

        draw_button("Next skin", 400, 350, 150, 50, RED, score_font, WHITE)
        draw_button("Next skin", 400, 450, 150, 50, RED, score_font, WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(400, 350, 150, 50).collidepoint(event.pos):
                    current_warrior_skin_index = (current_warrior_skin_index + 1) % len(warrior_skins)
                elif pygame.Rect(400, 450, 150, 50).collidepoint(event.pos):
                    current_wizard_skin_index = (current_wizard_skin_index + 1) % len(wizard_skins)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    skin_menu_running = False

        pygame.display.update()
        clock.tick(FPS)


def draw_bg():
    global current_bg
    bg_image = pygame.image.load(current_bg).convert_alpha()
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))


def main_menu():
    menu_running = True
    while menu_running:
        screen.fill((0, 0, 0))
        draw_bg()
        draw_text("Main Menu", count_font, WHITE, SCREEN_WIDTH // 3, 100)
        draw_button("Start", 400, 200, 200, 50, RED, score_font, WHITE)
        draw_button("Settings", 400, 270, 200, 50, RED, score_font, WHITE)
        draw_button("Table", 400, 340, 200, 50, RED, score_font, WHITE)
        draw_button("Exit", 400, 410, 200, 50, RED, score_font, WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(400, 200, 200, 50).collidepoint(event.pos):
                    return "start"
                elif pygame.Rect(400, 270, 200, 50).collidepoint(event.pos):
                    settings_menu()
                elif pygame.Rect(400, 340, 200, 50).collidepoint(event.pos):
                    display_leaderboard()
                elif pygame.Rect(400, 410, 200, 50).collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        clock.tick(FPS)


def name_entry_screen():
    input_active = [False, False]
    input_boxes = [pygame.Rect(400, 200, 200, 40), pygame.Rect(400, 300, 200, 40)]
    player_names = ["", ""]
    menu_running = True
    while menu_running:
        screen.fill((0, 0, 0))
        draw_bg()
        draw_text("Enter Player Names", count_font, WHITE, 300, 100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, box in enumerate(input_boxes):
                    if box.collidepoint(event.pos):
                        input_active[i] = True
                    else:
                        input_active[i] = False
            if event.type == pygame.KEYDOWN:
                for i in range(2):
                    if input_active[i]:
                        if event.key == pygame.K_RETURN:
                            input_active[i] = False
                        elif event.key == pygame.K_BACKSPACE:
                            player_names[i] = player_names[i][:-1]
                        else:
                            player_names[i] += event.unicode
                if event.key == pygame.K_ESCAPE:
                    return_to_menu()

        for i, box in enumerate(input_boxes):
            color = RED if input_active[i] else WHITE
            pygame.draw.rect(screen, color, box, 2)
            draw_text(player_names[i], score_font, WHITE, box.x + 5, box.y + 5)
        draw_text("Press ENTER to Start", score_font, WHITE, 400, 400)
        if all(player_names) and not any(input_active):
            menu_running = False
        pygame.display.update()
        clock.tick(FPS)
    return player_names


def game_loop(player_names):
    intro_count = 3
    last_count_update = pygame.time.get_ticks()
    round_over = False
    total_rounds = 0
    fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA,
                        pygame.image.load(warrior_skins[current_warrior_skin_index]).convert_alpha(),
                        WARRIOR_ANIMATION_STEPS)
    fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA,
                        pygame.image.load(wizard_skins[current_wizard_skin_index]).convert_alpha(),
                        WIZARD_ANIMATION_STEPS)
    run = True
    while run:
        clock.tick(FPS)
        draw_bg()
        draw_health_bar(fighter_1.health, 20, 20)
        draw_health_bar(fighter_2.health, 580, 20)
        draw_text(f"{player_names[0]}: {score[0]}", score_font, RED, 20, 60)
        draw_text(f"{player_names[1]}: {score[1]}", score_font, RED, 580, 60)
        if intro_count <= 0:
            fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
            fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
        else:
            draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
            if (pygame.time.get_ticks() - last_count_update) >= 1000:
                intro_count -= 1
                last_count_update = pygame.time.get_ticks()
        fighter_1.update()
        fighter_2.update()
        fighter_1.draw(screen)
        fighter_2.draw(screen)
        if not round_over:
            if not fighter_1.alive:
                score[1] += 1
                total_rounds += 1
                round_over = True
                update_player_score(player_names[1], 10)
            elif not fighter_2.alive:
                score[0] += 1
                total_rounds += 1
                round_over = True
                update_player_score(player_names[0], 10)
        else:
            screen.blit(victory_img, (360, 150))
            if pygame.time.get_ticks() - last_count_update > ROUND_OVER_COOLDOWN:
                if total_rounds >= 3:
                    if show_rematch_screen(fighter_1, fighter_2, player_names):
                        score[0], score[1] = 0, 0
                        total_rounds = 0
                    else:
                        run = False
                else:
                    round_over = False
                    intro_count = 3
                    fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA,
                                        pygame.image.load(warrior_skins[current_warrior_skin_index]).convert_alpha(),
                                        WARRIOR_ANIMATION_STEPS)
                    fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA,
                                        pygame.image.load(wizard_skins[current_wizard_skin_index]).convert_alpha(),
                                        WIZARD_ANIMATION_STEPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        pygame.display.update()


def show_rematch_screen(fighter_1, fighter_2, player_names):
    rematch_screen = True
    while rematch_screen:
        draw_bg()
        draw_health_bar(fighter_1.health, 20, 20)
        draw_health_bar(fighter_2.health, 580, 20)
        draw_text(f"{player_names[0]}: {score[0]}", score_font, RED, 20, 60)
        draw_text(f"{player_names[1]}: {score[1]}", score_font, RED, 580, 60)
        draw_text("Rematch?", count_font, WHITE, 400, 100)
        draw_button("Yes", 400, 200, 200, 50, RED, score_font, WHITE)
        draw_button("No", 400, 300, 200, 50, RED, score_font, WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect(400, 200, 200, 50).collidepoint(event.pos):
                    return True
                elif pygame.Rect(400, 300, 200, 50).collidepoint(event.pos):
                    return_to_menu()

        pygame.display.update()
        clock.tick(FPS)


def return_to_menu():
    menu_choice = main_menu()
    if menu_choice == "start":
        player_names = name_entry_screen()
        game_loop(player_names)


init_db()
menu_choice = main_menu()
if menu_choice == "start":
    player_names = name_entry_screen()
    game_loop(player_names)

pygame.quit()
