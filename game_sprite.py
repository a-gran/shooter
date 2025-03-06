import pygame  # Импортирует библиотеку pygame для создания игр

class GameSprite(pygame.sprite.Sprite):  # Создает класс GameSprite, наследуемый от pygame.sprite.Sprite
    def __init__(self, image, x, y, size_x, size_y, speed):  # Конструктор класса с параметрами
        super().__init__()  # Вызывает конструктор родительского класса pygame.sprite.Sprite
        self.image = pygame.transform.scale(pygame.image.load(image), (size_x, size_y))  # Загружает изображение и масштабирует его
        self.speed = speed  # Устанавливает скорость спрайта
        self.rect = self.image.get_rect()  # Получает прямоугольник изображения (для коллизий)
        self.rect.x = x  # Устанавливает начальную x-координату спрайта
        self.rect.y = y  # Устанавливает начальную y-координату спрайта

    def reset(self, mw):  # Метод для отображения спрайта на экране
        mw.blit(self.image, (self.rect.x, self.rect.y))  # Отрисовывает изображение на поверхности mw по координатам спрайта
