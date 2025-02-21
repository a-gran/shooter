# Импортируем основной модуль pygame для создания игры
import pygame
# Импортируем функцию randint для генерации случайных чисел
from random import randint
# Импортируем все переменные из файла variables.py
from variables import *
# Импортируем все флаги из файла flags.py
from flags import *
# Импортируем класс Player для создания игрока
from player import Player
# Импортируем класс Enemy для создания врагов
from enemy import Enemy
# Импортируем класс Asteroid для создания астероидов
from asteroid import Asteroid
# Импортируем все классы, связанные со взрывами
from explosion import *
# Импортируем класс для создания скроллящегося фона
from scrolling_background import ScrollBackground
# Импортируем модуль os для работы с операционной системой
import os

# Скрываем приветственное сообщение pygame
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

# Инициализируем все модули pygame
pygame.init()
# Инициализируем модуль для работы со звуком
pygame.mixer.init()

# Загружаем и запускаем фоновую музыку
pygame.mixer.music.load('space.ogg')
pygame.mixer.music.play()
# Загружаем звук выстрела
fire_sound = pygame.mixer.Sound('fire.ogg')
# Загружаем звуки взрывов
explosion_sound = pygame.mixer.Sound('explosion.mp3')
vzriv_sound = pygame.mixer.Sound('vzriv.ogg')

# Создаем шрифт большого размера для сообщений о победе/поражении
font1 = pygame.font.Font(None, 80)
# Создаем надпись "YOU WIN!" белого цвета
win = font1.render('YOU WIN!', True, (255, 255, 255))
# Создаем надпись "YOU LOSE!" красного цвета
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
# Создаем шрифт меньшего размера для счета
font2 = pygame.font.Font(None, 36)

# Устанавливаем заголовок окна игры
pygame.display.set_caption('Shooter')
# Создаем игровое окно заданного размера
mw = pygame.display.set_mode((win_width, win_height))
# Загружаем и масштабируем фоновое изображение
bg = pygame.transform.scale(pygame.image.load(img_back), (win_width, win_height))

# Создаем объект скроллящегося фона
background = ScrollBackground(img_back)

# Создаем игрока (космический корабль)
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
# Создаем группу для хранения врагов
enemies = pygame.sprite.Group()
# Создаем группу для хранения астероидов
asteroids = pygame.sprite.Group()
# Создаем группу для хранения пуль
bullets = pygame.sprite.Group()
# Создаем группу для хранения эффектов взрыва
explosions = pygame.sprite.Group()

# Функция для добавления нового врага
def add_enemy():
    # Создаем врага со случайной позицией по X и случайной скоростью
    enemy = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    # Добавляем врага в группу врагов
    enemies.add(enemy)

# Функция для добавления нового астероида
def add_asteroid():
    # Создаем астероид со случайной позицией по X
    asteroid = Asteroid(img_asteroid, randint(80, win_width - 80), -40, 60, 60, 1)
    # Добавляем астероид в группу астероидов
    asteroids.add(asteroid)

# Создаем начальное количество врагов (5 штук)
for i in range(1, 6):
    add_enemy()

# Создаем начальное количество астероидов (2 штуки)
for i in range(1, 3):
    add_asteroid()

# Основной игровой цикл
while run:
    # Обрабатываем все события в очереди pygame
    for event in pygame.event.get():
        # Если нажат крестик окна - завершаем игру
        if event.type == pygame.QUIT:
            run = False
        # Если нажата клавиша
        elif event.type == pygame.KEYDOWN:
            # Если нажат пробел - стреляем
            if event.key == pygame.K_SPACE:
                # Воспроизводим звук выстрела
                fire_sound.play()
                # Создаем пулю
                bullets = ship.fire()

    # Если игра не завершена
    if not finish:
        # Обновляем положение фона
        background.update()
        # Отрисовываем фон
        background.draw(mw)        
        
        # Создаем и отображаем текст со счетом
        text = font2.render("Score: " + str(score), 1, (255, 255, 255))
        mw.blit(text, (10, 20))
        
        # Обновляем положение всех спрайтов и отрисовываем все спрайты
        if not explosion_in_progress:
            ship.update()
            enemies.update()
            asteroids.update()
            bullets.update()
            ship.reset(mw)
            enemies.draw(mw)
            asteroids.draw(mw)
            bullets.draw(mw)
        
        explosions.update()
        explosions.draw(mw)

        # Проверяем столкновения пуль с врагами
        if not explosion_in_progress:
            collisions = pygame.sprite.groupcollide(enemies, bullets, True, True)
            # Обрабатываем каждое столкновение
            for collision in collisions:
                # Создаем эффект взрыва врага
                explosion1 = EnemyExplosion(collision.rect.centerx, collision.rect.centery)
                # Добавляем взрыв в группу взрывов
                explosions.add(explosion1)
                # Воспроизводим звук взрыва
                explosion_sound.play()
                # Увеличиваем счет
                score += 1                
                # Проверяем достижение победного счета
                if score >= score_win:
                    win_explosion_in_progress = True
                    explosion_start_time = pygame.time.get_ticks()
                else:
                    # Добавляем нового врага только если не достигнут победный счет
                    add_enemy()

            # Проверяем столкновения пуль с астероидами
            asteroid_hits = pygame.sprite.groupcollide(asteroids, bullets, True, True)
            # Обрабатываем каждое столкновение
            for hit in asteroid_hits:
                # Создаем эффект взрыва астероида
                explosion2 = AsteroidExplosion(hit.rect.centerx, hit.rect.centery)
                # Добавляем взрыв в группу взрывов
                explosions.add(explosion2)
                # Воспроизводим звук взрыва астероида
                vzriv_sound.play()
                # Добавляем новый астероид
                add_asteroid()

            # Проверяем столкновение игрока с врагами
            enemy_collision = pygame.sprite.spritecollide(ship, enemies, False)
            if enemy_collision:
                # Создаем эффект взрыва врага
                for enemy in enemy_collision:
                    explosion1 = EnemyExplosion(enemy.rect.centerx, enemy.rect.centery)
                    explosions.add(explosion1)
                # Создаем эффект взрыва корабля игрока
                ship_explosion = EnemyExplosion(ship.rect.centerx, ship.rect.centery)
                explosions.add(ship_explosion)                
                explosion_sound.play() # Воспроизводим звук взрыва                
                explosion_start_time = pygame.time.get_ticks() # Начинаем отсчет времени взрыва
                explosion_in_progress = True                
                ship.kill() # Скрываем спрайты

            # Проверяем столкновение игрока с астероидами
            asteroid_collision = pygame.sprite.spritecollide(ship, asteroids, False)
            if asteroid_collision:
                # Создаем эффект взрыва астероида
                for asteroid in asteroid_collision:
                    explosion2 = AsteroidExplosion(asteroid.rect.centerx, asteroid.rect.centery)
                    explosions.add(explosion2)
                # Создаем эффект взрыва корабля игрока
                ship_explosion = EnemyExplosion(ship.rect.centerx, ship.rect.centery)
                explosions.add(ship_explosion)                
                vzriv_sound.play() # Воспроизводим звук взрыва                
                explosion_start_time = pygame.time.get_ticks() # Начинаем отсчет времени взрыва
                explosion_in_progress = True               
                ship.kill()  # Скрываем спрайты

        # Если взрыв в процессе, проверяем, не пора ли показать game over
        if explosion_in_progress and not show_game_over:
            current_time = pygame.time.get_ticks()
            if current_time - explosion_start_time >= EXPLOSION_DURATION:
                show_game_over = True
                finish = True

        # Показываем game over только после завершения анимации взрыва
        if show_game_over:
            mw.blit(lose, (win_width//2-100, win_height//2-50))

        # Проверяем условия победы (набрано 10 очков)
        if score >= score_win:
            if win_explosion_in_progress:
                current_time = pygame.time.get_ticks()
                if current_time - explosion_start_time >= EXPLOSION_DURATION:
                    # Отображаем сообщение о победе только после завершения анимации
                    mw.blit(win, (win_width//2-100, win_height//2-50))
                    finish = True
            else:
                # Если нет активной анимации взрыва, сразу показываем победу
                mw.blit(win, (win_width//2-100, win_height//2-50))
                finish = True

    # Обновляем экран
    pygame.display.update()
    # Устанавливаем задержку для поддержания заданного FPS
    pygame.time.delay(1000 // FPS)

# Закрываем pygame
pygame.quit()