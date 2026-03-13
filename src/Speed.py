import pygame
import Puff as p
import random
import os
SCREEN_WIDTH = 400  # Format vertical type Doodle Jump
SCREEN_HEIGHT = 600
PLAYER_COLOR = (0, 128, 255)
GRAVITY = 0.5
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SPEED_PATH = os.path.join(BASE_DIR, "..", "assets", "speed")

class Speed(pygame.sprite.Sprite):
    def __init__(self, platforms, all_sprites, bullets_group):
        super().__init__()

        # 1. Chargement de la Sprite Sheet unique
        # Vérifie bien le chemin : "assets/speed_sprite_sheet_by_popgamer06_dg13zzz.jpg"
        try:
            full_path = os.path.join(SPEED_PATH, "Speed_12.png")
            print(f"Recherche de l'image ici : {full_path}")
            sprite_sheet = pygame.image.load(os.path.join(full_path)).convert_alpha()
        except Exception as e:
            # Sécurité si l'image n'est pas trouvée
            print(f"Erreur lors de l'affichage du sprite : {e}")
            sprite_sheet = pygame.Surface((1000, 500))
            sprite_sheet.fill((0, 0, 255))

        self.frames = []

        # 2. Découpage (Logique subsurface)
        # On définit la taille d'une seule case (à ajuster selon ton image)
        # Si ton image a par exemple 10 colonnes et 3 lignes :
        cols = 4
        rows = 1
        width = sprite_sheet.get_width() // cols
        height = sprite_sheet.get_height() // rows

        for row in range(rows):
            for col in range(cols):
                # On découpe la frame précise
                rect = pygame.Rect(col * width, row * height, width, height)
                frame = sprite_sheet.subsurface(rect)

                # On redimensionne pour le jeu
                frame = pygame.transform.scale(frame, (80, 100))
                self.frames.append(frame)

        # 3. Initialisation de l'image
        self.frame_index = 0.0
        self.animation_speed = 0.1
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=(200, 500))

        # Variables de jeu
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
        rand = random.randint(0,3)
        if rand == 0:
            puff = p.PuffBanana(self.rect.centerx, self.rect.top)
        if rand == 1:
            puff = p.PuffRaspberry(self.rect.centerx, self.rect.bottom)
        if rand == 2:
            puff = p.PuffBlackberry(self.rect.centerx, self.rect.bottom)
        if rand == 3:
            puff = p.PuffStrawberry(self.rect.centerx, self.rect.bottom)
        self.all_sprites.add(puff)
        self.bullets_group.add(puff)

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

