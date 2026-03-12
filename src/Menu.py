import pygame
import main 

# Configuration
WIDTH, HEIGHT = 400, 600
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gen Z Redemption - Menu")

# Polices
font = pygame.font.SysFont("agencyfb", 50, bold=True)
font_small = pygame.font.SysFont("agencyfb", 20, bold=True)  # Police plus petite pour le coin

# Lecture des scores depuis les fichiers texte
def read_score(filename):
    try:
        with open(filename, "r") as f:
            value = f.read().strip()
            return int(value)
    except (FileNotFoundError, ValueError):
        return 0

last_score = read_score("src/last_score.txt")
best_score = read_score("src/best_score.txt")

# 1. Chargement du fond
try:
    bg_menu = pygame.image.load('assets/fond.png').convert()
    bg_menu = pygame.transform.scale(bg_menu, (WIDTH, HEIGHT))
except:
    bg_menu = None 

play_button = pygame.Rect(100, 260, 200, 80)

running = True
while running:
    # --- AFFICHAGE ---
    if bg_menu:
        screen.blit(bg_menu, (0, 0))
    else:
        screen.fill((30, 30, 30))

    # --- TEXTE EN HAUT À GAUCHE ---
    version_text = font_small.render("v0.0.4 - Early Access", True, (200, 200, 200))
    screen.blit(version_text, (15, 15))

    last_score_text = font_small.render(f"Dernier score : {last_score}", True, (255, 255, 255))
    screen.blit(last_score_text, (15, 35))

    best_score_text = font_small.render(f"Meilleur score : {best_score}", True, (255, 255, 255))
    screen.blit(best_score_text, (15, 55))

    # --- BOUTON PLAY ---
    mouse_pos = pygame.mouse.get_pos()
    button_color = (50, 220, 90) if play_button.collidepoint(mouse_pos) else (34, 177, 76)
    
    pygame.draw.rect(screen, button_color, play_button, border_radius=15)
    
    text_surf = font.render("PLAY", True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=play_button.center)
    screen.blit(text_surf, text_rect)

    # --- EVENEMENTS ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: 
                if play_button.collidepoint(event.pos):
                    main.main()
                    # On recharge les scores après une partie
                    last_score = read_score("src/last_score.txt")
                    best_score = read_score("src/best_score.txt")

    pygame.display.flip()

pygame.quit()