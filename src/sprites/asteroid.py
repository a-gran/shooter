import pygame
import math
from random import randint
from src.config.variables import win_width, win_height
from src.sprites.game_sprite import GameSprite


class Asteroid(GameSprite):
    def __init__(self, image, x, y, size_x, size_y, speed):
        super().__init__(image, x, y, size_x, size_y, speed)
        self.base_speed = randint(2, 10)
        angle_degrees = randint(-70, 70)
        angle_radians = math.radians(angle_degrees)
        total = abs(math.sin(angle_radians)) + abs(math.cos(angle_radians))
        
        if total != 0:
            self.speed_x = (self.base_speed * math.sin(angle_radians)) / total
            self.speed_y = (self.base_speed * math.cos(angle_radians)) / total
        else:
            self.speed_x = 0
            self.speed_y = self.base_speed
            
        self.original_image = self.image
        self.rotation_angle = 0

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        self.rotation_angle = (self.rotation_angle + 1) % 360
        self.image = pygame.transform.rotate(self.original_image, self.rotation_angle)
        
        if self.rect.y > win_height or self.rect.x < -50 or self.rect.x > win_width:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            
            angle_degrees = randint(-45, 45)
            angle_radians = math.radians(angle_degrees)
            total = abs(math.sin(angle_radians)) + abs(math.cos(angle_radians))
            
            if total != 0:
                self.speed_x = (self.base_speed * math.sin(angle_radians)) / total
                self.speed_y = (self.base_speed * math.cos(angle_radians)) / total