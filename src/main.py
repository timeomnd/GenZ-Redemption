import pygame
import sys
import random
import Environment as e
import Speed as s
import Item

#const
SCREEN_WIDTH = 400  # Format vertical type Doodle Jump
SCREEN_HEIGHT = 600
FPS = 60
PLATFORM_COLOR = (34, 177, 76)
SCORE = 0


def init_display():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Doodle Shoot Platformer")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 24, bold=True)

    bg = e.background()
    if bg:
        bg_y = SCREEN_HEIGHT - bg.get_height()
    else:
        bg_y = 0

    return screen, clock, font, bg, bg_y


def init_entities():
    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    bullets_group = pygame.sprite.Group()
    items_group = pygame.sprite.Group()

    # 1. SOL de départ
    start_ground = e.Platform(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40)
    all_sprites.add(start_ground)
    platforms.add(start_ground)

    # 2. Plateformes initiales adaptées à la hauteur
    spacing = SCREEN_HEIGHT // 5
    for i in range(6):
        p = e.Platform(random.randint(0, SCREEN_WIDTH - 60), i * spacing, 60, 15)
        all_sprites.add(p)
        platforms.add(p)

    player = s.Speed(platforms, all_sprites, bullets_group)
    all_sprites.add(player)

    return all_sprites, platforms, bullets_group, items_group, player

def handle_events(player):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False # Retourne False pour arrêter le jeu (running = False)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
            if event.key == pygame.K_TAB:
                player.inventory.cycle_weapon()
    return True # Le jeu continue

def handle_collisions(player, items_group):
    hits_items = pygame.sprite.spritecollide(player, items_group, True)
    for item in hits_items:
        if hasattr(item, 'weapon_type'):
            player.inventory.add_weapon(item.weapon_type)


def spawn_puff(platform, items_group, all_sprites, player):
    puff_dict = {
        "red": Item.PuffStrawberryItem,
        "yellow": Item.PuffBananaItem,
        "blue": Item.PuffBlueberryItem,
        "black": Item.PuffBlackBerryItem
    }

    map_weapons = [item.weapon_type for item in items_group if hasattr(item, 'weapon_type')]
    available_classes = []

    for weapon_name, puff_class in puff_dict.items():
        if weapon_name not in map_weapons and not player.inventory.has_weapon(weapon_name):
            available_classes.append(puff_class)

    if available_classes:
        chosen_class = random.choice(available_classes)
        new_item = chosen_class(platform.rect.centerx, platform.rect.top - 20)
        items_group.add(new_item)
        all_sprites.add(new_item)


def update_scrolling_and_spawns(player, bg, bg_y, total_scroll, current_score, items_group, platforms, all_sprites):
    if player.rect.top <= SCREEN_HEIGHT / 3:
        scroll_dist = abs(player.vel_y)
        total_scroll += scroll_dist

        if int(total_scroll) > current_score:
            current_score = int(total_scroll)

        player.rect.y += scroll_dist

        if bg:
            bg_y += scroll_dist * 0.1

        for item in items_group:
            item.rect.y += scroll_dist
            item.base_y += scroll_dist
            if item.rect.y > SCREEN_HEIGHT:
                item.kill()

        for plat in platforms:
            plat.rect.y += scroll_dist
            if plat.rect.top >= SCREEN_HEIGHT:
                plat.kill()
                highest_plat_y = min([p.rect.y for p in platforms])

                MIN_GAP = 60
                MAX_GAP = 130
                new_y = highest_plat_y - random.randint(MIN_GAP, MAX_GAP)
                new_p = e.Platform(random.randint(0, SCREEN_WIDTH - 60), new_y, 60, 15)

                all_sprites.add(new_p)
                platforms.add(new_p)

                if random.randint(1, 10) <= 10:
                    spawn_puff(new_p, items_group, all_sprites, player)

    return bg_y, total_scroll, current_score

def draw_screen(screen, bg, bg_y, all_sprites, current_score, player, font):
    if bg:
        screen.fill((135, 206, 235))
        screen.blit(bg, (0, bg_y))
    else:
        screen.fill((135, 206, 235))

    all_sprites.draw(screen)

    # Affichage du score
    score_surf = font.render(f"Score : {current_score}", True, (255, 255, 255))
    screen.blit(score_surf, (10, 10))

    # Affichage de l'inventaire
    player.inventory.draw_ui(screen, SCREEN_HEIGHT)

    pygame.display.flip()

def save_scores(current_score):
    try:
        with open("../src/Score/last_score.txt", "w") as f_last:
            f_last.write(str(current_score))

        meilleur_score = 0
        try:
            with open("../src/Score/best_score.txt", "r") as f_best:
                contenu = f_best.read().strip()
                if contenu:
                    meilleur_score = int(contenu)
        except FileNotFoundError:
            meilleur_score = 0

        if current_score > meilleur_score:
            with open("../src/Score/best_score.txt", "w") as f_best:
                f_best.write(str(current_score))

    except Exception as error:
        print(f"Erreur lors de la sauvegarde : {error}")


def main():
    global SCORE
    SCORE = 0

    # 1. Initialisation
    screen, clock, font, bg, bg_y = init_display()
    all_sprites, platforms, bullets_group, items_group, player = init_entities()

    running = True
    game_over = False
    total_scroll = 0

    # 2. Boucle Principale
    while running:
        clock.tick(FPS)

        # A. Gestion des événements clavier
        running = handle_events(player)

        # B. Mise à jour des positions
        all_sprites.update()

        # C. Gestion des collisions (Ramasser les objets)
        handle_collisions(player, items_group)

        # D. Gestion du défilement et génération des objets
        bg_y, total_scroll, SCORE = update_scrolling_and_spawns(
            player, bg, bg_y, total_scroll, SCORE, items_group, platforms, all_sprites
        )

        # E. Condition de défaite
        if player.rect.top > SCREEN_HEIGHT:
            print(f"Game Over! Score final: {SCORE}")
            game_over = True
            running = False

        # F. Dessiner l'écran
        draw_screen(screen, bg, bg_y, all_sprites, SCORE, player, font)

    # 3. Fin du jeu et Sauvegarde
    save_scores(SCORE)

    if game_over:
        return

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()