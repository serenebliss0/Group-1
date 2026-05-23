import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 1280, 720

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cinematic Settings UI")

clock = pygame.time.Clock()

BG = (5, 3, 2)
ORANGE = (170, 70, 20)
LIGHT = (230, 220, 205)
DIM = (120, 90, 70)
LINE = (45, 25, 15)

title_font = pygame.font.SysFont("georgia", 72, bold=True)
body_font = pygame.font.SysFont("consolas", 18)
small_font = pygame.font.SysFont("consolas", 14)
button_font = pygame.font.SysFont("consolas", 16)


class Settings:
    def __init__(self):
        self.text_speed = "normal"
        self.keybinds = {
            "AUDIO": "A",
            "BRIGHTNESS": "B",
            "PERSONAL INFO": "C"
        }

    def save(self):
        print("Settings Saved!")


settings = Settings()


def draw_text(text, font, color, x, y):
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))


def draw_ui():
    screen.fill(BG)

    pygame.draw.line(screen, LINE, (640, 0), (640, HEIGHT), 1)

    draw_text("< BACK", small_font, DIM, 40, 30)

    draw_text("Settings", title_font, LIGHT, 70, 310)

    description = [
        "Adjust keybindings, audio preferences, and",
        "narrative pacing to suit your experience."
    ]

    y = 410
    for line in description:
        draw_text(line, body_font, DIM, 75, y)
        y += 28

    draw_text("KEYBINDINGS", small_font, ORANGE, 700, 140)

    start_y = 200

    for i, (action, key) in enumerate(settings.keybinds.items()):
        yy = start_y + i * 90

        draw_text(action, body_font, LIGHT, 700, yy)

        pygame.draw.line(screen, LINE, (700, yy + 42), (1140, yy + 42), 1)

        key_rect = pygame.Rect(1160, yy - 5, 38, 38)

        pygame.draw.rect(screen, ORANGE, key_rect, 1)

        key_text = body_font.render(key, True, ORANGE)
        screen.blit(key_text, key_text.get_rect(center=key_rect.center))

    draw_text("EXPERIENCE", small_font, ORANGE, 700, 470)

    draw_text("Text Speed", body_font, LIGHT, 700, 540)

    pygame.draw.line(screen, LINE, (700, 585), (1140, 585), 1)

    speed_rect = pygame.Rect(1110, 523, 88, 38)

    pygame.draw.rect(screen, ORANGE, speed_rect, 1)

    speed_text = button_font.render(settings.text_speed, True, ORANGE)

    screen.blit(speed_text, speed_text.get_rect(center=speed_rect.center))

    save_rect = pygame.Rect(700, 640, 500, 55)

    pygame.draw.rect(screen, ORANGE, save_rect, 1)

    save_text = button_font.render("SAVE & RETURN", True, LIGHT)

    screen.blit(save_text, (730, 658))

    return save_rect


running = True

while running:
    save_rect = draw_ui()

    back_rect = pygame.Rect(40, 30, 120, 40)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos

            # BACK
            if back_rect.collidepoint(mx, my):
                running = False
                sys.exit()

            # SAVE & RETURN
            if save_rect.collidepoint(mx, my):
                settings.save()
                running = False
                sys.exit()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()