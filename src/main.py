import pygame
import sys
import random
import Environment as e
import Speed as s
import Item
SCREEN_WIDTH = 400  # Format vertical type Doodle Jump
SCREEN_HEIGHT = 600
FPS = 60

# Couleurs
PLATFORM_COLOR = (34, 177, 76)

SCORE = 0
def main():
    global SCORE  # Réinitialisation du score à chaque partie
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Doodle Shoot Platformer")
    clock = pygame.time.Clock()
    # Police pour l'affichage du score
    font = pygame.font.SysFont("Arial", 24, bold=True)

    bg = e.background()

    # Groupes de sprites
    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    bullets_group = pygame.sprite.Group()
    items_group = pygame.sprite.Group()


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

    # Variables de jeu
    running = True
    game_over = False  # True si on perd, False si on ferme la fenêtre
    total_scroll = 0   # Hauteur totale parcourue vers le haut
    while running:
        clock.tick(FPS)

        # Événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()
                if event.key == pygame.K_TAB:
                    player.inventory.cycle_weapon()

        # Mise à jour
        all_sprites.update()
        # LOGIQUE DE COLLISION : RAMASSER LES ITEMS
        hits_items = pygame.sprite.spritecollide(player, items_group, True)  # True = détruit l'item de la map

        for item in hits_items:
            if hasattr(item, 'weapon_type'):
                player.inventory.add_weapon(item.weapon_type)

        # LOGIQUE DE SCROLLING (Caméra qui monte)
        if player.rect.top <= SCREEN_HEIGHT / 3:
            # On descend tout le monde selon la vitesse du joueur
            scroll_dist = abs(player.vel_y)
            total_scroll += scroll_dist

            # Le score dépend de la hauteur totale parcourue et ne peut que monter
            if int(total_scroll) > SCORE:
                SCORE = int(total_scroll)

            player.rect.y += scroll_dist

#logique pour supprimer les items et plateformes si ils sortent de l'écran et pour les faire descendre en même temps que l'écran
            for item in items_group:
                item.rect.y += scroll_dist
                item.base_y += scroll_dist
                if item.rect.y > SCREEN_HEIGHT :
                    item.kill()
            for plat in platforms:
                plat.rect.y += scroll_dist
                if plat.rect.top >= SCREEN_HEIGHT:
                    plat.kill()
                    new_p = e.Platform(random.randint(0, SCREEN_WIDTH - 60),
                                     random.randint(-50, 0), 60, 15)
                    all_sprites.add(new_p)
                    platforms.add(new_p)

                    if random.randint(1, 10) <= 10 :
                        puff_dict = {"red": Item.PuffStrawberryItem, "yellow": Item.PuffBananaItem, "blue": Item.PuffBlueberryItem, "black": Item.PuffBlackBerryItem}

                        map_weapons = [item.weapon_type for item in items_group if hasattr(item, 'weapon_type')]
                        available_classes = []
                        for weapon_name, puff_class in puff_dict.items():
                            # Vérification : Ni sur la map, Ni dans l'inventaire
                            if weapon_name not in map_weapons and not player.inventory.has_weapon(weapon_name):
                                available_classes.append(puff_class)

                            # S'il reste des puffs disponibles, on en choisit une au hasard
                        if available_classes:
                            chosen_class = random.choice(available_classes)
                            new_item = chosen_class(new_p.rect.centerx, new_p.rect.top - 20)

                            items_group.add(new_item)
                            all_sprites.add(new_item)
        # Condition de défaite (Game Over)
        if player.rect.top > SCREEN_HEIGHT:
            print(f"Game Over! Score final: {SCORE}")
            game_over = True
            running = False
        # --- DESSIN (Une seule fois par frame !) ---
        if bg:
            screen.blit(bg, (0, 0))
        else:
            screen.fill((135, 206, 235))

        all_sprites.draw(screen)

        # Affichage du score
        score_surf = font.render(f"Score : {SCORE}", True, (255, 255, 255))
        screen.blit(score_surf, (10, 10))

        # Affichage de l'inventaire
        player.inventory.draw_ui(screen, SCREEN_HEIGHT)

        pygame.display.flip()


    try:
        # Sauvegarder le score actuel
        with open("src/last_score.txt", "w") as f_last:
            f_last.write(str(SCORE))

        # Lire le meilleur score précédent
        try:
            with open("src/best_score.txt", "r") as f_best:
                contenu = f_best.read().strip()
                # Si le fichier est vide, on part de 0
                if (contenu):
                    meilleur_score = int(contenu) 
                else:
                    meilleur_score = 0
        except FileNotFoundError:
            meilleur_score = 0

        # Comparer et mettre à jour si nécessaire
        if SCORE > meilleur_score:
            with open("src/best_score.txt", "w") as f_best:
                f_best.write(str(SCORE))

    except Exception as error:
        print(f"Erreur lors de la sauvegarde : {error}")
    
    # Si on a perdu, on retourne simplement à l'appelant (le menu)
    if game_over:
        return

    # Si on a quitté via la croix, on ferme vraiment le jeu
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()