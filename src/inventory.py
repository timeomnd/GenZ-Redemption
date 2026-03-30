import pygame
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_PATH = os.path.join(BASE_DIR, "..", "assets")
class Inventory:
    def __init__(self):
        self.weapons = []
        self.current_index = -1 # pas d'amrme

        self.icons = {}
        icon_files = {
            "red": "puffRed.png",
            "blue": "puffBlue.png",
            "black": "puffBlack.png",
            "yellow": "puffYellow.png"
        }

        try:

            self.collect_sound = pygame.mixer.Sound("../assets/sound/item_collect_sound_effect.mp3")
            self.collect_sound.set_volume(0.4)
        except:
            self.collect_sound = None

        for weapon_name, filename in icon_files.items():
            try:
                path = os.path.join(ASSETS_PATH, filename)
                img = pygame.image.load(path).convert_alpha()
                img = pygame.transform.scale(img, (30, 30))
                self.icons[weapon_name] = img

            except:
                # Sécurité : Si l'image manque, on met un carré rose à la place
                fallback = pygame.Surface((30, 30))
                fallback.fill((255, 0, 255))
                self.icons[weapon_name] = fallback

    def add_weapon(self, weapon_type):
        if weapon_type not in self.weapons:
            self.weapons.append(weapon_type)
            if self.current_index == -1:
                self.current_index = 0
            print(f"[{weapon_type}] ajouté ! Inventaire : {self.weapons}")
            if self.collect_sound:
                self.collect_sound.play()

    def cycle_weapon(self):
        if not self.weapons:
            return

        self.current_index = (self.current_index + 1) % len(self.weapons)

    def get_current_weapon(self):
        if self.current_index == -1 or not self.weapons:
            return None
        return self.weapons[self.current_index]

    def has_weapon(self, weapon_type):
        return weapon_type in self.weapons

    def draw_ui(self, screen, screen_height):
        if not self.weapons:
            return

        SLOT_SIZE = 40
        PADDING = 10
        START_X = 10
        START_Y = screen_height - SLOT_SIZE - 10

        current_weapon = self.get_current_weapon()

        for i, weapon in enumerate(self.weapons):
            x = START_X + i * (SLOT_SIZE + PADDING)
            y = START_Y

            rect = pygame.Rect(x, y, SLOT_SIZE, SLOT_SIZE)
            pygame.draw.rect(screen, (30, 30, 30), rect)

            if weapon in self.icons:
                screen.blit(self.icons[weapon], (x + 5, y + 5))

            if weapon == current_weapon:
                pygame.draw.rect(screen, (255, 215, 0), rect, 3)  # Doré
            else:
                pygame.draw.rect(screen, (150, 150, 150), rect, 1)  # Gris