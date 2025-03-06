from game_sprite import GameSprite  # Импортируем класс GameSprite из модуля game_sprite

class Bullet(GameSprite):  # Создаем класс Bullet, который наследуется от GameSprite
    def update(self):  # Определяем метод update, который будет обновлять состояние пули
        self.rect.y += self.speed  # Изменяем положение пули по вертикали согласно ее скорости
        if self.rect.y < 0:  # Проверяем, вышла ли пуля за верхнюю границу экрана
            self.kill()  # Если пуля вышла за границу экрана, удаляем её из всех групп спрайтов
