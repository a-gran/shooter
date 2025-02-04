import pygame
from src.config.variables import img_bullet, win_width
from src.sprites.bullet import Bullet
from src.sprites.game_sprite import GameSprite

class Player(GameSprite):
    def __init__(self, image, x, y, size_x, size_y, speed):
        super().__init__(image, x, y, size_x, size_y, speed)
        self.bullets = pygame.sprite.Group()

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        self.bullets.add(bullet)
        return self.bullets

    def reset(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))