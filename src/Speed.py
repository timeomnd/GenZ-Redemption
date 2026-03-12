import pygame
import Puff
SCREEN_WIDTH = 400  # Format vertical type Doodle Jump
SCREEN_HEIGHT = 600
PLAYER_COLOR = (0, 128, 255)
GRAVITY = 0.5


class Speed(pygame.sprite.Sprite):
    def __init__(self, platforms, all_sprites, bullets_group):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect()
        # Position de départ au-dessus du sol
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        self.vel_y = 0
        self.platforms = platforms
        self.all_sprites = all_sprites
        self.bullets_group = bullets_group

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 7
        if keys[pygame.K_RIGHT]:
            self.rect.x += 7

    def shoot(self):
        bullet = Puff(self.rect.centerx, self.rect.top)
        self.all_sprites.add(bullet)
        self.bullets_group.add(bullet)

    def update(self):
        self.handle_keys()
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        # Collision avec les plateformes (uniquement en tombant)
        if self.vel_y > 0:
            hits = pygame.sprite.spritecollide(self, self.platforms, False)
            if hits:
                # On vérifie si les pieds du joueur sont bien au-dessus du haut de la plateforme
                lowest = hits[0]
                if self.rect.bottom < lowest.rect.bottom + 10:
                    self.rect.bottom = lowest.rect.top
                    self.vel_y = -15  # Rebond automatique

        # Wrap-around (téléportation gauche/droite)
        if self.rect.left > SCREEN_WIDTH: self.rect.right = 0
        if self.rect.right < 0: self.rect.left = SCREEN_WIDTH

