import pygame
import sys

# Game settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
GRAVITY = 0.5

# Player settings
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 60
PLAYER_COLOR = (0, 128, 255)
PLAYER_SPEED = 5
PLAYER_JUMP_POWER = 12

# Platform settings
PLATFORM_COLOR = (34, 177, 76)
PLATFORM_LIST = [
    (0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40),   # ground
    (100, 450, 150, 20),
    (350, 350, 200, 20),
    (600, 250, 180, 20)
]


class Player(pygame.sprite.Sprite):
    def __init__(self, platforms):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = SCREEN_HEIGHT - PLAYER_HEIGHT - 40
        self.vel_y = 0
        self.platforms = platforms
        self.on_ground = False

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED

    def jump(self):
        if self.on_ground:
            self.vel_y = -PLAYER_JUMP_POWER
            self.on_ground = False

    def update(self):
        self.handle_keys()
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        # Simple collision detection with platforms
        self.on_ground = False
        for platform in self.platforms:
            if self.rect.colliderect(platform.rect) and self.vel_y > 0:
                self.rect.bottom = platform.rect.top
                self.vel_y = 0
                self.on_ground = True

        # Prevent going offscreen
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.x > SCREEN_WIDTH - PLAYER_WIDTH:
            self.rect.x = SCREEN_WIDTH - PLAYER_WIDTH


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(PLATFORM_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Platformer Game")
    clock = pygame.time.Clock()

    # Create platforms
    platforms = pygame.sprite.Group()
    platform_objs = []
    for plat in PLATFORM_LIST:
        p = Platform(*plat)
        platforms.add(p)
        platform_objs.append(p)

    # Create player
    player = Player(platform_objs)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(platforms)

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()

        # Update
        player.update()

        # Draw
        screen.fill((135, 206, 235))  # sky blue
        all_sprites.draw(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()

