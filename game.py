import pygame



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

background = pygame.image.load("images/background.jpg")
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

def draw_button(text, rect, pressed=False):
    if pressed:
        width, height = rect.size
        new_width = int(width * button_scale_factor)
        new_height = int(height * button_scale_factor)
        rect = pygame.Rect(rect.centerx - new_width // 2, rect.centery - new_height // 2, new_width, new_height)

    pygame.draw.rect(screen, YELLOW, rect, border_radius=10)

    text_surf = font.render(text, True, SHADOW_COLOR)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect.move(2, 2))

    text_surf = font.render(text, True, WHITE)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)

def draw_volume_slider(position):
    slider_rect = pygame.Rect(335, 180, 200, 20)
    pygame.draw.rect(screen, WHITE, slider_rect)
    pygame.draw.rect(screen, BLUE, pygame.Rect(335, 180, position, 20))
    return slider_rect

def toggle_fullscreen():
    global screen, fullscreen
    if not fullscreen:
        screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
        fullscreen = True
    else:
        screen = pygame.display.set_mode((screen_width, screen_height))
        fullscreen = False

in_settings = False
fullscreen = False
dragging_slider = False
slider_start_x = 335

while running:
    if in_settings:
        screen.blit(background, (0, 0))

        fullscreen_text = "Fullscreen: On" if fullscreen else "Fullscreen: Off"
        draw_button(fullscreen_text, pygame.Rect(250, 100, 300, 50))

        pygame.draw.rect(screen, YELLOW, pygame.Rect(250, 170, 300, 40))
        music_text = font.render("Music", True, WHITE)
        screen.blit(music_text, (260, 180))

        slider_rect = draw_volume_slider(volume * 200)
        draw_button("Back to Menu", pygame.Rect(250, 500, 300, 50))

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
        screen.blit(background, (0, 0))

        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if buttons["Exit"].collidepoint(event.pos):
                    running = False
                elif buttons["Start"].collidepoint(event.pos):
                    print("Start button clicked")
                elif buttons["Settings"].collidepoint(event.pos):
                    in_settings = True

        for text, rect in buttons.items():
            pressed = button_pressed == text and current_time - button_pressed_time < click_animation_duration
            draw_button(text, rect, pressed)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

