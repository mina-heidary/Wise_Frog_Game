import pygame

class SettingIcon:
    def __init__(self, name, img_path, size, offset_y):
        self.name = name
        self.image = pygame.image.load(img_path).convert_alpha()
        self.image = pygame.transform.smoothscale(self.image, size)
        self.rect = self.image.get_rect()
        self.offset_y = offset_y
        self.visible = False

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

    def update(self, rect):
        self.rect.midtop = (rect.centerx, rect.bottom + self.offset_y)

    def draw(self, window):
        if self.visible:
            window.blit(self.image, self.rect)

    def clicked(self, mouse_pos):
        return self.visible and self.rect.collidepoint(mouse_pos)
    
    def create_setting_icons():
        icons = []
        icons.append(SettingIcon("volume", "data/menu/botton/icon/volume.png", (30, 30), 100))
        icons.append(SettingIcon("shop", "data/menu/botton/icon/shop.png", (32, 32), 10))
        icons.append(SettingIcon("bag", "data/menu/botton/icon/bag.png", (50, 50), 50))
        return icons
    
