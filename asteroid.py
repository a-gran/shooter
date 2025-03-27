import math                                     # Импорт модуля math для тригонометрических функций и преобразований
from random import randint                      # Импорт функции randint для генерации случайных целых чисел
from variables import win_width, win_height     # Импорт размеров окна из модуля variables
from game_sprite import GameSprite              # Импорт класса GameSprite, от которого наследуется Asteroid
import pygame                                   # Импорт библиотеки pygame для функций разработки игр

class Asteroid(GameSprite):                     # Определение класса Asteroid, наследующегося от GameSprite
    def __init__(self, image, x, y, size_x, size_y, speed):  # Конструктор с параметрами для изображения, позиции, размера и скорости
        super().__init__(image, x, y, size_x, size_y, speed)  # Вызов конструктора родительского класса
        self.base_speed = randint(2, 10)        # Установка случайной базовой скорости от 2 до 10
        angle_degrees = randint(-70, 70)        # Генерация случайного угла от -70 до 70 градусов
        angle_radians = math.radians(angle_degrees)  # Преобразование угла из градусов в радианы
        total = abs(math.sin(angle_radians)) + abs(math.cos(angle_radians))  # Расчёт коэффициента нормализации

        if total != 0:                          # Проверка, что коэффициент нормализации не равен нулю
            self.speed_x = (self.base_speed * math.sin(angle_radians)) / total  # Расчёт нормализованной горизонтальной составляющей скорости
            self.speed_y = (self.base_speed * math.cos(angle_radians)) / total  # Расчёт нормализованной вертикальной составляющей скорости
        else:                                   # Обработка крайнего случая, когда коэффициент нормализации равен нулю
            self.speed_x = 0                    # Установка горизонтальной скорости на ноль
            self.speed_y = self.base_speed      # Установка вертикальной скорости равной базовой скорости
            
        self.original_image = self.image        # Сохранение оригинального изображения для вращения
        self.rotation_angle = 0                 # Инициализация угла вращения нулем

    def update(self):                           # Метод для обновления позиции и внешнего вида астероида в каждом кадре
        self.rect.x += self.speed_x             # Обновление горизонтальной позиции на основе speed_x
        self.rect.y += self.speed_y             # Обновление вертикальной позиции на основе speed_y
        self.rotation_angle = (self.rotation_angle + 1) % 360  # Увеличение угла вращения и удержание его в диапазоне 0-359
        self.image = pygame.transform.rotate(self.original_image, self.rotation_angle)  # Вращение изображения на текущий угол
        
        # Проверка, вышел ли астероид за границы экрана
        if self.rect.y > win_height or self.rect.x < -50 or self.rect.x > win_width:
            self.rect.x = randint(80, win_width - 80)  # Сброс позиции x на случайное положение в пределах ширины экрана
            self.rect.y = 0                     # Сброс позиции y на верхнюю часть экрана
            angle_degrees = randint(-45, 45)    # Генерация нового случайного угла от -45 до 45 градусов
            angle_radians = math.radians(angle_degrees)  # Преобразование нового угла из градусов в радианы
            total = abs(math.sin(angle_radians)) + abs(math.cos(angle_radians))  # Расчёт нового коэффициента нормализации
                      
            if total != 0:                      # Проверка, что новый коэффициент нормализации не равен нулю
                self.speed_x = (self.base_speed * math.sin(angle_radians)) / total  # Пересчёт нормализованной горизонтальной скорости
                self.speed_y = (self.base_speed * math.cos(angle_radians)) / total  # Пересчёт нормализованной вертикальной скорости
