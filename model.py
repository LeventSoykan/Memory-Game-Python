
#Game Level
#High Scores List
#Shuffled Images
import random
import os


class GameData:
    def __init__(self, player_name=None, image_directory="thumb"):
        self.game_name = 'MEMORY GAME' + ' ' + player_name
        self.image_directory = image_directory

    @property
    def images(self):
        """get paths for images"""
        images = [f'{self.image_directory}\\' + x for x in os.listdir(self.image_directory)]*2
        random.shuffle(images)
        return images


if __name__ == '__main__':
    data = GameData('GUEST')
    print(data.images)
    print(data.game_name)