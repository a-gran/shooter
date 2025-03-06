import math
from random import randint
from variables import win_width, win_height
from game_sprite import GameSprite
import pygame

class Asteroid(GameSprite):
    def __init__(self, image, x, y, size_x, size_y, speed):
        super().__init__(image, x, y, size_x, size_y, speed)
        self.base_speed = speed  # Используем переданную скорость вместо случайной
        self.reset_movement()
        
        self.original_image = self.image
        self.rotation_angle = 0
        
    def reset_movement(self):
        angle_degrees = randint(-70, 70)
        angle_radians = math.radians(angle_degrees)
        
        # Убираем нормализацию по сумме компонентов, используем прямой расчет векторов
        self.speed_x = self.base_speed * math.sin(angle_radians)
        self.speed_y = self.base_speed * math.cos(angle_radians)

    def update(self):
        # Обновляем позицию
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        # Вращение астероида
        self.rotation_angle = (self.rotation_angle + 1) % 360
        self.image = pygame.transform.rotate(self.original_image, self.rotation_angle)
        
        # Проверка выхода за границы
        if self.rect.y > win_height or self.rect.x < -50 or self.rect.x > win_width:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            self.reset_movement()