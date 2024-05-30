import os

from back_progress.utils.add_back import add_back
from back_progress.utils.split_txt import split_txt
from back_progress.utils.txt2voice import text2audio


class CreateByTxtFile:
    def __init__(self, txt_file_path, saveAudioPath, saveBgmPath, voice, background_music,
                 background_volume_reduction=10,
                 title_pattern=r"第[一二三四五六七八九十1234567890]+章 \S+"):
        self.txt_file_path = txt_file_path
        self.title_pattern = title_pattern
        self.saveAudioPath = saveAudioPath
        self.saveBgmPath = saveBgmPath
        self.voice = voice
        self.background_music = background_music
        self.background_volume_reduction = background_volume_reduction

    # 读取整个文件
    def read_whole_file(self):
        with open(self.txt_file_path, 'r') as file:
            content = file.read()
            return content

    # 按照章分割
    def split_by_chapter(self):
        txt_content = self.read_whole_file()
        chapters = split_txt(txt_content, self.title_pattern)
        return chapters

    # 阅读一章小说
    async def read_one_chapter(self, title, content):
        savePath = os.path.join(self.saveAudioPath, f"{title}.mp3")
        data = content, savePath, self.voice
        await text2audio(data)
        return savePath, title

    # 给一章小说加背景音
    def add_bg_music(self, from_path, title, background_music, background_volume_reduction):
        to_path = os.path.join(self.saveBgmPath, f"{title}.mp3")
        data = from_path, to_path, background_music, background_volume_reduction
        add_back(data)
        return data
    # 一步方法
    async def forward(self):
        chapters = self.split_by_chapter()
        for title, content in chapters.items():
            savePath, title = await self.read_one_chapter(title, content)
            self.add_bg_music(savePath, title, self.background_music, self.background_volume_reduction)
            print(f"{title} 完成")
            print("--------------------------------------")
