from sys import implementation

import pygame
import math
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_PATH = os.path.join(BASE_DIR, "..", "assets")


class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite_path, scalex, scaley):
        super().__init__()
        try:
            image = pygame.image.load(sprite_path)
            self.image = pygame.transform.scale(image, (scalex, scaley))
        except:
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
        super().__init__(x, y, os.path.join(ASSETS_PATH, "puffRed.png"), scalex=40, scaley=40)
        self.weapon_type = "red"


class PuffBlueberryItem(Item):
    def __init__(self, x, y):
        super().__init__(x, y, os.path.join(ASSETS_PATH, "puffBlue.png"), scalex=40, scaley=40)
        self.weapon_type = "blue"


class PuffBlackBerryItem(Item):
    def __init__(self, x, y):
        super().__init__(x, y, os.path.join(ASSETS_PATH, "puffBlack.png"), scalex=40, scaley=40)
        self.weapon_type = "black"


class PuffBananaItem(Item):
    def __init__(self, x, y):
        super().__init__(x, y, os.path.join(ASSETS_PATH, "puffYellow.png"), scalex=40, scaley=40)
        self.weapon_type = "yellow"


class Burger(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "../assets/burger.png", scalex=40, scaley=40)
        self.type = "consumable"

    def play_abilitie(self, player):
        player.set_hp(25)


class TastyCrousty(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "../assets/tasty_crousty.png", scalex=120, scaley=120)
        self.type = "consumable"

    def play_abilitie(self, player):
        pass


class Tacos(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "../assets/tacos.png", scalex=50, scaley=50)
        self.type = "consumable"

    def play_abilitie(self, player):
        player.set_hp(50)


class TacosGratine(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "../assets/tacos_gratine.png", scalex=50, scaley=50)
        self.type = "consumable"

    def play_abilitie(self, player):
        player.set_hp(100)


class Poppers(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "../assets/poppers.png", scalex=120, scaley=60)
        self.type = "consumable"

    def play_abilitie(self, player):
        pass

class Monster(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "../assets/monster.png", scalex=40, scaley=40)
        self.type = "consumable"

    def play_abilitie(self, player):
        player.apply_monster()

class Redbull(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "../assets/redbull.png", scalex=40, scaley=40)
        self.type = "consumable"

    def play_abilitie(self, player):
        player.apply_redbull()

class Frozen(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "../assets/frozen.png", scalex=50, scaley=50)
        self.type = "consumable"

    def play_abilitie(self, player):
        pass