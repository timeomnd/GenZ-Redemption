import pygame
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_PATH = os.path.join(BASE_DIR, "..", "assets")


class Puff(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite_path, damage, cols, rows, scalex, scaley,
                 speed=-12, friction=0.90, rotation=0, is_tick_damage=True, duration=1000):
        super().__init__()

        self.setup_images(sprite_path, cols, rows, scalex, scaley, rotation)
        self.setup_physics(speed, friction)
        self.setup_stats(damage, is_tick_damage, duration)
        self.setup_animation(0.08)

        self.rect = self.image.get_rect(centerx=x, bottom=y)

    def setup_images(self, path, cols, rows, sx, sy, rotation):
        self.frames = []
        try:
            sheet = pygame.image.load(path).convert_alpha()
            width, height = sheet.get_width() // cols, sheet.get_height() // rows
            for row in range(rows):
                for col in range(cols):
                    frame = sheet.subsurface((col * width, row * height, width, height))
                    if rotation != 0:
                        frame = pygame.transform.rotate(frame, rotation)
                    self.frames.append(pygame.transform.scale(frame, (sx, sy)))
        except Exception as e:
            print(f"Erreur images : {e}")
            self.frames = [pygame.Surface((sx, sy))]

        self.current_frame = 0
        self.image = self.frames[0]

    def setup_physics(self, speed, friction):
        self.velocity = float(speed)
        self.friction = friction

    def setup_stats(self, damage, is_tick_damage, duration):
        self.damage = damage
        self.is_tick_damage = is_tick_damage
        self.spawn_time = pygame.time.get_ticks()
        self.duration = duration

    def setup_animation(self, speed):
        self.frame_index = 0.0
        self.animation_speed = speed

    def update(self):
        self.velocity *= self.friction
        self.rect.y += self.velocity

        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = len(self.frames) - 1

        self.image = self.frames[int(self.frame_index)]

        if pygame.time.get_ticks() - self.spawn_time > self.duration:
            self.kill()
#blue Puff
class PuffRaspberry(Puff):
    def __init__(self, x, y):
        super().__init__(x, y, os.path.join(ASSETS_PATH, "snowball.png"),damage=10, cols=3, rows=2, scalex=90, scaley=90, friction=0.98, rotation=-90)
class PuffStrawberry(Puff):
    def __init__(self, x, y):
        super().__init__(x, y, os.path.join(ASSETS_PATH, "fireball.png"),damage=15, cols=2, rows=2, scalex=90, scaley=90,friction=1.0, rotation=-90, is_tick_damage=False)
class PuffBlackberry(Puff):
    def __init__(self, x, y):
        super().__init__(x, y, os.path.join(ASSETS_PATH, "explosion.png"),damage=20, cols=6, rows=1, scalex=90, scaley=90,is_tick_damage=False)
class PuffBanana(Puff):
    def __init__(self, x, y):
        super().__init__(x, y, os.path.join(ASSETS_PATH, "smoke.png"),damage=10, cols=7, rows=1, scalex=125, scaley=150)

#red Puff
#black puff
#yellow puff