import pygame
import random
import os

fullscreen = False  
volume = 0.5

def load_image(filename):
    path = os.path.join(os.path.dirname(__file__), filename)
    if not os.path.exists(path):
        print(f"Image not found: {path}")
        return None
    try:
        return pygame.image.load(path).convert_alpha()
    except pygame.error as e:
        print(f"Error loading image {filename}: {e}")
        return None

def draw_button(screen, text, rect, hovered=False, pressed=False):
    font = pygame.font.SysFont("eastmanblack", 20)
    WHITE = (255, 255, 255)
    YELLOW = (255, 215, 69)
    DARK_YELLOW = (180, 190, 50)
    SHADOW_COLOR = (50, 50, 50)

    # Размер кнопки при наведении
    if hovered:
        rect = rect.inflate(10, 5)

    # Цвет при нажатии
    color = DARK_YELLOW if pressed else YELLOW

    pygame.draw.rect(screen, color, rect, border_radius=10)
    text_surf = font.render(text, True, SHADOW_COLOR)
    screen.blit(text_surf, text_surf.get_rect(center=rect.center).move(2, 2))
    text_surf = font.render(text, True, WHITE)
    screen.blit(text_surf, text_surf.get_rect(center=rect.center))

def fishing_game():
    global fullscreen  
    pygame.init()

    window_width, window_height = 800, 600
    window = pygame.display.set_mode((window_width, window_height), pygame.FULLSCREEN if fullscreen else 0)
    pygame.display.set_caption("Fishing Game")
    clock = pygame.time.Clock()

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    player_x = window_width // 2 - 50
    player_y = window_height - 120
    player_width, player_height = 100, 120

    fish_list = []
    fish_timer = 0
    FISH_SPAWN_TIME = 100

    score = 0
    time_limit = 60
    time_start = pygame.time.get_ticks()

    background_image = load_image("images/beach_background.png")
    player_img = load_image("images/stickman.png")
    rod_img = load_image("images/rod.png")
    fish_img = load_image("images/fish.png")

    if background_image:
        background_image = pygame.transform.scale(background_image, (window_width, window_height))
    if player_img:
        player_img = pygame.transform.scale(player_img, (player_width, player_height))
    if rod_img:
        rod_img = pygame.transform.scale(rod_img, (30, 100))
    if fish_img:
        fish_img = pygame.transform.scale(fish_img, (40, 30))

    font = pygame.font.Font(None, 36)

    def spawn_fish():
        center_y = window_height // 2
        fish_y = random.randint(center_y - 25, center_y + 25)
        fish_x = random.choice([-40, window_width + 40])
        direction = 1 if fish_x < 0 else -1
        speed = random.uniform(2, 4) * direction
        fish_list.append([fish_x, fish_y, speed])

    running = True
    while running:
        window.fill(WHITE)
        fish_hooked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    rod_x = player_x + (player_width // 2) - (rod_img.get_width() // 2)
                    rod_y = player_y - rod_img.get_height()
                    rod_rect = pygame.Rect(rod_x, rod_y, rod_img.get_width(), rod_img.get_height())
                    for fish in fish_list[:]:
                        fish_rect = pygame.Rect(fish[0], fish[1], fish_img.get_width(), fish_img.get_height())
                        if rod_rect.colliderect(fish_rect):
                            fish_list.remove(fish)
                            score += 10
                            fish_hooked = True
                    if not fish_hooked:
                        print("Промах!")

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= 5
        if keys[pygame.K_RIGHT] and player_x < window_width - player_width:
            player_x += 5

        fish_timer += 1
        if fish_timer >= FISH_SPAWN_TIME:
            spawn_fish()
            fish_timer = 0

        for fish in fish_list[:]:
            fish[0] += fish[2]
            if fish[0] < -50 or fish[0] > window_width + 50:
                fish_list.remove(fish)

        rod_x = player_x + (player_width // 2) - (rod_img.get_width() // 2)
        rod_y = player_y - rod_img.get_height()

        if background_image:
            window.blit(background_image, (0, 0))
        if player_img:
            window.blit(player_img, (player_x, player_y))
        if rod_img:
            window.blit(rod_img, (rod_x, rod_y))

        for fish in fish_list:
            window.blit(fish_img, (fish[0], fish[1]))

        window.blit(font.render(f"Score: {score}", True, BLACK), (10, 10))
        time_remaining = max(0, time_limit - (pygame.time.get_ticks() - time_start) // 1000)
        window.blit(font.render(f"Time: {time_remaining}", True, BLACK), (window_width // 2 - 40, 10))

        if time_remaining <= 0:
            running = False

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

def menu():
    global fullscreen, volume
    pygame.init()
    screen_width, screen_height = 800, 600

    def create_window():
        flags = pygame.FULLSCREEN if fullscreen else 0
        return pygame.display.set_mode((screen_width, screen_height), flags)

    screen = create_window()
    clock = pygame.time.Clock()
    background = load_image("images/background.jpg")
    if background:
        background = pygame.transform.scale(background, (screen_width, screen_height))

    buttons = {
        "Start": pygame.Rect(250, 236, 300, 68),
        "Settings": pygame.Rect(250, 314, 145, 50),
        "Exit": pygame.Rect(405, 314, 145, 50)
    }

    settings_buttons = {
        "Fullscreen": pygame.Rect(250, 100, 300, 50),
        "Back": pygame.Rect(250, 500, 300, 50)
    }

    button_pressed = None
    button_pressed_time = 0
    click_animation_duration = 150
    in_settings = False

    dragging_volume = False
    volume_bar_rect = pygame.Rect(250, 180, 300, 10)

    running = True
    while running:
        screen.fill((0, 0, 0))
        if background:
            screen.blit(background, (0, 0))

        current_time = pygame.time.get_ticks()
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if in_settings:
                    for text, rect in settings_buttons.items():
                        if rect.collidepoint(event.pos):
                            button_pressed = text
                            button_pressed_time = current_time
                            if text == "Fullscreen":
                                fullscreen = not fullscreen
                                screen = create_window()
                                if background:
                                    background = pygame.transform.scale(background, (screen_width, screen_height))
                            elif text == "Back":
                                in_settings = False
                    if volume_bar_rect.collidepoint(event.pos):
                        dragging_volume = True
                else:
                    for text, rect in buttons.items():
                        if rect.collidepoint(event.pos):
                            button_pressed = text
                            button_pressed_time = current_time
                            if text == "Exit":
                                running = False
                            elif text == "Start":
                                fishing_game()
                            elif text == "Settings":
                                in_settings = True
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging_volume = False

        if dragging_volume and in_settings:
            rel_x = mouse_pos[0] - volume_bar_rect.x
            volume = max(0.0, min(1.0, rel_x / volume_bar_rect.width))

        if in_settings:
            for text, rect in settings_buttons.items():
                hovered = rect.collidepoint(mouse_pos)
                pressed = button_pressed == text and current_time - button_pressed_time < click_animation_duration
                label = f"Fullscreen: {'On' if fullscreen else 'Off'}" if text == "Fullscreen" else "Back to Menu"
                draw_button(screen, label, rect, hovered, pressed)

            # Volume bar
            pygame.draw.rect(screen, (180, 180, 180), volume_bar_rect)
            fill_rect = pygame.Rect(volume_bar_rect.x, volume_bar_rect.y, int(volume * volume_bar_rect.width), volume_bar_rect.height)
            pygame.draw.rect(screen, (255, 215, 0), fill_rect)
            pygame.draw.circle(screen, (255, 255, 255), (volume_bar_rect.x + int(volume * volume_bar_rect.width), volume_bar_rect.y + 5), 8)

            # Volume label
            font = pygame.font.SysFont("arial", 24)
            text = font.render(f"Volume: {int(volume * 100)}%", True, (255, 255, 255))
            screen.blit(text, (volume_bar_rect.x, volume_bar_rect.y - 30))
        else:
            for text, rect in buttons.items():
                hovered = rect.collidepoint(mouse_pos)
                pressed = button_pressed == text and current_time - button_pressed_time < click_animation_duration
                draw_button(screen, text, rect, hovered, pressed)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
menu()
