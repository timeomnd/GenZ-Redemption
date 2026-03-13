import pygame
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_PATH = os.path.join(BASE_DIR, "..", "assets")

class Puff(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite_path, speed, damage, cols, rows, scalex, scaley):
        super().__init__()
        try :
            sprite_sheet = pygame.image.load(sprite_path)
            self.frames = []
            width = sprite_sheet.get_width() // cols
            height = sprite_sheet.get_height() // rows
            for row in range(rows) :
                for col in range(cols):
                    #découper le sprite en plusieurs frames et prendre le frame en fonction de i puis l'ajouter à la liste de frames
                    x_pos = col * width
                    y_pos = row * height
                    frame = sprite_sheet.subsurface((x_pos, y_pos, width, height))
                    frame = pygame.transform.scale(frame, (scalex, scaley))
                    self.frames.append(frame)
        except :
            self.frames = [pygame.Surface((60, 60))]

        #Début de l'animation à frames[0]
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(centerx=x, bottom=y)

        # Variables de mouvement
        self.velocity = float(speed)  # Vitesse initiale (ex: -12)
        self.friction = 0.90  # Facteur de ralentissement (plus c'est bas, plus vite ça s'arrête)

        # Variables de temps
        self.damage = damage
        self.spawn_time = pygame.time.get_ticks()
        self.duration = 1000  # 3 secondes en millisecondes

        self.animation_speed = 0.08
        self.frame_index = 0.0

    def update(self):
        #la vitesse décroit grâce à la friction qui est < 1
        self.velocity *= self.friction
        self.rect.y += self.velocity

        self.frame_index += self.animation_speed

        # On bloque l'index sur la dernière image si on dépasse
        if self.frame_index >= len(self.frames):
            self.frame_index = len(self.frames) - 1
        self.current_frame = int(self.frame_index) % len(self.frames)
        self.image = self.frames[self.current_frame]

        # 3. Suppression après 3 secondes
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_time > self.duration:
            self.kill()

#blue Puff
class PuffRaspberry(Puff):
    def __init__(self, x, y):
        super().__init__(x,y,os.path.join(ASSETS_PATH, "ice_sparkles.png"),-12, 10, 5, 1, 90, 90)
class PuffStrawberry(Puff):
    def __init__(self, x, y):
        super().__init__(x,y,os.path.join(ASSETS_PATH, "fireball.png"), -12, 10, 2, 2, 90, 90)
class PuffBlackberry(Puff):
    def __init__(self, x, y):
        super().__init__(x,y,os.path.join(ASSETS_PATH, "explosion.png"),-12,10,6,1, 90, 90)
class PuffBanana(Puff):
    def __init__(self, x, y):
        super().__init__(x,y,os.path.join(ASSETS_PATH, "smoke.png"),-12,10,7,1, 125, 150)

#red Puff
#black puff
#yellow puff