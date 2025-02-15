# Импортируем библиотеку pygame для создания игры
import pygame

# Базовый класс для всех типов взрывов, наследуется от pygame.sprite.Sprite
class BaseExplosion(pygame.sprite.Sprite):
    # Инициализация взрыва с координатами x, y и масштабом (по умолчанию 100)
    def __init__(self, x, y, scale=100):
        # Вызываем конструктор родительского класса Sprite
        pygame.sprite.Sprite.__init__(self)
        # Создаем пустой список для хранения кадров анимации
        self.images = []
        # Загружаем изображения взрыва (метод должен быть реализован в дочерних классах)
        self.load_explosion_images()
        # Индекс текущего кадра анимации
        self.index = 0
        # Устанавливаем текущее изображение как первый кадр анимации
        self.image = self.images[self.index]
        # Получаем прямоугольник для текущего изображения
        self.rect = self.image.get_rect()
        # Устанавливаем центр прямоугольника в заданные координаты
        self.rect.center = [x, y]
        # Счетчик для контроля скорости анимации
        self.counter = 0
        # Скорость смены кадров анимации
        self.explosion_speed = 4

    # Метод обновления состояния взрыва
    def update(self):
        # Увеличиваем счетчик
        self.counter += 1
        # Если прошло достаточно времени и не достигнут последний кадр
        if self.counter >= self.explosion_speed and self.index < len(self.images) - 1:
            # Сбрасываем счетчик
            self.counter = 0
            # Переходим к следующему кадру
            self.index += 1
            # Обновляем текущее изображение
            self.image = self.images[self.index]
        # Если достигнут последний кадр и прошло достаточно времени
        if self.index >= len(self.images) - 1 and self.counter >= self.explosion_speed:
            # Удаляем спрайт
            self.kill()

# Класс для взрыва врагов, наследуется от BaseExplosion
class EnemyExplosion(BaseExplosion):
    # Инициализация взрыва врага
    def __init__(self, x, y):
        # Вызываем конструктор родительского класса
        super().__init__(x, y, scale=100)
        # Устанавливаем скорость анимации для врагов
        self.explosion_speed = 4

    # Метод загрузки изображений взрыва врага
    def load_explosion_images(self):
        # Загружаем 5 кадров анимации взрыва
        for num in range(1, 6):
            # Загружаем изображение
            img = pygame.image.load(f"img/exp{num}.png")
            # Масштабируем изображение до размера 100x100
            img = pygame.transform.scale(img, (100, 100))
            # Добавляем изображение в список кадров
            self.images.append(img)

# Класс для взрыва астероидов, наследуется от BaseExplosion
class AsteroidExplosion(BaseExplosion):
    # Инициализация взрыва астероида
    def __init__(self, x, y):
        # Вызываем конструктор родительского класса с увеличенным масштабом
        super().__init__(x, y, scale=120)
        # Устанавливаем более медленную скорость анимации для астероидов
        self.explosion_speed = 5
        
    # Метод загрузки изображений взрыва астероида
    def load_explosion_images(self):
        # Загружаем 6 кадров анимации взрыва
        for num in range(1, 7):
            # Загружаем изображение
            img = pygame.image.load(f"vzriv/vzriv{num}.png")
            # Масштабируем изображение до размера 120x120
            img = pygame.transform.scale(img, (120, 120))
            # Добавляем изображение в список кадров
            self.images.append(img)