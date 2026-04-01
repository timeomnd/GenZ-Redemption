import pygame
import main
import sys

# --- CONFIGURATION ---
pygame.init()

# 1. Résolution pour le menu
monitor_info = pygame.display.Info()
WIDTH = 400
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gen Z Redemption - Menu")

# Polices
font = pygame.font.SysFont("agencyfb", 50, bold=True)
font_small = pygame.font.SysFont("agencyfb", 20, bold=True)

# --- FONCTIONS ---
def read_score(filename):
    try:

        with open(filename, "r") as f:
            value = f.read().strip()
            return int(value) if value else 0
    except (FileNotFoundError, ValueError):
        pass
    return 0

# --- CHARGEMENT DES RESSOURCES ---

last_score = read_score("../src/Score/last_score.txt")
best_score = read_score("../src/Score/best_score.txt")

# Fond d'écran
bg_menu = pygame.image.load("../assets/fond.png").convert()
bg_menu = pygame.transform.scale(bg_menu, (WIDTH, HEIGHT))


# Bouton Play centré dynamiquement
play_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 40, 200, 80)

# Musique
try:
    pygame.mixer.music.load("../assets/sound/musique_fond.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)
except:
    pass

# --- BOUCLE PRINCIPALE ---
running = True
while running:
    if bg_menu:
        screen.blit(bg_menu, (0, 0))
    else:
        screen.fill((30, 30, 30))

    # --- TEXTES ---
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
            if event.button == 1 and play_button.collidepoint(event.pos):
                # On coupe la musique du menu avant de lancer le jeu
                pygame.mixer.music.stop()
                
                # Lancement du jeu (SCORE sera mis à 0 dans main.main)
                main.main()
                
                # Au retour du jeu, on relance la musique et on actualise les scores

                pygame.mixer.music.play(-1)
                last_score = read_score("../src/Score/last_score.txt")
                best_score = read_score("../src/Score/best_score.txt")

    pygame.display.flip()

pygame.quit()
sys.exit()