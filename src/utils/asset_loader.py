import pygame
import os

class AssetLoader:
    @staticmethod
    def get_asset_path(category, filename):
        """Get the full path for an asset file"""
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        return os.path.join(base_dir, 'assets', category, filename)

    @staticmethod
    def load_image(category, filename):
        """Load an image asset"""
        full_path = AssetLoader.get_asset_path(category, filename)
        return pygame.image.load(full_path)

    @staticmethod
    def load_sound(filename):
        """Load a sound asset"""
        full_path = AssetLoader.get_asset_path('sounds', filename)
        return pygame.mixer.Sound(full_path)

    @staticmethod
    def load_explosion_frames(explosion_type):
        """Load explosion animation frames"""
        frames = []
        directory = 'explosions/' + explosion_type
        if explosion_type == 'enemy':
            frame_count = 5
            prefix = 'exp'
        else:  # asteroid
            frame_count = 6
            prefix = 'vzriv'
            
        for i in range(1, frame_count + 1):
            filename = f"{prefix}{i}.png"
            full_path = AssetLoader.get_asset_path(directory, filename)
            frames.append(pygame.image.load(full_path))
        return frames