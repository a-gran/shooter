from src.utils.asset_loader import AssetLoader

# Определяем пути к файлам изображений
img_back = AssetLoader.get_asset_path('backgrounds', 'space1.jpg')
img_hero = AssetLoader.get_asset_path('ships', 'spaceship.png')
img_enemy = AssetLoader.get_asset_path('ships', 'transport.png')
img_asteroid = AssetLoader.get_asset_path('objects', 'asteroid.png')
img_bullet = AssetLoader.get_asset_path('objects', 'bullet.png')

score = 0  # Инициализируем счетчик набранных очков
lost = 0   # Инициализируем счетчик пропущенных врагов
max_lost = 3  # Устанавливаем максимальное допустимое количество пропущенных врагов
win_width = 1000  # Устанавливаем ширину игрового окна
win_height = 800  # Устанавливаем высоту игрового окна