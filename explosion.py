# explosion.py
import pygame

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
        # Этот метод должен быть переопределен в классах-наследниках
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
        self.explosion_speed = 4  # Можно настроить скорость для врагов

    def load_explosion_images(self):
        for num in range(1, 6):  # 5 кадров для взрыва врага
            img = pygame.image.load(f"img/exp{num}.png")
            img = pygame.transform.scale(img, (100, 100))
            self.images.append(img)

class AsteroidExplosion(BaseExplosion):
    def __init__(self, x, y):
        super().__init__(x, y, scale=120)  # Больший размер для астероидов
        self.explosion_speed = 5  # Немного медленнее для астероидов

    def load_explosion_images(self):
        for num in range(1, 7):  # 6 кадров для взрыва астероида
            img = pygame.image.load(f"vzriv/vzriv{num}.png")
            img = pygame.transform.scale(img, (120, 120))
            self.images.append(img)