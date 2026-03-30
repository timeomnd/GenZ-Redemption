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
            bg_image = pygame.image.load(os.path.join(ASSETS_PATH, 'gratte-ciel.png')).convert_alpha()

            original_width, original_height = bg_image.get_size()

            ratio = SCREEN_WIDTH / original_width
            new_height = int(original_height * ratio)

            bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, new_height))
            return bg_image
        except:
            background = None
            return None
