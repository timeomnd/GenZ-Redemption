import pygame
import Puff as p
import inventory

SCREEN_WIDTH = 400  # Format vertical type Doodle Jump
SCREEN_HEIGHT = 600
PLAYER_COLOR = (0, 128, 255)
GRAVITY = 0.5


class Speed(pygame.sprite.Sprite):
    def __init__(self, platforms, all_sprites, bullets_group):
        super().__init__()

        try:
            self.jump_sound = pygame.mixer.Sound("../assets/sounds/jump.mp3")
            self.jump_sound.set_volume(0.4)  # Volume à 40%
        except Exception as e:
            print(f"Impossible de charger le son du saut : {e}")
            self.jump_sound = None

        # 1. Chargement de la Sprite Sheet unique
        try:
            sprite_sheet = pygame.image.load("../assets/speed/Speed.png").convert_alpha()
        except Exception as e:
            # Sécurité si l'image n'est pas trouvée
            print(f"Erreur lors de l'affichage du sprite : {e}")
            sprite_sheet = pygame.Surface((1000, 500))
            sprite_sheet.fill((0, 0, 255))

        self.inventory = inventory.Inventory()
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
        self.animation_speed = 0.09
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=(200, 500))

        # Variables de jeu
        self.rect = self.image.get_rect()
        # Position de départ au-dessus du sol
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        self.vel_y = 0
        self.platforms = platforms
        self.all_sprites = all_sprites
        self.bullets_group = bullets_group

        # --- STATISTIQUES ET EFFETS ---
        self.Hp = 100

        # Statistiques de base
        self.base_jump_power = -15
        self.base_move_speed = 7

        # Statistiques actuelles
        self.jump_power = self.base_jump_power
        self.move_speed = self.base_move_speed

        # Gestion des effets (chronomètres et états)
        self.monster_active = False
        self.monster_end_time = 0

        self.redbull_active = False
        self.redbull_end_time = 0

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.move_speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.move_speed

    def shoot(self):
        current_weapon = self.inventory.get_current_weapon()
        if not current_weapon:
            return

        puff = None
        # On tire la Puff qui correspond à l'arme équipée
        if current_weapon == "yellow":
            puff = p.PuffBanana(self.rect.centerx, self.rect.top)
        elif current_weapon == "blue":
            puff = p.PuffRaspberry(self.rect.centerx, self.rect.top)
        elif current_weapon == "black":
            puff = p.PuffBlackberry(self.rect.centerx, self.rect.top)
        elif current_weapon == "red":
            puff = p.PuffStrawberry(self.rect.centerx, self.rect.top)

        if puff:
            self.all_sprites.add(puff)
            self.bullets_group.add(puff)

    def update(self):
        current_time = pygame.time.get_ticks()

        # Annuler l'effet Monster après 8 secondes
        if self.monster_active and current_time > self.monster_end_time:
            self.monster_active = False
            self.set_speed(self.base_move_speed)  # Retour à la normale

        # Annuler l'effet Redbull après 8 secondes
        if self.redbull_active and current_time > self.redbull_end_time:
            self.redbull_active = False
            self.jump_power = self.base_jump_power  # Retour à la normale

        self.handle_keys()

        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        # Collision avec les plateformes (uniquement en tombant)
        if self.vel_y > 0:
            hits = pygame.sprite.spritecollide(self, self.platforms, False)
            if hits:
                lowest = hits[0]

                # On vérifie si les pieds du joueur sont bien au-dessus du haut de la plateforme
                if self.rect.bottom < lowest.rect.bottom + 10:
                    self.rect.bottom = lowest.rect.top
                    self.vel_y = self.jump_power  # Rebond automatique avec la puissance actuelle

                    if self.jump_sound:
                        self.jump_sound.play()

                    # GESTION DES TYPES
                    # On utilise hasattr par sécurité au cas où une plateforme (comme le sol de départ) n'aurait pas de type défini
                    if hasattr(lowest, 'type'):
                        if lowest.type == "fragile":
                            # La plateforme rouge est détruite après le rebond
                            lowest.kill()

                        if lowest.type == "fake":
                            self.vel_y = 0
                            lowest.kill()

                        if lowest.type == "bouncing":
                            self.vel_y = -20


        # Wrap-around (téléportation gauche/droite)
        if self.rect.left > SCREEN_WIDTH: self.rect.right = 0
        if self.rect.right < 0: self.rect.left = SCREEN_WIDTH

    def draw_health_bar(self, screen):
        # Paramètres de la barre
        bar_width = 100
        bar_height = 15
        x = 10
        y = 40

        # Calcule la largeur de la barre de vie en fonction des Hp actuels
        health_ratio = max(0, min(self.Hp, 100)) / 100.0
        current_bar_width = int(bar_width * health_ratio)

        # Couleurs
        bg_color = (255, 0, 0)  # Rouge pour le fond (vie perdue)
        hp_color = (0, 255, 0)  # Vert pour la vie actuelle

        # Dessiner le fond de la barre
        pygame.draw.rect(screen, bg_color, (x, y, bar_width, bar_height))
        # Dessiner la vie actuelle
        pygame.draw.rect(screen, hp_color, (x, y, current_bar_width, bar_height))
        # Dessiner un contour blanc
        pygame.draw.rect(screen, (255, 255, 255), (x, y, bar_width, bar_height), 2)

    def set_hp(self, hp):
        self.Hp += hp
        if self.Hp > 100:
            self.Hp = 100

    def set_jump(self, new_jump_power):
        self.jump_power = new_jump_power
        self.vel_y = self.jump_power

    def set_speed(self, new_move_speed):
        self.move_speed = new_move_speed

    def check_death_combo(self):
        if self.monster_active and self.redbull_active:
            self.Hp = 0  # Le joueur meurt

    def apply_monster(self):
        self.monster_active = True
        self.monster_end_time = pygame.time.get_ticks() + 8000
        self.set_speed(12)  # Augmente la vitesse horizontale
        self.check_death_combo()

    def apply_redbull(self):
        self.redbull_active = True
        self.redbull_end_time = pygame.time.get_ticks() + 8000
        self.set_jump(-25)  # Augmente le saut
        self.check_death_combo()