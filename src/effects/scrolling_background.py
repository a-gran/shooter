import pygame
from src.config.variables import win_width, win_height

class ScrollBackground:
    def __init__(self, image_path):
        # Загружаем изображение фона
        self.image = pygame.image.load(image_path)
        # Создаем два экземпляра изображения для плавного скроллинга
        self.bg_1 = pygame.transform.scale(self.image, (win_width, win_height))
        self.bg_2 = pygame.transform.scale(self.image, (win_width, win_height))
        # Начальные позиции для обоих изображений
        self.bg1_y = 0
        self.bg2_y = -win_height
        self.scroll_speed = 2

    def update(self):
        # Двигаем оба изображения вниз
        self.bg1_y += self.scroll_speed
        self.bg2_y += self.scroll_speed

        # Если первое изображение полностью ушло вниз
        if self.bg1_y >= win_height:
            self.bg1_y = self.bg2_y - win_height

        # Если второе изображение полностью ушло вниз
        if self.bg2_y >= win_height:
            self.bg2_y = self.bg1_y - win_height

    def draw(self, surface):
        # Отрисовываем оба изображения
        surface.blit(self.bg_1, (0, self.bg1_y))
        surface.blit(self.bg_2, (0, self.bg2_y))