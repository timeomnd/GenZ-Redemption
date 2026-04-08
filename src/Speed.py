import pygame
import Puff as p
import inventory

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
PLAYER_COLOR = (0, 128, 255)
GRAVITY = 0.5


class Speed(pygame.sprite.Sprite):
    def __init__(self, platforms, all_sprites, bullets_group):
        super().__init__()

        try:
            self.jump_sound = pygame.mixer.Sound("../assets/sounds/jump.mp3")
            self.jump_sound.set_volume(0.4)
        except Exception as e:
            print(f"Erreur son : {e}")
            self.jump_sound = None

        try:
            sprite_sheet = pygame.image.load("../assets/speed/Speed.png").convert_alpha()
        except Exception as e:
            print(f"Erreur sprite : {e}")
            sprite_sheet = pygame.Surface((1000, 500))
            sprite_sheet.fill((0, 0, 255))

        self.inventory = inventory.Inventory()
        self.frames = []

        cols = 4
        rows = 1
        width = sprite_sheet.get_width() // cols
        height = sprite_sheet.get_height() // rows

        for row in range(rows):
            for col in range(cols):
                rect = pygame.Rect(col * width, row * height, width, height)
                frame = sprite_sheet.subsurface(rect)
                frame = pygame.transform.scale(frame, (80, 100))
                self.frames.append(frame)

        self.frame_index = 0.0
        self.animation_speed = 0.09
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)

        self.vel_y = 0
        self.platforms = platforms
        self.all_sprites = all_sprites
        self.bullets_group = bullets_group

        self.Hp = 100
        self.base_jump_power = -15
        self.base_move_speed = 7
        self.jump_power = self.base_jump_power
        self.move_speed = self.base_move_speed

        self.monster_active = False
        self.monster_end_time = 0
        self.redbull_active = False
        self.redbull_end_time = 0
        self.tasty_active = False
        self.tasty_end_time = 0
        self.frozen_active = False
        self.frozen_end_time = 0

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        current_speed = self.move_speed if not self.frozen_active else self.base_move_speed / 2

        if keys[pygame.K_LEFT]:
            self.rect.x -= current_speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += current_speed

    def shoot(self):
        current_weapon = self.inventory.get_current_weapon()
        if not current_weapon: return

        puff = None
        if current_weapon == "yellow":
            puff = p.PuffBanana(self.rect.centerx, self.rect.top)
        elif current_weapon == "blue":
            puff = p.PuffRaspberry(self.rect.centerx, self.rect.top)
        elif current_weapon == "black":
            puff = p.PuffBlackberry(self.rect.centerx, self.rect.top)
        elif current_weapon == "red":
            puff = p.PuffStrawberry(self.rect.centerx, self.rect.top)

        if puff:
            self.all_sprites.add(puff)
            self.bullets_group.add(puff)

    def update(self):
        current_time = pygame.time.get_ticks()

        # Gestion des fins d'effets
        if self.monster_active and current_time > self.monster_end_time:
            self.monster_active = False
            self.move_speed = self.base_move_speed

        if self.redbull_active and current_time > self.redbull_end_time:
            self.redbull_active = False
            self.jump_power = self.base_jump_power

        if self.tasty_active and current_time > self.tasty_end_time:
            self.tasty_active = False
            self.jump_power = self.base_jump_power

        if self.frozen_active and current_time > self.frozen_end_time:
            self.frozen_active = False
            self.move_speed = self.base_move_speed

        self.handle_keys()

        # Animation
        current_anim_speed = self.animation_speed if not self.frozen_active else self.animation_speed / 2
        self.frame_index += current_anim_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

        # Physique
        current_gravity = GRAVITY if not self.frozen_active else GRAVITY / 3
        self.vel_y += current_gravity
        self.rect.y += self.vel_y

        # Collisions
        if self.vel_y > 0:
            hits = pygame.sprite.spritecollide(self, self.platforms, False)
            if hits:
                lowest = hits[0]
                if self.rect.bottom < lowest.rect.bottom + 10:
                    self.rect.bottom = lowest.rect.top
                    self.vel_y = self.jump_power
                    if self.jump_sound: self.jump_sound.play()

                    if hasattr(lowest, 'type'):
                        if lowest.type == "fragile":
                            if self.Hp > 10:
                                self.set_hp(-10)
                            lowest.kill()
                        elif lowest.type == "fake":
                            self.vel_y = 0
                            lowest.kill()
                        elif lowest.type == "bouncing":
                            self.vel_y = -20

        if self.rect.left > SCREEN_WIDTH: self.rect.right = 0
        if self.rect.right < 0: self.rect.left = SCREEN_WIDTH

    def draw_health_bar(self, screen):
        bar_width, bar_height = 100, 15
        x, y = 10, 40
        health_ratio = max(0, min(self.Hp, 100)) / 100.0
        current_bar_width = int(bar_width * health_ratio)

        pygame.draw.rect(screen, (255, 0, 0), (x, y, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (x, y, current_bar_width, bar_height))
        pygame.draw.rect(screen, (255, 255, 255), (x, y, bar_width, bar_height), 2)

    def set_hp(self, hp):
        self.Hp = min(100, self.Hp + hp)

    def set_jump(self, new_jump_power):
        self.jump_power = new_jump_power
        self.vel_y = self.jump_power

    def set_speed(self, new_move_speed):
        self.move_speed = new_move_speed

    def check_death_combo(self):
        if self.monster_active and self.redbull_active:
            self.Hp = 0

    def apply_monster(self):
        self.monster_active = True
        self.monster_end_time = pygame.time.get_ticks() + 5000
        self.move_speed = 12
        self.check_death_combo()

    def apply_redbull(self):
        self.redbull_active = True
        self.redbull_end_time = pygame.time.get_ticks() + 5000
        self.jump_power = -20
        self.check_death_combo()

    def apply_tasty_crousty(self):
        self.tasty_active = True
        self.tasty_end_time = pygame.time.get_ticks() + 5000
        self.jump_power = -8

    def apply_frozen(self):
        self.frozen_active = True
        self.frozen_end_time = pygame.time.get_ticks() + 5000