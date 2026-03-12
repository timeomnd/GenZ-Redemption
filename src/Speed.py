import pygame


class Speed(pygame.sprite.Sprite):
    def __init__(self, platforms, all_sprites, bullets_group):
        super().__init__()

        # 1. Chargement de la Sprite Sheet unique
        # Vérifie bien le chemin : "assets/speed_sprite_sheet_by_popgamer06_dg13zzz.jpg"
        try:
            sprite_sheet = pygame.image.load("../assets/speed/speed_12.png").convert_alpha()
        except:
            # Sécurité si l'image n'est pas trouvée
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
        self.vel_y = 0
        self.platforms = platforms
        self.all_sprites = all_sprites
        self.bullets_group = bullets_group
        self.facing_right = True

    def animate(self):
        # Logique de saut : frames 1 à 4 (indices 1 à 4)
        if self.vel_y < 0:
            start_jump = 0
            end_jump = 3
            self.frame_index += self.animation_speed
            if self.frame_index < start_jump or self.frame_index > end_jump:
                self.frame_index = start_jump
            new_image = self.frames[int(self.frame_index)]
        else:
            # Frame de base (immobile)
            new_image = self.frames[0]

        # Miroir selon la direction
        if not self.facing_right:
            self.image = pygame.transform.flip(new_image, True, False)
        else:
            self.image = new_image

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_q]:
            self.rect.x -= 7
            self.facing_right = False
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += 7
            self.facing_right = True

    def update(self):
        self.handle_keys()
        self.animate()

        # Gravité et mouvement
        self.vel_y += 0.5  # GRAVITY
        self.rect.y += self.vel_y

        # Collision plateformes
        if self.vel_y > 0:
            hits = pygame.sprite.spritecollide(self, self.platforms, False)
            if hits:
                if self.rect.bottom < hits[0].rect.bottom + 10:
                    self.rect.bottom = hits[0].rect.top
                    self.vel_y = -15

                # Wrap-around
        if self.rect.left > 400: self.rect.right = 0
        if self.rect.right < 0: self.rect.left = 400