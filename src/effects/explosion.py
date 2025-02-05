import pygame
from src.utils.asset_loader import AssetLoader

class BaseExplosion(pygame.sprite.Sprite):
    def __init__(self, x, y, scale=100):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.load_explosion_images()
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0
        self.explosion_speed = 4

    def load_explosion_images(self):
        pass

    def update(self):
        self.counter += 1
        if self.counter >= self.explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        if self.index >= len(self.images) - 1 and self.counter >= self.explosion_speed:
            self.kill()

class EnemyExplosion(BaseExplosion):
    def __init__(self, x, y):
        super().__init__(x, y, scale=100)
        self.explosion_speed = 4

    def load_explosion_images(self):
        frames = AssetLoader.load_explosion_frames('enemy')
        self.images = [pygame.transform.scale(frame, (100, 100)) for frame in frames]

class AsteroidExplosion(BaseExplosion):
    def __init__(self, x, y):
        super().__init__(x, y, scale=120)
        self.explosion_speed = 5

    def load_explosion_images(self):
        frames = AssetLoader.load_explosion_frames('asteroid')
        self.images = [pygame.transform.scale(frame, (120, 120)) for frame in frames]