import pygame
import random

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600


# --- CLASSE DE BASE ---
class Platform(pygame.sprite.Sprite):

    def __init__(self, x, y, w, h, color, p_type, min_gap, max_gap):
        super().__init__()
        self.type = p_type
        self.min_gap = min_gap
        self.max_gap = max_gap

        self.image = pygame.Surface((w, h))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        # Par défaut, une plateforme ne fait rien de spécial
        pass


# --- SOUS-CLASSES DE PLATEFORMES ---
class NormalPlatform(Platform):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h, color=(34, 177, 76), p_type="normal", min_gap=60, max_gap=130)


class MovingPlatform(Platform):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h, color=(255, 127, 39), p_type="mouvante", min_gap=60, max_gap=130)
        self.speed_x = 3

    def update(self):
        # On surcharge la méthode update uniquement pour celle-ci
        self.rect.x += self.speed_x
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.speed_x *= -1


class FragilePlatform(Platform):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h, color=(237, 28, 36), p_type="fragile", min_gap=40, max_gap=80)


class FakePlatform(Platform):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h, color=(0, 0, 0), p_type="fake", min_gap=10, max_gap=40)


class BouncingPlatform(Platform):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h, color=(63, 72, 204), p_type="bouncing", min_gap=60, max_gap=130)


class StartPlatform(Platform):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h, color=(34, 177, 76), p_type="start", min_gap=0, max_gap=0)


# --- FONCTION DE GÉNÉRATION ALÉATOIRE ---
def generate_random_platform(x, y, w, h):

    # On associe directement la classe à sa probabilité
    choix_possibles = [
        {"classe": NormalPlatform, "proba": 60},
        {"classe": MovingPlatform, "proba": 20},
        {"classe": FragilePlatform, "proba": 12},
        {"classe": BouncingPlatform, "proba": 8},
        {"classe": FakePlatform, "proba": 8}
    ]

    liste_probas = []
    for c in choix_possibles:
        liste_probas.append(c["proba"])

    # On choisit le dictionnaire gagnant
    choix_gagnant = random.choices(choix_possibles, weights=liste_probas, k=1)[0]

    # On récupère la CLASSE (NormalPlatform, MovingPlatform, etc.)
    ClassePlateforme = choix_gagnant["classe"]

    # On crée et on retourne un objet de cette classe
    return ClassePlateforme(x, y, w, h)


def background():
    # Chargement du fond
    try:
        bg_image = pygame.image.load("../assets/arriere_plans/gratte-ciel.png").convert_alpha()
        original_width, original_height = bg_image.get_size()
        ratio = SCREEN_WIDTH / original_width
        new_height = int(original_height * ratio)
        bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, new_height))
        return bg_image
    except:
        return None