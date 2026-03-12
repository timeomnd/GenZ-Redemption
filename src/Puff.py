import pygame

class Puff(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, damage):
        super().__init__()
        sprite_sheet = pygame.image.load("../assets/smoke.png")
        self.frames = []
        width = sprite_sheet.get_width() // 7
        height = sprite_sheet.get_height()
        for i in range(7) :
            #découper le sprite en plusieurs frames et prendre le frame en fonction de i puis l'ajouter à la liste de frames
            frame = sprite_sheet.subsurface((i*width, 0, width, height))
            self.frames.append(frame)

            #Début de l'animation à frames[0]
            self.current_frame = 0
            self.image = self.frames[self.current_frame]
            self.rect = self.image.get_rect(centerx=x, bottom=y)

            self.speed = speed
            self.damage = damage
            self.animation_speed = 0.2
            self.frame_index = 0.0

    def update(self):
        self.rect.y += self.speed

        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.current_frame = int(self.frame_index)
            self.image = self.frames[self.current_frame]

        if self.rect.bottom < 0:
            self.kill()
