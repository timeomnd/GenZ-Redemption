import pygame
import sys
import random
import Environment as e
import Speed as s
SCREEN_WIDTH = 400  # Format vertical type Doodle Jump
SCREEN_HEIGHT = 600
FPS = 60

# Couleurs
PLATFORM_COLOR = (34, 177, 76)

SCORE = 0
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Doodle Shoot Platformer")
    clock = pygame.time.Clock()

    bg = e.background()

    # Groupes de sprites
    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    bullets_group = pygame.sprite.Group()

    # 1. Création du SOL de départ (largeur totale pour ne pas tomber)
    start_ground = e.Platform(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40)
    all_sprites.add(start_ground)
    platforms.add(start_ground)

    # 2. Création des plateformes initiales au-dessus
    for i in range(5):
        p = e.Platform(random.randint(0, SCREEN_WIDTH - 60), i * 120, 60, 15)
        all_sprites.add(p)
        platforms.add(p)

    # 3. Création du joueur
    player = s.Speed(platforms, all_sprites, bullets_group)
    all_sprites.add(player)

    running = True
    while running:
        clock.tick(FPS)

        # Événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()

        # Mise à jour
        all_sprites.update()

        # LOGIQUE DE SCROLLING (Caméra qui monte)
        if player.rect.top <= SCREEN_HEIGHT / 3:
            # On descend tout le monde selon la vitesse du joueur
            scroll_dist = abs(player.vel_y)
            player.rect.y += scroll_dist
            for plat in platforms:
                plat.rect.y += scroll_dist
                # Recyclage des plateformes qui sortent par le bas
                if plat.rect.top >= SCREEN_HEIGHT:
                    plat.kill()
                    new_p = e.Platform(random.randint(0, SCREEN_WIDTH - 60),
                                     random.randint(-50, 0), 60, 15)
                    all_sprites.add(new_p)
                    platforms.add(new_p)

        # Condition de défaite (Game Over)
        if player.rect.top > SCREEN_HEIGHT:
            print("Game Over!")
            print(SCORE)
            running = False

        # Dessin
        if bg:
            screen.blit(bg, (0, 0))
        else:
            screen.fill((135, 206, 235))

        all_sprites.draw(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()