from sys import implementation

import pygame
import math
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_PATH = os.path.join(BASE_DIR, "..", "assets")
class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite_path, scalex, scaley, weapon_type):
        super().__init__()
        try :
            image = pygame.image.load(sprite_path)
            self.image = pygame.transform.scale(image, (scalex, scaley))
        except :
            self.image = pygame.Surface((scalex, scaley))
            self.image.fill((0, 255, 0))

        self.rect = self.image.get_rect(centerx=x, bottom=y)

        self.base_y = float(self.rect.y)
        self.levitate_speed = 0.005
        self.levitate_range = 10
        self.weapon_type = weapon_type
        self.time_offset = pygame.time.get_ticks()

    def update(self):
        current_time = pygame.time.get_ticks()
        offset_y = math.sin((current_time - self.time_offset) * self.levitate_speed) * self.levitate_range

        self.rect.y = int(self.base_y + offset_y)


class PuffStrawberryItem(Item):
    def __init__(self, x, y):
        super().__init__(x, y, os.path.join(ASSETS_PATH, "puffRed.png"), scalex=40, scaley=40, weapon_type = "red")

class PuffBlueberryItem(Item):
    def __init__(self, x, y):
        super().__init__(x, y, os.path.join(ASSETS_PATH, "puffBlue.png"), scalex=40, scaley=40, weapon_type = "blue")
class PuffBlackBerryItem(Item):
    def __init__(self, x, y):
        super().__init__(x, y, os.path.join(ASSETS_PATH, "puffBlack.png"), scalex=40, scaley=40, weapon_type = "black")
        
class PuffBananaItem(Item):
    def __init__(self, x, y):
        super().__init__(x, y, os.path.join(ASSETS_PATH, "puffYellow.png"), scalex=40, scaley=40, weapon_type = "yellow")
