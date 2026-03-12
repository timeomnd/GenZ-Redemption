import pygame
import sys
import random

# --- CONFIGURATION DU JEU ---
SCREEN_WIDTH = 400  # Format vertical type Doodle Jump
SCREEN_HEIGHT = 600
FPS = 60
GRAVITY = 0.5

# Couleurs
PLAYER_COLOR = (0, 128, 255)
PLATFORM_COLOR = (34, 177, 76)
BULLET_COLOR = (255, 215, 0)  

SCORE = 0

# --- CLASSES ---

class Bullet(pygame.sprite.Sprite):
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

class Player(pygame.sprite.Sprite):
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
        bullet = Bullet(self.rect.centerx, self.rect.top)
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
        

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(PLATFORM_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# --- FONCTION PRINCIPALE ---

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Doodle Shoot Platformer")
    clock = pygame.time.Clock()

    # Chargement du fond
    try:
        background = pygame.image.load('assets/fond_tik_tok.jpg').convert()
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    except:
        background = None

    # Groupes de sprites
    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    bullets_group = pygame.sprite.Group()

    # 1. Création du SOL de départ (largeur totale pour ne pas tomber)
    start_ground = Platform(0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40)
    all_sprites.add(start_ground)
    platforms.add(start_ground)

    # 2. Création des plateformes initiales au-dessus
    for i in range(5):
        p = Platform(random.randint(0, SCREEN_WIDTH - 60), i * 120, 60, 15)
        all_sprites.add(p)
        platforms.add(p)

    # 3. Création du joueur
    player = Player(platforms, all_sprites, bullets_group)
    all_sprites.add(player)

    running = True
    while running:
        clock.tick(FPS)

        # Événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()

        # Mise à jour
        all_sprites.update()

        # LOGIQUE DE SCROLLING (Caméra qui monte)
        if player.rect.top <= SCREEN_HEIGHT / 3:
            # On descend tout le monde selon la vitesse du joueur
            scroll_dist = abs(player.vel_y)
            player.rect.y += scroll_dist
            for plat in platforms:
                plat.rect.y += scroll_dist
                # Recyclage des plateformes qui sortent par le bas
                if plat.rect.top >= SCREEN_HEIGHT:
                    plat.kill()
                    new_p = Platform(random.randint(0, SCREEN_WIDTH - 60), 
                                     random.randint(-50, 0), 60, 15)
                    all_sprites.add(new_p)
                    platforms.add(new_p)

        # Condition de défaite (Game Over)
        if player.rect.top > SCREEN_HEIGHT:
            print("Game Over!")
            print(SCORE)
            running = False

        # Dessin
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill((135, 206, 235))

        all_sprites.draw(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main() 