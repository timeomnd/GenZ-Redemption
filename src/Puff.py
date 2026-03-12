import pygame
BULLET_COLOR = (255, 215, 0)

class Puff(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((6, 12))
        self.image.fill(BULLET_COLOR)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -12

    def update(self):
        self.rect.y += self.speed
        # Supprime la balle si elle sort de l'écran
        if self.rect.bottom < 0:
            self.kill()
