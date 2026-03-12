import pygame
import main  # Ton fichier de jeu renommé

# Configuration
WIDTH, HEIGHT = 400, 600
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gen Z Redemption - Menu")

# Police
font = pygame.font.SysFont("Arial", 50, bold=True)

# 1. Chargement du fond
try:
    bg_menu = pygame.image.load('assets/fond.png').convert()
    bg_menu = pygame.transform.scale(bg_menu, (WIDTH, HEIGHT))
except:
    bg_menu = None # Sécurité si l'image est manquante

# 2. Bouton PLAY
play_button = pygame.Rect(100, 260, 200, 80)

running = True
while running:
    # --- AFFICHAGE ---
    if bg_menu:
        screen.blit(bg_menu, (0, 0))
    else:
        screen.fill((30, 30, 30))

    # Petit effet visuel : change de couleur si la souris est dessus
    mouse_pos = pygame.mouse.get_pos()
    button_color = (50, 220, 90) if play_button.collidepoint(mouse_pos) else (34, 177, 76)
    
    # Dessin du bouton avec bordure arrondie
    pygame.draw.rect(screen, button_color, play_button, border_radius=15)
    
    # Texte du bouton
    text_surf = font.render("PLAY", True, (255, 255, 255))
    text_rect = text_surf.get_rect(center=play_button.center)
    screen.blit(text_surf, text_rect)

    # --- EVENEMENTS ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Clic gauche
                if play_button.collidepoint(event.pos):
                    # Lancement du jeu
                    main.main()

    pygame.display.flip()

pygame.quit()