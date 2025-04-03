import pygame                                                    # Импорт основного модуля pygame
from random import randint                                            # Импорт функции для случайных чисел
import os                                                             # Импорт модуля для работы с ОС
from variables import *                                               # Импорт всех переменных из файла variables.py
from flags import *                                                   # Импорт всех флагов из файла flags.py
from player import Player                                             # Импорт класса игрока
from enemy import Enemy                                               # Импорт класса врага
from asteroid import Asteroid                                         # Импорт класса астероида
from explosion import *                                               # Импорт всех классов взрывов
from scrolling_background import ScrollBackground                     # Импорт класса для скроллящегося фона

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"                     # Скрытие приветственного сообщения pygame

pygame.init()                                                         # Инициализация всех модулей pygame

pygame.mixer.music.load('space.ogg')                                  # Загрузка фоновой музыки
pygame.mixer.music.play()                                             # Воспроизведение фоновой музыки
fire_sound = pygame.mixer.Sound('fire.ogg')                           # Загрузка звука выстрела
explosion_sound = pygame.mixer.Sound('explosion.mp3')                 # Загрузка звука взрыва
vzriv_sound = pygame.mixer.Sound('vzriv.ogg')                         # Загрузка альтернативного звука взрыва

font1 = pygame.font.Font(None, 80)                                    # Создание крупного шрифта
win = font1.render('YOU WIN!', True, (255, 255, 255))                 # Создание текста победы белого цвета
lose = font1.render('YOU LOSE!', True, (180, 0, 0))                   # Создание текста поражения красного цвета
font2 = pygame.font.Font(None, 36)                                    # Создание шрифта меньшего размера для счета

pygame.display.set_caption('Shooter')                                 # Установка заголовка окна
mw = pygame.display.set_mode((win_width, win_height))                 # Создание игрового окна
bg = pygame.transform.scale(pygame.image.load(img_back), (win_width, win_height))  # Загрузка и масштабирование фона

background = ScrollBackground(img_back)                               # Создание объекта скроллящегося фона

ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)             # Создание корабля игрока
enemies = pygame.sprite.Group()                                       # Создание группы врагов
asteroids = pygame.sprite.Group()                                     # Создание группы астероидов
bullets = pygame.sprite.Group()                                       # Создание группы пуль
explosions = pygame.sprite.Group()                                    # Создание группы взрывов

def add_enemy():                                                      # Определение функции для добавления врага
    enemy = Enemy(img_ship, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))  # Создание врага со случайными параметрами
    enemies.add(enemy)                                                # Добавление врага в группу

def add_asteroid():                                                   # Определение функции для добавления астероида
    asteroid = Asteroid(img_asteroid, randint(80, win_width - 80), -40, 60, 60, 1)  # Создание астероида со случайной позицией
    asteroids.add(asteroid)                                           # Добавление астероида в группу

for i in range(1, 10):                                                # Цикл для создания начальных врагов
    add_enemy()                                                       # Добавление врага

for i in range(1, 10):                                                # Цикл для создания начальных астероидов
    add_asteroid()                                                    # Добавление астероида

while run:                                                            # Основной игровой цикл
    for event in pygame.event.get():                                  # Обработка всех событий
        if event.type == pygame.QUIT:                                 # Проверка на выход из игры
            run = False                                               # Остановка игрового цикла
        elif event.type == pygame.KEYDOWN:                            # Проверка на нажатие клавиши
            if event.key == pygame.K_SPACE:                           # Проверка на нажатие пробела
                fire_sound.play()                                      # Воспроизведение звука выстрела
                bullets = ship.fire()                                  # Создание пули

    if not finish:                                                    # Проверка, не завершена ли игра
        background.update()                                           # Обновление положения фона
        background.draw(mw)                                           # Отрисовка фона
        
        text = font2.render("Score: " + str(score), 1, (255, 255, 255))  # Создание текста со счетом
        mw.blit(text, (10, 20))                                       # Отображение счета
        
        if not explosion_in_progress:                                 # Проверка, нет ли активного взрыва
            ship.update()                                             # Обновление позиции корабля
            enemies.update()                                          # Обновление позиций врагов
            asteroids.update()                                        # Обновление позиций астероидов
            bullets.update()                                          # Обновление позиций пуль
            ship.reset(mw)                                            # Отрисовка корабля
            enemies.draw(mw)                                          # Отрисовка врагов
            asteroids.draw(mw)                                        # Отрисовка астероидов
            bullets.draw(mw)                                          # Отрисовка пуль
        
        explosions.update()                                           # Обновление анимаций взрывов
        explosions.draw(mw)                                           # Отрисовка взрывов

        if not explosion_in_progress:                                 # Проверка, нет ли активного взрыва
            collisions = pygame.sprite.groupcollide(enemies, bullets, True, True)  # Проверка столкновений пуль с врагами
            for collision in collisions:                              # Обработка каждого столкновения
                explosion1 = EnemyExplosion(collision.rect.centerx, collision.rect.centery)  # Создание эффекта взрыва
                explosions.add(explosion1)                            # Добавление взрыва в группу
                explosion_sound.play()                                # Воспроизведение звука взрыва
                score += 1                                            # Увеличение счета
                if score >= score_win:                                # Проверка достижения победного счета
                    win_explosion_in_progress = True                  # Установка флага взрыва при победе
                    explosion_start_time = pygame.time.get_ticks()    # Запоминание времени начала взрыва
                else:
                    add_enemy()                                       # Добавление нового врага

            asteroid_hits = pygame.sprite.groupcollide(asteroids, bullets, True, True)  # Проверка столкновений пуль с астероидами
            for hit in asteroid_hits:                                 # Обработка каждого столкновения
                explosion2 = AsteroidExplosion(hit.rect.centerx, hit.rect.centery)  # Создание эффекта взрыва астероида
                explosions.add(explosion2)                            # Добавление взрыва в группу
                vzriv_sound.play()                                    # Воспроизведение звука взрыва
                add_asteroid()                                        # Добавление нового астероида

            enemy_collision = pygame.sprite.spritecollide(ship, enemies, False)  # Проверка столкновения корабля с врагами
            if enemy_collision:                                       # Если произошло столкновение с врагом
                for enemy in enemy_collision:                         # Обработка каждого столкнувшегося врага
                    explosion1 = EnemyExplosion(enemy.rect.centerx, enemy.rect.centery)  # Создание эффекта взрыва врага
                    explosions.add(explosion1)                        # Добавление взрыва в группу
                ship_explosion = EnemyExplosion(ship.rect.centerx, ship.rect.centery)  # Создание эффекта взрыва корабля
                explosions.add(ship_explosion)                        # Добавление взрыва в группу
                explosion_sound.play()                                # Воспроизведение звука взрыва
                explosion_start_time = pygame.time.get_ticks()        # Запоминание времени начала взрыва
                explosion_in_progress = True                          # Установка флага активного взрыва
                ship.kill()                                           # Удаление спрайта корабля

            asteroid_collision = pygame.sprite.spritecollide(ship, asteroids, False)  # Проверка столкновения корабля с астероидами
            if asteroid_collision:                                    # Если произошло столкновение с астероидом
                for asteroid in asteroid_collision:                   # Обработка каждого столкнувшегося астероида
                    explosion2 = AsteroidExplosion(asteroid.rect.centerx, asteroid.rect.centery)  # Создание эффекта взрыва астероида
                    explosions.add(explosion2)                        # Добавление взрыва в группу
                ship_explosion = EnemyExplosion(ship.rect.centerx, ship.rect.centery)  # Создание эффекта взрыва корабля
                explosions.add(ship_explosion)                        # Добавление взрыва в группу
                vzriv_sound.play()                                    # Воспроизведение звука взрыва
                explosion_start_time = pygame.time.get_ticks()        # Запоминание времени начала взрыва
                explosion_in_progress = True                          # Установка флага активного взрыва
                ship.kill()                                           # Удаление спрайта корабля

        if explosion_in_progress and not show_game_over:              # Проверка активности взрыва и отсутствия экрана проигрыша
            current_time = pygame.time.get_ticks()                    # Получение текущего времени
            if current_time - explosion_start_time >= EXPLOSION_DURATION:  # Проверка длительности взрыва
                show_game_over = True                                 # Установка флага показа экрана проигрыша
                finish = True                                         # Установка флага завершения игры

        if show_game_over:                                            # Проверка флага показа экрана проигрыша
            mw.blit(lose, (win_width//2-100, win_height//2-50))       # Отображение сообщения о проигрыше

        if score >= score_win:                                        # Проверка достижения победного счета
            if win_explosion_in_progress:                             # Если активен взрыв при победе
                current_time = pygame.time.get_ticks()                # Получение текущего времени
                if current_time - explosion_start_time >= EXPLOSION_DURATION:  # Проверка длительности взрыва
                    mw.blit(win, (win_width//2-100, win_height//2-50))# Отображение сообщения о победе
                    finish = True                                     # Установка флага завершения игры
            else:
                mw.blit(win, (win_width//2-100, win_height//2-50))    # Отображение сообщения о победе
                finish = True                                         # Установка флага завершения игры

    pygame.display.update()                                           # Обновление экрана
    pygame.time.delay(1000 // FPS)                                    # Задержка для поддержания FPS

pygame.quit()                                                         # Закрытие pygame