import time

import pygame

def play_mp3(file_path):
    time.sleep(3)
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


if __name__ == "__main__":
    mp3_file = "/data/mp3/Entry_level 2-1/Veryhappy.mp3"  # 你的MP3文件路径
    play_mp3(mp3_file)
