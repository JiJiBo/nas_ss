import asyncio
import os

from back_progress.utils.CreateAudioBookBase import CreateAudioBookBase
from back_progress.utils.config import tesst_dir_data
from back_progress.utils.split_txt import split_txt


class CreateByTxtFile(CreateAudioBookBase):
    def __init__(self, book_id, txt_file_path, saveAudioPath, saveBgmPath, voice, background_music,
                 background_volume_reduction=10, encoding="utf-8",
                 title_pattern=r"(\n\s*第\s*[\d一二三四五六七八九十百千万]+\s*章.*)"):
        super().__init__(book_id, None, saveAudioPath, saveBgmPath, voice, background_music,
                         background_volume_reduction, encoding)
        self.txt_file_path = txt_file_path
        self.title_pattern = title_pattern

    def read_whole_file(self):
        with open(self.txt_file_path, 'r', encoding=self.encoding) as file:
            content = file.read()
            return content

    async def split_by_chapter(self):
        print("阅读中...")
        txt_content = self.read_whole_file()
        self.saveAudioPath = os.path.join(self.saveAudioPath, self.book_name)
        print("音频保存路径：", self.saveAudioPath)
        self.saveBookPath = os.path.join(self.saveBookPath, self.book_name)
        print("书籍保存路径：", self.saveBookPath)
        self.saveBgmPath = os.path.join(self.saveBgmPath, self.book_name)
        print("背景音乐保存路径：", self.saveBgmPath)
        os.makedirs(self.saveAudioPath, exist_ok=True)
        os.makedirs(self.saveBgmPath, exist_ok=True)
        os.makedirs(self.saveBookPath, exist_ok=True)
        print("阅读完成", "总字数", len(txt_content))
        print("分割中...")
        chapters = split_txt(txt_content, self.title_pattern)
        print("分割完成")

        print(self.book_name, "分割结果如下：", len(chapters), "章")
        print("--------------------------------------")
        return chapters


async def main():
    root = tesst_dir_data
    txt_file_path = os.path.join(root, "超级小说.txt")
    background_music = os.path.join(root, "fzg.mp3")
    saveAudioPath = os.path.join(root, "audio")
    saveBgmPath = os.path.join(root, "bgm")
    voice = "zh-CN-YunxiNeural"
    creater = CreateByTxtFile(1, txt_file_path, saveAudioPath, saveBgmPath, voice, background_music, encoding="utf-8")
    await creater.forward()


if __name__ == '__main__':
    asyncio.run(main())
