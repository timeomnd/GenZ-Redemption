import pygame
import sys
import random
import Environment as e
import Speed as s
import Item
import Enemy

# --- CONFIGURATION ---
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 60
SCORE = 0


def init_display():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Gen Z Redemption")
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
    except:
        sounds["collect"] = None

    try:
        sounds["mob"] = pygame.mixer.Sound("../assets/sounds/mob_sound.mp3")
        sounds["mob"].set_volume(0.2)
    except:
        sounds["mob"] = None
    return sounds


def init_entities():
    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    bullets_group = pygame.sprite.Group()
    items_group = pygame.sprite.Group()
    enemies_group = pygame.sprite.Group()

    # Plateforme de départ (Solide)
    start_ground = e.StartPlatform(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40)
    all_sprites.add(start_ground)
    platforms.add(start_ground)

    # Génération initiale des plateformes
    spacing = SCREEN_HEIGHT // 5
    for i in range(6):
        p = e.generate_random_platform(random.randint(0, SCREEN_WIDTH - 60), i * spacing, 60, 15)
        all_sprites.add(p)
        platforms.add(p)

    player = s.Speed(platforms, all_sprites, bullets_group)
    all_sprites.add(player)

    return all_sprites, platforms, bullets_group, items_group, enemies_group, player


# --- LOGIQUE DE SPAWN ---

def spawn_consumable(platform, items_group, all_sprites):
    consumable_classes = [Item.Burger, Item.TastyCrousty, Item.Tacos, Item.TacosGratine,
                          Item.Poppers, Item.Monster, Item.Redbull, Item.Frozen]
    chosen_class = random.choice(consumable_classes)
    new_item = chosen_class(platform.rect.centerx, platform.rect.top - 20)
    items_group.add(new_item)
    all_sprites.add(new_item)


def spawn_puff(platform, items_group, all_sprites, player):
    puff_dict = {"red": Item.PuffStrawberryItem, "yellow": Item.PuffBananaItem,
                 "blue": Item.PuffBlueberryItem, "black": Item.PuffBlackBerryItem}
    map_weapons = [item.weapon_type for item in items_group if hasattr(item, 'weapon_type')]
    available_classes = [cls for name, cls in puff_dict.items()
                         if name not in map_weapons and not player.inventory.has_weapon(name)]
    if available_classes:
        chosen_class = random.choice(available_classes)
        new_item = chosen_class(platform.rect.centerx, platform.rect.top - 25)
        items_group.add(new_item)
        all_sprites.add(new_item)


def spawn_enemy(platform, enemies_group, all_sprites):
    enemy_classes = [Enemy.PinkEnemy, Enemy.BlueEnemy, Enemy.GreenEnemy]
    chosen_class = random.choice(enemy_classes)
    new_enemy = chosen_class(platform.rect.centerx, platform.rect.top - 30)
    enemies_group.add(new_enemy)
    all_sprites.add(new_enemy)


# --- COLLISIONS & SCROLLING ---

def handle_collisions(player, items_group, enemies_group, bullets_group, sounds):
    # Items
    hits_items = pygame.sprite.spritecollide(player, items_group, True)
    for item in hits_items:
        if sounds["collect"]: sounds["collect"].play()
        if hasattr(item, 'weapon_type'): player.inventory.add_weapon(item.weapon_type)
        if hasattr(item, 'type') and item.type == "consumable": item.play_abilitie(player)

    # Joueur / Ennemis
    hits_enemies = pygame.sprite.spritecollide(player, enemies_group, False)
    for enemy in hits_enemies:
        if hasattr(enemy, 'apply_effect'):
            enemy.apply_effect(player)
        else:
            player.set_hp(-20)
        enemy.kill()

    # Tirs / Ennemis
    pygame.sprite.groupcollide(enemies_group, bullets_group, True, True)


def update_scrolling_and_spawns(player, bg, bg_y, total_scroll, current_score, items_group, enemies_group, platforms,
                                all_sprites):
    if player.rect.top <= SCREEN_HEIGHT / 3:
        scroll_dist = abs(player.vel_y)
        total_scroll += scroll_dist
        current_score = max(current_score, int(total_scroll))
        player.rect.y += scroll_dist
        if bg: bg_y += scroll_dist * 0.1

        for sprite in list(items_group) + list(enemies_group):
            sprite.rect.y += scroll_dist
            if hasattr(sprite, 'base_y'): sprite.base_y += scroll_dist
            if sprite.rect.y > SCREEN_HEIGHT: sprite.kill()

        for plat in platforms:
            plat.rect.y += scroll_dist
            if plat.rect.top >= SCREEN_HEIGHT: plat.kill()

    while True:
        highest_y = min([p.rect.y for p in platforms]) if platforms else SCREEN_HEIGHT
        if highest_y <= 0: break

        new_y = highest_y - random.randint(70, 130)
        new_p = e.generate_random_platform(random.randint(0, SCREEN_WIDTH - 60), new_y, 60, 15)
        all_sprites.add(new_p)
        platforms.add(new_p)

        if new_p.type == "fake":
            alt_x = (new_p.rect.x + 150) % (SCREEN_WIDTH - 60)
            safe_p = e.NormalPlatform(alt_x, new_y, 60, 15)
            all_sprites.add(safe_p)
            platforms.add(safe_p)

        if new_p.type in ["normal", "bouncing"]:
            rand = random.randint(1, 100)
            if rand <= 5:
                spawn_puff(new_p, items_group, all_sprites, player)
            elif rand <= 10:
                spawn_consumable(new_p, items_group, all_sprites)
            elif rand <= 20:
                spawn_enemy(new_p, enemies_group, all_sprites)

    return bg_y, total_scroll, current_score


def draw_screen(screen, bg, bg_y, all_sprites, current_score, player, font, d_timer, h_timer):
    screen.fill((135, 206, 235))
    if bg: screen.blit(bg, (0, bg_y))
    all_sprites.draw(screen)

    if d_timer > 0: e.draw_damage_flash(screen)
    if h_timer > 0: e.draw_heal_flash(screen)
    if hasattr(player, 'frozen_active') and player.frozen_active: e.draw_frozen_filter(screen)

    score_surf = font.render(f"Score : {current_score}", True, (255, 255, 255))
    screen.blit(score_surf, (10, 10))
    player.inventory.draw_ui(screen, SCREEN_HEIGHT)
    player.draw_health_bar(screen)
    pygame.display.flip()


def save_scores(current_score):
    try:
        with open("../src/Score/last_score.txt", "w") as f:
            f.write(str(current_score))
        best = 0
        try:
            with open("../src/Score/best_score.txt", "r") as f:
                c = f.read().strip()
                if c: best = int(c)
        except:
            pass
        if current_score > best:
            with open("../src/Score/best_score.txt", "w") as f: f.write(str(current_score))
    except:
        pass


def main():
    global SCORE
    SCORE = 0
    screen, clock, font, bg, bg_y = init_display()
    sounds = load_assets()
    all_sprites, platforms, bullets, items, enemies, player = init_entities()

    running = True
    total_scroll = 0
    d_timer, h_timer = 0, 0
    last_hp = player.Hp
    mob_playing = False

    while running:
        clock.tick(FPS)
        if player.Hp <= 0 or player.rect.top > SCREEN_HEIGHT:
            running = False
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: player.shoot()
                if event.key == pygame.K_TAB: player.inventory.cycle_weapon()

        all_sprites.update()

        if player.Hp < last_hp:
            d_timer = 10
        elif player.Hp > last_hp:
            h_timer = 10
        last_hp = player.Hp

        handle_collisions(player, items, enemies, bullets, sounds)
        bg_y, total_scroll, SCORE = update_scrolling_and_spawns(player, bg, bg_y, total_scroll, SCORE, items, enemies,
                                                                platforms, all_sprites)

        if sounds["mob"]:
            mob_visible = any(0 < en.rect.y < SCREEN_HEIGHT for en in enemies)
            if mob_visible and not mob_playing:
                sounds["mob"].play(-1);
                mob_playing = True
            elif not mob_visible and mob_playing:
                sounds["mob"].stop();
                mob_playing = False

        draw_screen(screen, bg, bg_y, all_sprites, SCORE, player, font, d_timer, h_timer)
        if d_timer > 0: d_timer -= 1
        if h_timer > 0: h_timer -= 1

    if sounds["mob"]: sounds["mob"].stop()
    save_scores(SCORE)
    return


if __name__ == '__main__':
    main()