import pygame

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, image, x, y, size_x, size_y, speed):
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load(image), (size_x, size_y))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self, mw):
        mw.blit(self.image, (self.rect.x, self.rect.y))