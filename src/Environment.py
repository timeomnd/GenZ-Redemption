import pygame

# --- CONFIGURATION DU JEU ---
SCREEN_WIDTH = 400  # Format vertical type Doodle Jump
SCREEN_HEIGHT = 600
FPS = 60

# Couleurs
PLATFORM_COLOR = (34, 177, 76)
BULLET_COLOR = (255, 215, 0)  

SCORE = 0

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(PLATFORM_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

def background() :
    # Chargement du fond
        try:
            background = pygame.image.load("../assets/fond_test.jpg").convert()
            background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
            return background
        except:
            background = None
            return None
