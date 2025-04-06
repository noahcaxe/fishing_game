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

    if hovered:
        rect = rect.inflate(10, 5)

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
    player_y = window_height - 140
    player_width, player_height = 100, 120

    rod_enabled = False  
    fish_list = []
    fish_timer = 0
    FISH_SPAWN_TIME = 100

    score = 0
    time_limit = 60
    time_start = pygame.time.get_ticks()

    # Load images
    background_image = load_image("images/beach_background.png")
    player_img = load_image("images/stickman.png")
    player_caught_img = load_image("images/stickman_caught_fish.png")
    rod_with_line_img = load_image("images/rod_with_line.png") 
    rod_no_line_img = load_image("images/rod_no_line.png")      
    fish_img = load_image("images/fish.png")
    rod_invisible_img = load_image("images/rod_invisible.png")
    doroga_img = load_image("images/doroga.png")

    if background_image:
        background_image = pygame.transform.scale(background_image, (window_width, window_height))
    if player_img:
        player_img = pygame.transform.scale(player_img, (player_width, player_height))
    if player_caught_img:
        player_caught_img = pygame.transform.scale(player_caught_img, (120,130))
    if rod_with_line_img:
        rod_with_line_img = pygame.transform.scale(rod_with_line_img, (player_width, player_height))
    if rod_no_line_img:
        rod_no_line_img = pygame.transform.scale(rod_no_line_img, (player_width, player_height))
    if fish_img:
        fish_img = pygame.transform.scale(fish_img, (40, 30))
    if rod_invisible_img:
        rod_invisible_img = pygame.transform.scale(rod_invisible_img, (player_width, player_height))
    

    current_rod_img = rod_with_line_img

    font = pygame.font.Font(None, 36)

    # Direction and timers
    facing_right = True
    caught_fish_timer = 0
    CAUGHT_DISPLAY_TIME = 1000
    cooldown_timer = 0

    def spawn_fish():
        fish_y = random.randint(player_y - 200, player_y - 100)
        fish_x = random.choice([-40, window_width + 40])
        direction = 1 if fish_x < 0 else -1
        speed = random.uniform(2, 4) * direction
        fish_list.append([fish_x, fish_y, speed])
        

# Отрисовка рыбы
    

    running = True
    while running:
        window.fill(WHITE)
        fish_hooked = False
        current_time = pygame.time.get_ticks()

        

        # Rod status based on cooldown
        if current_time < cooldown_timer:
            rod_enabled = False
            current_rod_img = rod_with_line_img
        else:
            current_rod_img = rod_no_line_img if rod_enabled else rod_with_line_img

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if current_time >= cooldown_timer:
                        rod_enabled = not rod_enabled
                        print("Удочка достана!" if rod_enabled else "Удочка убрана!")
                    else:
                        print("Идёт перезарядка! Подожди.")
                    
                elif event.key == pygame.K_w and rod_enabled:
                    rod_x = player_x + (player_width // 2) - (rod_no_line_img.get_width() // 2)
                    rod_y = player_y
                    rod_rect = pygame.Rect(rod_x, 0, rod_no_line_img.get_width(), rod_y + rod_no_line_img.get_height())
                    
                    
                    for fish in fish_list:
                        fish_x, fish_y, fish_speed = fish
                        
                        # Отзеркалить рыбу в зависимости от направления
                        if fish_speed < 0:
                            fish_img_flipped = pygame.transform.flip(fish_img, True, False)
                        else:
                            fish_img_flipped = fish_img

                        # Отображаем рыбу
                        window.blit(fish_img_flipped, (fish_x, fish_y))
                
                    for fish in fish_list[:]:
                        
                        fish_rect = pygame.Rect(fish[0], fish[1], fish_img.get_width(), fish_img.get_height())
                        if rod_rect.colliderect(fish_rect):
                            print("Поймал рыбу!")
                            fish_list.remove(fish)
                            score += 1
                            fish_hooked = True
                            caught_fish_timer = pygame.time.get_ticks() + CAUGHT_DISPLAY_TIME

                    if not fish_hooked:
                        print("Промах!")
                        cooldown_timer = pygame.time.get_ticks() + 3500
                        rod_enabled = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player_x > 0:
            player_x -= 5
            facing_right = False
        if keys[pygame.K_d] and player_x < window_width - player_width:
            player_x += 5
            facing_right = True

        # Fish spawn logic
        fish_timer += 1
        if fish_timer >= FISH_SPAWN_TIME:
            spawn_fish()
            fish_timer = 0

        # Move fish
        for fish in fish_list[:]:
            fish[0] += fish[2]
            if fish[0] < -50 or fish[0] > window_width + 50:
                fish_list.remove(fish)

        # Draw background
        if background_image:
            window.blit(background_image, (0, 0))

        # Draw player
        if pygame.time.get_ticks() < caught_fish_timer:
            img = player_caught_img
            current_rod_img = rod_invisible_img
        else:
            img = player_img

        if not facing_right:
            img = pygame.transform.flip(img, True, False)

        window.blit(img, (player_x, player_y))

        # Draw rod with flip
        rod_img_to_draw = current_rod_img
        if not facing_right:
            rod_img_to_draw = pygame.transform.flip(current_rod_img, True, False)

        rod_x = player_x + (player_width // 2) - (rod_img_to_draw.get_width() // 2)
        rod_y = player_y - rod_img_to_draw.get_height()
        window.blit(rod_img_to_draw, (rod_x+25, 450))

        # Draw fish
        for fish in fish_list:
            window.blit(fish_img, (fish[0], fish[1]))

        # Draw HUD
        window.blit(font.render(f"Score: {score}", True, BLACK), (10, 10))
        time_remaining = max(0, time_limit - (pygame.time.get_ticks() - time_start) // 1000)
        window.blit(font.render(f"Time: {time_remaining}", True, BLACK), (window_width // 2 - 40, 10))

        # Cooldown bar
        if current_time < cooldown_timer:
            cooldown_progress = (cooldown_timer - current_time) / 3500
            bar_width = 100
            bar_height = 10
            bar_x = rod_x  + (player_width // 2) - (bar_width // 2) + 20
            bar_y = rod_y + 100

            pygame.draw.rect(window, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height), border_radius=3)
            pygame.draw.rect(window, (255, 50, 50), (bar_x, bar_y, bar_width * cooldown_progress, bar_height), border_radius=3)
            pygame.draw.rect(window, (0, 0, 0), (bar_x, bar_y, bar_width, bar_height), 2, border_radius=3)
        

        clock.tick(60)
        pygame.display.update()
        
        if time_remaining <= 0:
            print("Время вышло!")
            running = False
            menu()

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
    volume_bar_rect = pygame.Rect(250, 195, 300, 10)

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

            yellow_bg_rect = pygame.Rect(250, 160, 300, 65)

            pygame.draw.rect(screen, (255, 215, 69), yellow_bg_rect, border_radius=10)

            volume_bar_inner_x = yellow_bg_rect.x + 5
            volume_bar_inner_width = yellow_bg_rect.width - 10
            volume_bar_rect = pygame.Rect(volume_bar_inner_x, 200, volume_bar_inner_width, 10)

            pygame.draw.rect(screen, (180, 180, 180), volume_bar_rect, border_radius=10)
            fill_rect = pygame.Rect(volume_bar_rect.x, volume_bar_rect.y, int(volume * volume_bar_rect.width),
                                    volume_bar_rect.height)
            pygame.draw.rect(screen, (251, 255, 148), fill_rect, border_radius=10)

            pygame.draw.circle(screen, (255, 255, 255),
                               (volume_bar_rect.x + int(volume * volume_bar_rect.width), volume_bar_rect.y + 5), 8)

            font = pygame.font.SysFont("eastmanblack", 20)
            label_text = f"Volume: {int(volume * 100)}%"
            text_surf_shadow = font.render(label_text, True, (50, 50, 50))
            text_surf_main = font.render(label_text, True, (255, 255, 255))
            text_rect = text_surf_main.get_rect(
                midtop=(yellow_bg_rect.centerx, yellow_bg_rect.y + 10))
            screen.blit(text_surf_shadow, text_rect.move(2, 2))
            screen.blit(text_surf_main, text_rect)


        else:
            for text, rect in buttons.items():
                hovered = rect.collidepoint(mouse_pos)
                pressed = button_pressed == text and current_time - button_pressed_time < click_animation_duration
                draw_button(screen, text, rect, hovered, pressed)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


menu()
