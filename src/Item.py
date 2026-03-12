import pygame


class ItemBar:
    def __init__(self, screen_width, screen_height):
        self.slot_size = 50  # Taille d'une case
        self.padding = 10  # Espace entre les cases

        # On calcule X pour centrer la barre en bas de l'écran
        self.y = screen_height - self.slot_size - 10

        # Liste de vos items (ajoutez ceux que vous voulez !)
        self.items = []
        self.load_item("Puff", "../assets/puff.png")
        self.load_item("Redbull", "../assets/redbull.png")
        self.load_item("Tacos", "../assets/tacos.png")

        # Calcul du point de départ X pour que ce soit centré
        total_width = len(self.items) * self.slot_size + (len(self.items) - 1) * self.padding
        self.start_x = (screen_width - total_width) // 2

        self.selected_index = 0  # L'item sélectionné par défaut (0 = le premier)

    def load_item(self, name, filepath):
        try:
            # Charge l'image et la redimensionne pour qu'elle rentre dans la case
            img = pygame.image.load(filepath).convert_alpha()
            img = pygame.transform.scale(img, (40, 40))
            self.items.append({"name": name, "image": img})
        except Exception as e:
            print(f"Erreur de chargement pour {name}: {e}")

    def draw(self, screen):
        for i, item in enumerate(self.items):
            x = self.start_x + i * (self.slot_size + self.padding)

            # Si c'est l'item sélectionné, on dessine une case dorée/jaune épaisse
            if i == self.selected_index:
                color = (255, 215, 0)  # Or
                thickness = 4
            else:
                color = (200, 200, 200)  # Gris clair
                thickness = 2

            # Dessiner le contour de la case
            pygame.draw.rect(screen, color, (x, self.y, self.slot_size, self.slot_size), thickness)

            # Dessiner l'image au centre de la case
            img = item["image"]
            img_rect = img.get_rect(center=(x + self.slot_size // 2, self.y + self.slot_size // 2))
            screen.blit(img, img_rect)

    def get_selected_item_name(self):
        # Renvoie le nom de l'item actuellement sélectionné
        if self.items:
            return self.items[self.selected_index]["name"]
        return None