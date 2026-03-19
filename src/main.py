import pygame
import sys
import random
import Environment as e
import Speed as s

FPS = 60
PLATFORM_COLOR = (34, 177, 76)

SCREEN_WIDTH = 400  
SCREEN_HEIGHT = 600


def main():
    global SCORE
    SCORE = 0  
    
    pygame.init()

    pygame.mixer.music.load("../assets/sound/musique_saut.mp3")
    pygame.mixer.music.set_volume(0.5)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Doodle Shoot Platformer")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("Arial", 24, bold=True)
    bg = e.background()

    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    bullets_group = pygame.sprite.Group()

    # 1. SOL de départ
    start_ground = e.Platform(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40)
    all_sprites.add(start_ground)
    platforms.add(start_ground)

    # 2. Plateformes initiales adaptées à la hauteur
    # On calcule l'espacement pour que le jeu reste jouable peu importe SCREEN_HEIGHT
    spacing = SCREEN_HEIGHT // 5
    for i in range(6):
        p = e.Platform(random.randint(0, SCREEN_WIDTH - 60), i * spacing, 60, 15)
        all_sprites.add(p)
        platforms.add(p)

    player = s.Speed(platforms, all_sprites, bullets_group)
    all_sprites.add(player)

    running = True
    game_over = False 
    total_scroll = 0 
    
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()

        all_sprites.update()
        # LOGIQUE DE SCROLLING
        if player.rect.top <= SCREEN_HEIGHT / 3:
            scroll_dist = abs(player.vel_y)
            total_scroll += scroll_dist
            if int(total_scroll) > SCORE:
                SCORE = int(total_scroll)

            player.rect.y += scroll_dist
            for plat in platforms:
                plat.rect.y += scroll_dist
                if plat.rect.top >= SCREEN_HEIGHT:
                    plat.kill()
                    # On fait réapparaître en haut
                    new_p = e.Platform(random.randint(0, SCREEN_WIDTH - 60),
                                     random.randint(-spacing, 0), 60, 15)
                    all_sprites.add(new_p)
                    platforms.add(new_p)

        # Défaite
        if player.rect.top > SCREEN_HEIGHT:
            print(f"Game Over! Score final: {SCORE}")
            game_over = True
            running = False

        # Dessin
        if bg:
            screen.blit(bg, (0, 0))
        else:
            screen.fill((135, 206, 235))

        all_sprites.draw(screen)
        score_surf = font.render(f"Score : {SCORE}", True, (255, 255, 255))
        screen.blit(score_surf, (10, 10))
        pygame.display.flip()

    # --- SAUVEGARDE (Tes chemins d'origine) ---
    try:
        with open("../src/Score/last_score.txt", "w") as f_last:
            f_last.write(str(SCORE))

        meilleur_score = 0
        try:
            with open("../src/Score/best_score.txt", "r") as f_best:
                contenu = f_best.read().strip()
                if contenu:
                    meilleur_score = int(contenu)
        except FileNotFoundError:
            meilleur_score = 0

        if SCORE > meilleur_score:
            with open("../src/Score/best_score.txt", "w") as f_best:
                f_best.write(str(SCORE))

    except Exception as error:
        print(f"Erreur lors de la sauvegarde : {error}")
    
    if game_over:
        return 

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()