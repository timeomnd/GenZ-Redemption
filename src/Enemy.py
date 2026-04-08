import pygame
import os
import math
import random

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, color_name, scale_w, scale_h, hp, damage):
        super().__init__()

        self.frames = []
        base_path = f"../assets/Enemy/{color_name}"

        # Chargement des 8 frames (de 1 à 8)
        for i in range(1, 9):
            img_path = f"{base_path}/{color_name}{i}.png"
            try:
                original_image = pygame.image.load(img_path).convert_alpha()
                self.frames.append(pygame.transform.scale(original_image, (scale_w, scale_h)))
            except Exception as error:
                print(f"Image introuvable : {img_path} - {error}")
                # Carré rouge de secours
                surf = pygame.Surface((scale_w, scale_h))
                surf.fill((255, 0, 0))
                self.frames.append(surf)

        self.current_frame = 0
        self.animation_speed = 0.15  # Vitesse de l'animation

        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(midbottom=(x, y))

        # Mémorise la vraie position verticale (hors lévitation)
        self.base_y = float(self.rect.y)

        # Vitesse sur l'axe X (choisit aléatoirement de partir à gauche ou à droite)
        self.speed_x = random.choice([-1.5, 1.5])

        # Paramètres de lévitation
        self.levitation_amplitude = 8  # Hauteur du mouvement (en pixels)
        self.levitation_speed = 0.004  # Vitesse du mouvement de haut en bas
        # Un décalage aléatoire pour éviter que tous les mobs montent et descendent en même temps
        self.levitation_offset = random.uniform(0, 2 * math.pi)

        self.hp = hp
        self.damage = damage  # Dégâts de base infligés au joueur

    def animate(self):
        self.current_frame += self.animation_speed
        if self.current_frame >= len(self.frames):
            self.current_frame = 0
        self.image = self.frames[int(self.current_frame)]

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp <= 0:
            self.kill()

    def update(self):
        self.animate()

        self.rect.x += self.speed_x

        # Rebondir sur les bords de l'écran (0 et 400 = SCREEN_WIDTH)
        if self.rect.left <= 0:
            self.rect.left = 0
            self.speed_x *= -1  # Inverse la direction (repart à droite)
        elif self.rect.right >= 400:
            self.rect.right = 400
            self.speed_x *= -1  # Inverse la direction (repart à gauche)

        current_time = pygame.time.get_ticks()

        offset_y = math.sin(current_time * self.levitation_speed + self.levitation_offset) * self.levitation_amplitude

        # On applique le décalage à la hauteur de base
        self.rect.y = int(self.base_y + offset_y)

    # Méthode à redéfinir dans chaque sous-classe pour appliquer les effets
    def apply_effect(self, player):
        pass


class PinkEnemy(Enemy):
    def __init__(self, x, y):
        # Pink fait plus de dégâts mais pas d'effet
        super().__init__(x, y, "Pink", scale_w=64, scale_h=64, hp=20, damage=20)

    def apply_effect(self, player):
        player.take_damage(self.damage)


class BlueEnemy(Enemy):
    def __init__(self, x, y):
        # Blue fait un peu de dégâts
        super().__init__(x, y, "Blue", scale_w=64, scale_h=64, hp=15, damage=10)

    def apply_effect(self, player):
        player.take_damage(self.damage)
        # On suppose que le joueur a une méthode pour ça (voir plus bas)
        player.apply_slow_effect(duration=5000) # 5000 ms


class GreenEnemy(Enemy):
    def __init__(self, x, y):
        # Green fait peu de dégâts à l'impact
        super().__init__(x, y, "Green", scale_w=64, scale_h=64, hp=15, damage=5)

    def apply_effect(self, player):
        player.take_damage(self.damage)
        # Empoisonne le joueur
        player.apply_poison_effect(duration=5000, tick_damage=2) # 5 secondes, 2 hp par seconde