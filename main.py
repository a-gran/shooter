# Импортируем необходимые библиотеки
import pygame      # Основная библиотека для создания игр
import os         # Для работы с путями к файлам
from random import randint  # Для генерации случайных чисел

# Импортируем все переменные из файла конфигурации
from src.config.variables import *
from src.config.constants import FPS  # Импортируем константу FPS

# Импортируем классы спрайтов
from src.sprites.player import Player       # Класс игрока
from src.sprites.enemy import Enemy         # Класс врага
from src.sprites.asteroid import Asteroid   # Класс астероида

# Импортируем эффекты
from src.effects.explosion import EnemyExplosion, AsteroidExplosion  # Классы взрывов
from src.effects.scrolling_background import ScrollBackground        # Класс для скроллинга фона

# Импортируем утилиты
from src.utils.asset_loader import AssetLoader  # Загрузчик ресурсов

# Скрываем приветственное сообщение pygame
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
pygame.init()       # Инициализируем pygame
pygame.mixer.init() # Инициализируем звуковую подсистему

# Загружаем и настраиваем звуки
pygame.mixer.music.load(AssetLoader.get_asset_path('sounds', 'space.ogg'))  # Фоновая музыка
pygame.mixer.music.play(-1)  # Зацикливаем воспроизведение музыки
fire_sound = AssetLoader.load_sound('fire.ogg')         # Звук выстрела
explosion_sound = AssetLoader.load_sound('explosion.mp3')  # Звук взрыва врага
vzriv_sound = AssetLoader.load_sound('vzriv.ogg')         # Звук взрыва астероида

# Создаем шрифты и текст
font1 = pygame.font.Font(None, 80)  # Шрифт для сообщений о победе/поражении
win = font1.render('YOU WIN!', True, (255, 255, 255))   # Текст победы
lose = font1.render('YOU LOSE!', True, (180, 0, 0))     # Текст поражения
font2 = pygame.font.Font(None, 36)  # Шрифт для счета

# Настраиваем окно игры
pygame.display.set_caption('Shooter')  # Заголовок окна
mw = pygame.display.set_mode((win_width, win_height))  # Создаем окно
bg = pygame.transform.scale(pygame.image.load(img_back), (win_width, win_height))  # Загружаем фон

# Создаем объект фона со скроллингом
background = ScrollBackground(img_back)

# Создаем игрока и группы спрайтов
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)  # Создаем игрока
enemies = pygame.sprite.Group()      # Группа врагов
asteroids = pygame.sprite.Group()    # Группа астероидов
bullets = pygame.sprite.Group()      # Группа пуль
explosions = pygame.sprite.Group()   # Группа взрывов

# Функция добавления нового врага
def add_enemy():
    enemy = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    enemies.add(enemy)

# Функция добавления нового астероида
def add_asteroid():
    asteroid = Asteroid(img_asteroid, randint(80, win_width - 80), -40, 60, 60, 1)
    asteroids.add(asteroid)

# Создаем начальных врагов и астероидов
for i in range(1, 6):
    add_enemy()
for i in range(1, 3):
    add_asteroid()

finish = False  # Флаг завершения игры
run = True     # Флаг работы игры

# Основной игровой цикл
while run:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Если нажат крестик окна
            run = False
        elif event.type == pygame.KEYDOWN:  # Если нажата клавиша
            if event.key == pygame.K_SPACE:  # Если это пробел
                fire_sound.play()  # Воспроизводим звук выстрела
                bullets = ship.fire()  # Создаем пулю

    if not finish:  # Если игра не завершена
        # Обновляем и отрисовываем фон
        background.update()
        background.draw(mw)
        
        # Отображаем счет
        text = font2.render("Score: " + str(score), 1, (255, 255, 255))
        mw.blit(text, (10, 20))
        
        # Обновляем все спрайты
        ship.update()
        enemies.update()
        asteroids.update()
        bullets.update()
        explosions.update()
        
        # Отрисовываем все спрайты
        ship.reset(mw)
        enemies.draw(mw)
        asteroids.draw(mw)
        bullets.draw(mw)
        explosions.draw(mw)

        # Проверяем столкновения пуль с врагами
        collisions = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for collision in collisions:
            # Создаем взрыв
            explosion1 = EnemyExplosion(collision.rect.centerx, collision.rect.centery)
            explosions.add(explosion1)
            explosion_sound.play()  # Звук взрыва
            score += 1  # Увеличиваем счет
            
            if score >= 10:  # Если достигнут счет для победы
                # Ждем завершения анимации взрыва
                while len(explosions) > 0:
                    background.update()
                    background.draw(mw)
                    text = font2.render("Score: " + str(score), 1, (255, 255, 255))
                    mw.blit(text, (10, 20))
                    explosions.update()
                    explosions.draw(mw)
                    pygame.display.update()
                    pygame.time.delay(20)
                
                pygame.time.delay(500)  # Дополнительная пауза
                mw.blit(win, (win_width//2-100, win_height//2-50))  # Показываем победу
                finish = True  # Завершаем игру
            else:
                add_enemy()  # Добавляем нового врага

        # Проверяем столкновения пуль с астероидами
        asteroid_hits = pygame.sprite.groupcollide(asteroids, bullets, True, True)
        for hit in asteroid_hits:
            # Создаем взрыв астероида
            explosion2 = AsteroidExplosion(hit.rect.centerx, hit.rect.centery)
            explosions.add(explosion2)
            vzriv_sound.play()  # Звук взрыва астероида
            add_asteroid()  # Добавляем новый астероид

        # Проверяем условие поражения
        if lost >= max_lost:  # Если пропущено максимальное количество врагов
            mw.blit(lose, (win_width//2-100, win_height//2-50))  # Показываем поражение
            finish = True  # Завершаем игру

    pygame.display.update()  # Обновляем экран
    pygame.time.delay(1000 // FPS)  # Задержка для поддержания FPS

pygame.quit()  # Закрываем pygame при выходе