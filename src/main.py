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
    bg_y = SCREEN_HEIGHT - bg.get_height() if bg else 0

    return screen, clock, font, bg, bg_y

def load_assets():
    sounds = {}
    try:
        sounds["collect"] = pygame.mixer.Sound("../assets/sounds/item_collect_sound_effect.mp3")
        sounds["collect"].set_volume(0.4)
    except Exception as err:
        print(f"Erreur chargement son collect : {err}")
        sounds["collect"] = None
    return sounds


def init_entities():
    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    bullets_group = pygame.sprite.Group()
    items_group = pygame.sprite.Group()

    start_ground = e.StartPlatform(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40)
    all_sprites.add(start_ground)
    platforms.add(start_ground)

    spacing = SCREEN_HEIGHT // 5
    for i in range(6):
        p = e.generate_random_platform(random.randint(0, SCREEN_WIDTH - 60), i * spacing, 60, 15)
        all_sprites.add(p)
        platforms.add(p)

    player = s.Speed(platforms, all_sprites, bullets_group)
    all_sprites.add(player)

    return all_sprites, platforms, bullets_group, items_group, player

def handle_events(player):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
            if event.key == pygame.K_TAB:
                player.inventory.cycle_weapon()
    return True

def handle_collisions(player, items_group, sounds):
    hits_items = pygame.sprite.spritecollide(player, items_group, True)
    for item in hits_items:
        if sounds["collect"]:
            sounds["collect"].play()

        if hasattr(item, 'weapon_type'):
            player.inventory.add_weapon(item.weapon_type)
        if hasattr(item, 'type') and item.type == "consumable":
            item.play_abilitie(player)

def spawn_consumable(platform, items_group, all_sprites):
    consumable_classes = [
        Item.Burger,
        Item.TastyCrousty,
        Item.Tacos,
        Item.TacosGratine,
        Item.Poppers,
        Item.Monster,
        Item.Redbull,
        Item.Frozen
    ]
    chosen_class = random.choice(consumable_classes)
    new_item = chosen_class(platform.rect.centerx, platform.rect.top -20)

    items_group.add(new_item)
    all_sprites.add(new_item)
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
        new_item = chosen_class(platform.rect.centerx, platform.rect.top - 25)
        items_group.add(new_item)
        all_sprites.add(new_item)


def update_scrolling_and_spawns(player, bg, bg_y, total_scroll, current_score, items_group, platforms, all_sprites):
    # Gestion du score et du défilement vertical
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

    # Génération des nouvelles plateformes et items
    while True:
        highest_plat_y = SCREEN_HEIGHT
        for p in platforms:
            if p.rect.y < highest_plat_y:
                highest_plat_y = p.rect.y

        if highest_plat_y <= 0:
            break

        new_y = highest_plat_y - random.randint(60, 130)
        new_p = e.generate_random_platform(random.randint(0, SCREEN_WIDTH - 60), new_y, 60, 15)

        all_sprites.add(new_p)
        platforms.add(new_p)

        # Spawn limité aux plateformes stables
        if new_p.type in ["normal", "bouncing"]:
            if random.randint(1, 100) <= 5: # 5% de chance pour les armes
                spawn_puff(new_p, items_group, all_sprites, player)
            elif random.randint(1, 100) <= 5: # 5% de chance pour les objets
                spawn_consumable(new_p, items_group, all_sprites)

    return bg_y, total_scroll, current_score

def draw_screen(screen, bg, bg_y, all_sprites, current_score, player, font, damage_timer):
    if bg:
        screen.fill((135, 206, 235))
        screen.blit(bg, (0, bg_y))
    else:
        screen.fill((135, 206, 235))

    all_sprites.draw(screen)

    if damage_timer > 0:
        e.draw_damage_flash(screen)

    if hasattr(player, 'frozen_active') and player.frozen_active:
        e.draw_frozen_filter(screen)

    score_surf = font.render(f"Score : {current_score}", True, (255, 255, 255))
    screen.blit(score_surf, (10, 10))

    player.inventory.draw_ui(screen, SCREEN_HEIGHT)
    player.draw_health_bar(screen)

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

    screen, clock, font, bg, bg_y = init_display()
    sounds = load_assets() # On charge les sons ici
    all_sprites, platforms, bullets_group, items_group, player = init_entities()

    running = True
    game_over = False
    total_scroll = 0
    damage_timer = 0
    last_hp = player.Hp

    while running:
        clock.tick(FPS)

        if player.Hp <= 0:
            game_over = True
            running = False
            continue

        running = handle_events(player)
        all_sprites.update()

        # Flash rouge si dégâts
        if player.Hp < last_hp:
            damage_timer = 10
        last_hp = player.Hp

        # Collisions avec passage des sons
        handle_collisions(player, items_group, sounds)

        # Scrolling et spawn
        from __main__ import update_scrolling_and_spawns # Sécurité import
        bg_y, total_scroll, SCORE = update_scrolling_and_spawns(
            player, bg, bg_y, total_scroll, SCORE, items_group, platforms, all_sprites
        )

        if player.rect.top > SCREEN_HEIGHT:
            game_over = True
            running = False

        draw_screen(screen, bg, bg_y, all_sprites, SCORE, player, font, damage_timer)

        if damage_timer > 0:
            damage_timer -= 1

    # save_scores(SCORE) # Active cette ligne si tu as la fonction
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()