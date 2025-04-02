import pygame
import random
import os

# Функция для загрузки изображения
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

# Функция для отрисовки кнопки
def draw_button(screen, text, rect, pressed=False):
    font = pygame.font.SysFont("eastmanblack", 20)
    WHITE = (255, 255, 255)
    YELLOW = (255, 215, 69)
    SHADOW_COLOR = (50, 50, 50)

    # Эффект нажатия
    if pressed:
        width, height = rect.size
        new_width = int(width * 0.9)
        new_height = int(height * 0.9)
        rect = pygame.Rect(rect.centerx - new_width // 2, rect.centery - new_height // 2, new_width, new_height)

    pygame.draw.rect(screen, YELLOW, rect, border_radius=10)

    text_surf = font.render(text, True, SHADOW_COLOR)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect.move(2, 2))

    text_surf = font.render(text, True, WHITE)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)

# Игровой процесс (функция для игры)
def fishing_game():
    pygame.init()

    # Параметры экрана
    window_width = 800
    window_height = 600
    window = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Fishing Game")
    clock = pygame.time.Clock()

    # Цвета
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # Переменные для игрока
    player_x = window_width // 2 - 50
    player_y = window_height - 120
    player_width = 100
    player_height = 120

    # Переменные для рыбы
    fish_list = []
    FISH_SPAWN_TIME = 100
    fish_timer = 0
    score = 0
    time_limit = 60
    time_start = pygame.time.get_ticks()

    # Загружаем изображения
    background_image = load_image("images/beach_background.png")
    if background_image:
        background_image = pygame.transform.scale(background_image, (window_width, window_height))

    player_img = load_image("images/stickman.png")
    if player_img:
        player_img = pygame.transform.scale(player_img, (player_width, player_height))

    rod_img = load_image("images/rod.png")
    if rod_img:
        rod_img = pygame.transform.scale(rod_img, (30, 100))

    fish_img = load_image("images/fish.png")
    if fish_img:
        fish_img = pygame.transform.scale(fish_img, (40, 30))

    font = pygame.font.Font(None, 36)

    # Функция для спауна рыбы
    def spawn_fish():
        water_zone_start = int(window_height * 0.3)
        fish_y = random.randint(water_zone_start, window_height - 50)
        fish_x = random.choice([-40, window_width + 40])  # Spawn outside left or right screen
        direction = 1 if fish_x < 0 else -1
        speed = random.uniform(2, 4) * direction
        fish_list.append([fish_x, fish_y, speed])

    # Игровой цикл
    running = True
    while running:
        window.fill(WHITE)

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Управление движением игрока
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= 5
        if keys[pygame.K_RIGHT] and player_x < window_width - player_width:
            player_x += 5

        # Спавн рыбы
        fish_timer += 1
        if fish_timer >= FISH_SPAWN_TIME:
            spawn_fish()
            fish_timer = 0

        # Движение рыбы
        for fish in fish_list[:]:
            fish[0] += fish[2]
            if fish[0] < -50 or fish[0] > window_width + 50:
                fish_list.remove(fish)

        # Отображение фона
        if background_image:
            window.blit(background_image, (0, 0))

        # Отображение игрока
        if player_img:
            window.blit(player_img, (player_x, player_y))

        # Отображение удочки
        if rod_img:
            rod_x = player_x + (player_width // 2) - (rod_img.get_width() // 2)
            rod_y = player_y - rod_img.get_height()
            window.blit(rod_img, (rod_x, rod_y))

        # Отображение рыбы
        for fish in fish_list:
            window.blit(fish_img, (fish[0], fish[1]))

        # Отображение счета
        score_text = font.render(f"Score: {score}", True, BLACK)
        window.blit(score_text, (10, 10))

        # Отображение таймера
        time_elapsed = (pygame.time.get_ticks() - time_start) // 1000
        time_remaining = max(0, time_limit - time_elapsed)
        timer_text = font.render(f"Time: {time_remaining}", True, BLACK)
        window.blit(timer_text, (window_width // 2 - 40, 10))

        if time_remaining <= 0:
            running = False

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

# Главное меню
def menu():
    pygame.init()
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    running = True

    WHITE = (255, 255, 255)
    YELLOW = (255, 215, 69)
    BLUE = (47, 30, 199)
    BLACK = (0, 0, 0)
    SHADOW_COLOR = (50, 50, 50)

    # Загружаем фон с помощью функции load_image
    background = load_image("images/background.jpg")
    if background:
        background = pygame.transform.scale(background, (screen_width, screen_height))

    font = pygame.font.SysFont("eastmanblack", 20)

    buttons = {
        "Start": pygame.Rect(250, 236, 300, 68),
        "Settings": pygame.Rect(250, 314, 145, 50),
        "Exit": pygame.Rect(405, 314, 145, 50)
    }

    button_pressed = None
    button_pressed_time = 0
    click_animation_duration = 150
    button_scale_factor = 0.9

    volume = 1.0
    pygame.mixer.music.set_volume(volume)

    in_settings = False
    fullscreen = False
    dragging_slider = False
    slider_start_x = 335

    # Функция для отрисовки ползунка громкости
    def draw_volume_slider(position):
        slider_rect = pygame.Rect(335, 180, 200, 20)
        pygame.draw.rect(screen, WHITE, slider_rect)
        pygame.draw.rect(screen, BLUE, pygame.Rect(335, 180, position, 20))
        return slider_rect

    # Функция для включения/выключения полноэкранного режима
    def toggle_fullscreen():
        
        global screen, fullscreen
        fullscreen = False
        if not fullscreen:
            screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
            fullscreen = True
        else:
            screen = pygame.display.set_mode((screen_width, screen_height))
            fullscreen = False

    while running:
        if in_settings:
            if background:
                screen.blit(background, (0, 0))

            fullscreen_text = "Fullscreen: On" if fullscreen else "Fullscreen: Off"
            draw_button(screen, fullscreen_text, pygame.Rect(250, 100, 300, 50))

            pygame.draw.rect(screen, YELLOW, pygame.Rect(250, 170, 300, 40))
            music_text = font.render("Music", True, WHITE)
            screen.blit(music_text, (260, 180))

            slider_rect = draw_volume_slider(volume * 200)
            draw_button(screen, "Back to Menu", pygame.Rect(250, 500, 300, 50))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.Rect(250, 100, 300, 50).collidepoint(event.pos):
                        toggle_fullscreen()
                    if pygame.Rect(250, 500, 300, 50).collidepoint(event.pos):
                        in_settings = False
                    if slider_rect.collidepoint(event.pos):
                        dragging_slider = True
                        slider_start_x = max(min(event.pos[0] - 335, 200), 0)
                        volume = slider_start_x / 200

                elif event.type == pygame.MOUSEMOTION:
                    if dragging_slider:
                        slider_start_x = max(min(event.pos[0] - 335, 200), 0)
                        volume = slider_start_x / 200
                        pygame.mixer.music.set_volume(volume)

                elif event.type == pygame.MOUSEBUTTONUP:
                    dragging_slider = False

        else:
            if background:
                screen.blit(background, (0, 0))

            current_time = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if buttons["Exit"].collidepoint(event.pos):
                        running = False
                    elif buttons["Start"].collidepoint(event.pos):
                        fishing_game()  # Start the fishing game
                    elif buttons["Settings"].collidepoint(event.pos):
                        in_settings = True

            for text, rect in buttons.items():
                pressed = button_pressed == text and current_time - button_pressed_time < click_animation_duration
                draw_button(screen, text, rect, pressed)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

menu()  # Call the menu to start the game
