from random import randint  # Импортируем функцию randint для генерации случайных целых чисел
from variables import *  # Импортируем все переменные из модуля variables
from game_sprite import GameSprite  # Импортируем класс GameSprite, от которого наследуется Enemy

class Enemy(GameSprite):  # Объявляем класс Enemy, который наследуется от GameSprite
    def update(self):  # Определяем метод update, который будет обновлять состояние врага в каждом кадре игры
        self.rect.y += self.speed  # Увеличиваем координату y врага на значение его скорости (движение вниз)
        if self.rect.y > win_height:  # Проверяем, вышел ли враг за нижнюю границу экрана
            self.rect.x = randint(80, win_width - 80)  # Если да, то задаем новую случайную координату x в пределах окна
            self.rect.y = 0  # И перемещаем врага вверх за пределы экрана (в начало экрана)