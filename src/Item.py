import pygame
import math


class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite_path, scalex, scaley):
        super().__init__()
        image = pygame.image.load(sprite_path)
        self.image = pygame.transform.scale(image, (scalex, scaley))

        self.rect = self.image.get_rect(centerx=x, bottom=y)

        self.base_y = float(self.rect.y)
        self.levitate_speed = 0.005
        self.levitate_range = 10
        self.time_offset = pygame.time.get_ticks()

    def update(self):
        current_time = pygame.time.get_ticks()
        offset_y = math.sin((current_time - self.time_offset) * self.levitate_speed) * self.levitate_range

        self.rect.y = int(self.base_y + offset_y)


class PuffStrawberryItem(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "../assets/puffs/puffRed.png", scalex=40, scaley=40)
        self.weapon_type = "red"


class PuffBlueberryItem(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "../assets/puffs/puffBlue.png", scalex=40, scaley=40)
        self.weapon_type = "blue"


class PuffBlackBerryItem(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "../assets/puffs/puffBlack.png", scalex=40, scaley=40)
        self.weapon_type = "black"


class PuffBananaItem(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "../assets/puffs/puffYellow.png", scalex=40, scaley=40)
        self.weapon_type = "yellow"


class Burger(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "../assets/items/burger.png", scalex=40, scaley=40)
        self.type = "consumable"

    def play_abilitie(self, player):
        player.set_hp(25)


class TastyCrousty(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "../assets/items/tasty_crousty.png", scalex=120, scaley=120)
        self.type = "consumable"

    def play_abilitie(self, player):
        player.apply_tasty_crousty()


class Tacos(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "../assets/items/tacos.png", scalex=50, scaley=50)
        self.type = "consumable"

    def play_abilitie(self, player):
        player.set_hp(50)


class TacosGratine(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "../assets/items/tacos_gratine.png", scalex=50, scaley=50)
        self.type = "consumable"

    def play_abilitie(self, player):
        player.set_hp(100)


class Poppers(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "../assets/items/poppers.png", scalex=120, scaley=60)
        self.type = "consumable"

    def play_abilitie(self, player):
        pass

class Monster(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "../assets/items/monster.png", scalex=40, scaley=40)
        self.type = "consumable"

    def play_abilitie(self, player):
        player.apply_monster()

class Redbull(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "../assets/items/redbull.png", scalex=40, scaley=40)
        self.type = "consumable"

    def play_abilitie(self, player):
        player.apply_redbull()

class Frozen(Item):
    def __init__(self, x, y):
        super().__init__(x, y, "../assets/items/frozen.png", scalex=50, scaley=50)
        self.type = "consumable"

    def play_abilitie(self, player):
        player.apply_frozen()