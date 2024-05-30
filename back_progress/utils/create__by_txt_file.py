import asyncio
import os

from back_progress.utils.CreateAudioBookBase import CreateAudioBookBase
from back_progress.utils.config import tesst_dir_data
from back_progress.utils.split_txt import split_txt



class CreateByTxtFile(CreateAudioBookBase):
    def __init__(self, txt_file_path, saveAudioPath, saveBgmPath, voice, background_music,
                 background_volume_reduction=10, encoding="utf-8", title_pattern=r"第[一二三四五六七八九十1234567890]+章 \S+"):
        super().__init__(None, saveAudioPath, saveBgmPath, voice, background_music, background_volume_reduction, encoding)
        self.txt_file_path = txt_file_path
        self.title_pattern = title_pattern
        self.book_name = os.path.basename(self.txt_file_path).split(".")[0]

    def read_whole_file(self):
        with open(self.txt_file_path, 'r', encoding=self.encoding) as file:
            content = file.read()
            return content

    async def split_by_chapter(self):
        print("阅读中...")
        txt_content = self.read_whole_file()
        print("阅读完成")
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
    creater = CreateByTxtFile(txt_file_path, saveAudioPath, saveBgmPath, voice, background_music, encoding="utf-8")
    await creater.forward()


if __name__ == '__main__':
    asyncio.run(main())
