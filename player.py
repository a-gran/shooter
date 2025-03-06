# Импортируем все переменные из файла variables
from variables import *
# Импортируем класс Bullet из файла bullet
from bullet import Bullet
# Импортируем библиотеку pygame
import pygame
# Импортируем базовый класс GameSprite
from game_sprite import GameSprite

# Создаем класс Player, наследующийся от GameSprite
class Player(GameSprite):
    # Инициализируем игрока с параметрами: изображение, координаты, размеры и скорость
    def __init__(self, image, x, y, size_x, size_y, speed):
        # Вызываем конструктор родительского класса
        super().__init__(image, x, y, size_x, size_y, speed)
        # Создаем группу для хранения пуль игрока
        self.bullets = pygame.sprite.Group()

    # Метод обновления состояния игрока
    def update(self):
        # Получаем состояние всех клавиш
        keys = pygame.key.get_pressed()
        # Если нажата клавиша влево и игрок не достиг левой границы
        if keys[pygame.K_LEFT] and self.rect.x > 5:
            # Двигаем игрока влево
            self.rect.x -= self.speed
        # Если нажата клавиша вправо и игрок не достиг правой границы
        if keys[pygame.K_RIGHT] and self.rect.x < win_width - 80:
            # Двигаем игрока вправо
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.y > 5:
            # Двигаем игрока влево
            self.rect.y -= self.speed
        # Если нажата клавиша вправо и игрок не достиг правой границы
        if keys[pygame.K_DOWN] and self.rect.y < win_height - 100:
            # Двигаем игрока вправо
            self.rect.y += self.speed

    # Метод для стрельбы
    def fire(self):
        # Создаем новую пулю по центру игрока
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        # Добавляем пулю в группу пуль
        self.bullets.add(bullet)
        # Возвращаем группу пуль
        return self.bullets

    # Метод для отрисовки игрока
    def reset(self, surface):
        # Отрисовываем изображение игрока на переданной поверхности
        surface.blit(self.image, (self.rect.x, self.rect.y))