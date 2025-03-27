import pygame                                                 # Импортируем библиотеку pygame для создания игры

class BaseExplosion(pygame.sprite.Sprite):                    # Базовый класс для всех типов взрывов, наследуется от pygame.sprite.Sprite
    def __init__(self, x, y, scale=100):                      # Инициализация взрыва с координатами x, y и масштабом (по умолчанию 100)
        pygame.sprite.Sprite.__init__(self)                   # Вызываем конструктор родительского класса Sprite
        self.images = []                                      # Создаем пустой список для хранения кадров анимации
        self.load_explosion_images()                          # Загружаем изображения взрыва (метод должен быть реализован в дочерних классах)
        self.index = 0                                        # Индекс текущего кадра анимации
        self.image = self.images[self.index]                  # Устанавливаем текущее изображение как первый кадр анимации
        self.rect = self.image.get_rect()                     # Получаем прямоугольник для текущего изображения
        self.rect.center = [x, y]                             # Устанавливаем центр прямоугольника в заданные координаты
        self.counter = 0                                      # Счетчик для контроля скорости анимации
        self.explosion_speed = 4                              # Скорость смены кадров анимации

    def update(self):                                         # Метод обновления состояния взрыва
        self.counter += 1                                     # Увеличиваем счетчик
        if self.counter >= self.explosion_speed and self.index < len(self.images) - 1:  # Если прошло достаточно времени и не достигнут последний кадр
            self.counter = 0                                  # Сбрасываем счетчик
            self.index += 1                                   # Переходим к следующему кадру
            self.image = self.images[self.index]              # Обновляем текущее изображение
        if self.index >= len(self.images) - 1 and self.counter >= self.explosion_speed:  # Если достигнут последний кадр и прошло достаточно времени
            self.kill()                                       # Удаляем спрайт

class EnemyExplosion(BaseExplosion):                          # Класс для взрыва врагов, наследуется от BaseExplosion
    def __init__(self, x, y):                                 # Инициализация взрыва врага
        super().__init__(x, y, scale=100)                     # Вызываем конструктор родительского класса
        self.explosion_speed = 4                              # Устанавливаем скорость анимации для врагов

    def load_explosion_images(self):                          # Метод загрузки изображений взрыва врага
        for num in range(1, 6):                               # Загружаем 5 кадров анимации взрыва
            img = pygame.image.load(f'img/exp{num}.png')      # Загружаем изображение
            img = pygame.transform.scale(img, (100, 100))     # Масштабируем изображение до размера 100x100
            self.images.append(img)                           # Добавляем изображение в список кадров

class AsteroidExplosion(BaseExplosion):                       # Класс для взрыва астероидов, наследуется от BaseExplosion
    def __init__(self, x, y):                                 # Инициализация взрыва астероида
        super().__init__(x, y, scale=120)                     # Вызываем конструктор родительского класса с увеличенным масштабом
        self.explosion_speed = 5                              # Устанавливаем более медленную скорость анимации для астероидов
        
    def load_explosion_images(self):                          # Метод загрузки изображений взрыва астероида
        for num in range(1, 7):                               # Загружаем 6 кадров анимации взрыва
            img = pygame.image.load(f'vzriv/vzriv{num}.png')  # Загружаем изображение
            img = pygame.transform.scale(img, (120, 120))     # Масштабируем изображение до размера 120x120
            self.images.append(img)                           # Добавляем изображение в список кадров