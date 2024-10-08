import os
import pygame
from gtts import gTTS
from Util.GetPath import GetPath


class TextToSpeechPlayer:
    def __init__(self, language='en'):
        self.language = language
        pygame.mixer.init()

    def play_text(self, text):
        """将文本转换为语音并播放"""
        tts = gTTS(text=text, lang=self.language)
        mp3_directory = GetPath().get_mp3_path()
        temp_file = mp3_directory
        tts.save(temp_file)

        pygame.mixer.music.load(temp_file)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        # 播放完毕后，删除临时文件
        os.remove(temp_file)

# 使用示例
# player = TextToSpeechPlayer()  # 你可以指定任何支持的语言
# player.play_text("Hello")
